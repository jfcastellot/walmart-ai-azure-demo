"""
Entrenamiento del modelo de forecast de ventas semanales.

Uso local (smoke test):
    python -m src.ml.train_forecast

En Azure ML se invoca como componente del pipeline.
"""
import argparse
import os
from pathlib import Path

import joblib
import mlflow
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def load_walmart_data(data_dir: Path) -> pd.DataFrame:
    """Carga y une las 3 tablas del dataset de Walmart Kaggle."""
    train = pd.read_csv(data_dir / "train.csv", parse_dates=["Date"])
    features = pd.read_csv(data_dir / "features.csv", parse_dates=["Date"])
    stores = pd.read_csv(data_dir / "stores.csv")

    df = train.merge(features, on=["Store", "Date", "IsHoliday"], how="left")
    df = df.merge(stores, on="Store", how="left")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Crea features temporales y categóricas básicas."""
    df = df.copy()
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
    df["DayOfYear"] = df["Date"].dt.dayofyear

    # One-hot para tipo de tienda (A/B/C)
    df = pd.get_dummies(df, columns=["Type"], prefix="StoreType")

    # Rellenar NaNs de markdowns con 0 (no había promo)
    markdown_cols = [c for c in df.columns if c.startswith("MarkDown")]
    df[markdown_cols] = df[markdown_cols].fillna(0)

    # Rellenar CPI y Unemployment con mediana
    df["CPI"] = df["CPI"].fillna(df["CPI"].median())
    df["Unemployment"] = df["Unemployment"].fillna(df["Unemployment"].median())

    return df


def split_temporal(df: pd.DataFrame, test_weeks: int = 8):
    """Split temporal — NO usar random split en series de tiempo."""
    cutoff = df["Date"].max() - pd.Timedelta(weeks=test_weeks)
    train = df[df["Date"] <= cutoff]
    test = df[df["Date"] > cutoff]
    return train, test


def train_model(
    train_df: pd.DataFrame,
    feature_cols: list,
    target: str,
    n_estimators: int = 100,
    max_depth: int = 15,
    random_state: int = 42,
) -> RandomForestRegressor:
    """Entrena un RandomForest con los features dados."""
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(train_df[feature_cols], train_df[target])
    return model


def evaluate(model, test_df: pd.DataFrame, feature_cols: list, target: str) -> dict:
    """Calcula MAE, RMSE y R² en el set de prueba."""
    preds = model.predict(test_df[feature_cols])
    mae = mean_absolute_error(test_df[target], preds)
    rmse = np.sqrt(mean_squared_error(test_df[target], preds))
    r2 = r2_score(test_df[target], preds)
    return {"mae": mae, "rmse": rmse, "r2": r2}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--max-depth", type=int, default=15)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    mlflow.set_experiment("walmart-forecast")
    with mlflow.start_run():
        print("📥 Cargando datos...")
        df = load_walmart_data(args.data_dir)
        print(f"   Filas: {len(df):,}")

        print("🔧 Feature engineering...")
        df = engineer_features(df)

        print("✂️  Split temporal...")
        train_df, test_df = split_temporal(df, test_weeks=8)
        print(f"   Train: {len(train_df):,} | Test: {len(test_df):,}")

        feature_cols = [
            "Store", "Dept", "IsHoliday", "Temperature", "Fuel_Price",
            "CPI", "Unemployment", "Size", "Year", "Month", "Week", "DayOfYear",
            "MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5",
            "StoreType_A", "StoreType_B", "StoreType_C",
        ]
        target = "Weekly_Sales"

        print("🧠 Entrenando RandomForest...")
        model = train_model(
            train_df, feature_cols, target,
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
        )

        print("📊 Evaluando...")
        metrics = evaluate(model, test_df, feature_cols, target)
        print(f"   MAE:  ${metrics['mae']:,.2f}")
        print(f"   RMSE: ${metrics['rmse']:,.2f}")
        print(f"   R²:   {metrics['r2']:.4f}")

        # Log a MLflow
        mlflow.log_params({
            "n_estimators": args.n_estimators,
            "max_depth": args.max_depth,
            "test_weeks": 8,
        })
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "model")

        # Guardar modelo local
        model_path = args.output_dir / "forecast_model.joblib"
        joblib.dump(model, model_path)
        print(f"💾 Modelo guardado en {model_path}")


if __name__ == "__main__":
    main()
