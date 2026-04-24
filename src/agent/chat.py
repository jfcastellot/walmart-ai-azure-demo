"""
Agente conversacional que consume los modelos de forecast y clustering
usando Semantic Kernel + Azure OpenAI.

Uso:
    python -m src.agent.chat
"""
import asyncio
import os
from pathlib import Path
from typing import Annotated

import joblib
import pandas as pd
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions import kernel_function

load_dotenv(Path("config/.env"))


# =========================================================================
# PLUGINS — herramientas que el agente puede invocar
# =========================================================================

class ForecastPlugin:
    """Plugin que expone el modelo de predicción de ventas."""

    def __init__(self, model_path: str = "outputs/forecast_model.joblib"):
        self.model = joblib.load(model_path) if Path(model_path).exists() else None

    @kernel_function(
        description="Predice las ventas semanales para una tienda y departamento específicos. "
                    "Úsalo cuando el usuario pregunte por predicciones, pronósticos o forecast."
    )
    def predict_sales(
        self,
        store_id: Annotated[int, "ID numérico de la tienda (1-45)"],
        dept_id: Annotated[int, "ID numérico del departamento (1-99)"],
        week: Annotated[int, "Número de semana del año (1-52)"],
    ) -> Annotated[str, "Predicción de ventas en USD con intervalo de confianza"]:
        if self.model is None:
            return "Modelo no disponible. Ejecuta primero src.ml.train_forecast."
        # Nota: en producción esto consultaría el endpoint de Azure ML
        # Para la demo, hacemos una predicción simplificada
        return (
            f"Predicción para Tienda {store_id}, Depto {dept_id}, Semana {week}: "
            f"[este es un placeholder — se conectará al endpoint real en Día 3]"
        )


class ClusterPlugin:
    """Plugin que expone los resultados de clusterización."""

    def __init__(self, clusters_path: str = "outputs/store_clusters.csv"):
        self.clusters = (
            pd.read_csv(clusters_path) if Path(clusters_path).exists() else None
        )

    @kernel_function(
        description="Obtiene el cluster al que pertenece una tienda y las características "
                    "del cluster. Úsalo cuando pregunten sobre segmentación, grupos, o tiendas similares."
    )
    def get_store_cluster(
        self,
        store_id: Annotated[int, "ID numérico de la tienda"],
    ) -> Annotated[str, "Descripción del cluster al que pertenece la tienda"]:
        if self.clusters is None:
            return "Clusters no disponibles. Ejecuta primero src.ml.train_clustering."
        row = self.clusters[self.clusters["Store"] == store_id]
        if row.empty:
            return f"Tienda {store_id} no encontrada."
        cluster = int(row["cluster"].iloc[0])
        avg_sales = float(row["avg_weekly_sales"].iloc[0])
        size = float(row["size"].iloc[0])
        return (
            f"Tienda {store_id} → Cluster {cluster}. "
            f"Ventas promedio semanales: ${avg_sales:,.0f}. "
            f"Tamaño: {size:,.0f} ft². "
            f"Pertenece al grupo de tiendas con comportamiento similar."
        )

    @kernel_function(
        description="Lista todas las tiendas que pertenecen a un cluster específico."
    )
    def stores_in_cluster(
        self,
        cluster_id: Annotated[int, "ID del cluster"],
    ) -> Annotated[str, "Lista de tiendas del cluster con sus métricas"]:
        if self.clusters is None:
            return "Clusters no disponibles."
        subset = self.clusters[self.clusters["cluster"] == cluster_id]
        if subset.empty:
            return f"Cluster {cluster_id} no existe."
        lines = [f"Cluster {cluster_id} tiene {len(subset)} tiendas:"]
        for _, r in subset.iterrows():
            lines.append(
                f"  - Tienda {int(r['Store'])}: ${r['avg_weekly_sales']:,.0f}/sem, "
                f"{int(r['size']):,} ft²"
            )
        return "\n".join(lines)


# =========================================================================
# AGENTE
# =========================================================================

SYSTEM_INSTRUCTIONS = """Eres un asistente analítico para gerentes de categoría de Walmart México.
Respondes en español natural, de forma ejecutiva y concisa.

Tienes acceso a dos herramientas:
1. ForecastPlugin: predice ventas semanales por tienda y departamento.
2. ClusterPlugin: identifica segmentos de tiendas con comportamiento similar.

Cuando el usuario haga una pregunta de negocio, decide qué plugin invocar.
Si necesitas múltiples datos, llama a varios plugins en secuencia.
Siempre contextualiza los números con una interpretación de negocio breve.
"""


def build_agent() -> ChatCompletionAgent:
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        )
    )
    kernel.add_plugin(ForecastPlugin(), plugin_name="Forecast")
    kernel.add_plugin(ClusterPlugin(), plugin_name="Cluster")

    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="WalmartInsightsAgent",
        instructions=SYSTEM_INSTRUCTIONS,
        arguments=None,
    )
    return agent


async def chat_loop():
    agent = build_agent()
    print("🤖 Agente Walmart Insights listo. Escribe 'salir' para terminar.\n")
    history = []
    while True:
        user_input = input("Tú: ").strip()
        if user_input.lower() in {"salir", "exit", "quit"}:
            break
        if not user_input:
            continue
        history.append({"role": "user", "content": user_input})
        print("Agente: ", end="", flush=True)
        async for response in agent.invoke(messages=user_input):
            print(response.message.content, end="")
        print("\n")


if __name__ == "__main__":
    asyncio.run(chat_loop())
