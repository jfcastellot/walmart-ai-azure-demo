"""
Clusterización de tiendas por comportamiento de ventas.

Uso local:
    python -m src.ml.train_clustering
"""
import argparse
from pathlib import Path

import joblib
import mlflow
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def build_store_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega métricas a nivel tienda para clusterizar."""
    profile = df.groupby("Store").agg(
        avg_weekly_sales=("Weekly_Sales", "mean"),
        std_weekly_sales=("Weekly_Sales", "std"),
        max_weekly_sales=("Weekly_Sales", "max"),
        total_sales=("Weekly_Sales", "sum"),
        n_departments=("Dept", "nunique"),
        size=("Size", "first"),
        avg_temperature=("Temperature", "mean"),
        avg_unemployment=("Unemployment", "mean"),
    ).reset_index()

    # Estacionalidad: desviación estándar por tienda en diciembre vs promedio
    dec_sales = df[df["Date"].dt.month == 12].groupby("Store")["Weekly_Sales"].mean()
    profile["dec_sales_lift"] = profile["Store"].map(dec_sales) / profile["avg_weekly_sales"]
    profile["dec_sales_lift"] = profile["dec_sales_lift"].fillna(1.0)

    return profile


def find_best_k(X_scaled: np.ndarray, k_range=range(2, 8)) -> tuple[int, dict]:
    """Prueba varios k y devuelve el mejor por silhouette score."""
    scores = {}
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        scores[k] = silhouette_score(X_scaled, labels)
    best_k = max(scores, key=scores.get)
    return best_k, scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    mlflow.set_experiment("walmart-clustering")
    with mlflow.start_run():
        print("📥 Cargando datos...")
        train = pd.read_csv(args.data_dir / "train.csv", parse_dates=["Date"])
        features = pd.read_csv(args.data_dir / "features.csv", parse_dates=["Date"])
        stores = pd.read_csv(args.data_dir / "stores.csv")
        df = train.merge(features, on=["Store", "Date", "IsHoliday"], how="left")
        df = df.merge(stores, on="Store", how="left")

        print("🔧 Construyendo perfil por tienda...")
        profile = build_store_profile(df)
        print(f"   {len(profile)} tiendas perfiladas")

        feature_cols = [
            "avg_weekly_sales", "std_weekly_sales", "max_weekly_sales",
            "total_sales", "n_departments", "size",
            "avg_temperature", "avg_unemployment", "dec_sales_lift",
        ]

        print("📏 Normalizando features...")
        scaler = StandardScaler()
        X = scaler.fit_transform(profile[feature_cols])

        print("🔍 Buscando mejor k...")
        best_k, scores = find_best_k(X)
        print(f"   Mejor k = {best_k} (silhouette = {scores[best_k]:.3f})")

        print(f"🎯 Entrenando KMeans con k={best_k}...")
        km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        profile["cluster"] = km.fit_predict(X)

        # PCA para visualización
        pca = PCA(n_components=2)
        coords = pca.fit_transform(X)
        profile["pca_x"] = coords[:, 0]
        profile["pca_y"] = coords[:, 1]

        # Log a MLflow
        mlflow.log_params({"k": best_k, "n_features": len(feature_cols)})
        mlflow.log_metric("silhouette_score", scores[best_k])
        for k, s in scores.items():
            mlflow.log_metric(f"silhouette_k_{k}", s)

        # Guardar modelo y perfil
        joblib.dump({"scaler": scaler, "kmeans": km, "pca": pca}, args.output_dir / "clustering_model.joblib")
        profile.to_csv(args.output_dir / "store_clusters.csv", index=False)
        print(f"💾 Guardado en {args.output_dir}")

        # Resumen por cluster
        summary = profile.groupby("cluster").agg(
            n_stores=("Store", "count"),
            avg_sales=("avg_weekly_sales", "mean"),
            avg_size=("size", "mean"),
        ).round(2)
        print("\n📋 Resumen por cluster:")
        print(summary)


if __name__ == "__main__":
    main()
