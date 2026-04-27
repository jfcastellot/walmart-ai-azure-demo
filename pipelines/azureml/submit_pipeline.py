"""
Somete el pipeline de entrenamiento a Azure Machine Learning.

Uso:
    python pipelines/azureml/submit_pipeline.py
"""
import os
from pathlib import Path

from azure.ai.ml import MLClient, Input, command
from azure.ai.ml.dsl import pipeline
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(Path("config/.env"))


def get_ml_client() -> MLClient:
    return MLClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
        resource_group_name=os.environ["AZURE_RESOURCE_GROUP"],
        workspace_name=os.environ["AZUREML_WORKSPACE_NAME"],
    )


# ---------------------------------------------------------------------------
# Componentes del pipeline (cada uno corre un script)
# ---------------------------------------------------------------------------

train_forecast_component = command(
    name="train_forecast",
    display_name="Entrenar modelo de forecast",
    inputs={"data_dir": Input(type="uri_folder")},
    outputs={"model_dir": {"type": "uri_folder", "mode": "rw_mount"}},
    code="./src/ml",
    command=(
        "python train_forecast.py "
        "--data-dir ${{inputs.data_dir}} "
        "--output-dir ${{outputs.model_dir}}"
    ),
    environment="azureml:AzureML-sklearn-1.5@latest",
)

train_clustering_component = command(
    name="train_clustering",
    display_name="Entrenar clustering de tiendas",
    inputs={"data_dir": Input(type="uri_folder")},
    outputs={"model_dir": {"type": "uri_folder", "mode": "rw_mount"}},
    code="./src/ml",
    command=(
        "python train_clustering.py "
        "--data-dir ${{inputs.data_dir}} "
        "--output-dir ${{outputs.model_dir}}"
    ),
    environment="azureml:AzureML-sklearn-1.5@latest",
)


# ---------------------------------------------------------------------------
# Pipeline — orquesta los componentes en paralelo
# ---------------------------------------------------------------------------

@pipeline(
    name="walmart-training-pipeline",
    description="Entrena forecast + clustering en paralelo",
    default_compute=os.environ.get("AZUREML_COMPUTE_NAME", "cpu-cluster"),
)
def training_pipeline(input_data: Input):
    forecast_step = train_forecast_component(data_dir=input_data)
    clustering_step = train_clustering_component(data_dir=input_data)
    return {
        "forecast_model": forecast_step.outputs.model_dir,
        "clustering_model": clustering_step.outputs.model_dir,
    }


def main():
    ml_client = get_ml_client()

    # Referencia al data asset (lo registras en Día 1 vía UI o CLI)
    data_input = Input(
        type="uri_folder",
        path=f"azureml:walmart-raw-dataset:1",
    )

    job = training_pipeline(input_data=data_input)
    job.experiment_name = "walmart-training"

    print("🚀 Enviando pipeline a Azure ML...")
    submitted = ml_client.jobs.create_or_update(job)
    print(f"✅ Job: {submitted.name}")
    print(f"🔗 URL: {submitted.studio_url}")


if __name__ == "__main__":
    main()
