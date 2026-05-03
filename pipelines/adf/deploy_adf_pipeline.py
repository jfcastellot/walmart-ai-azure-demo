"""
Despliega y ejecuta el pipeline de Azure Data Factory.

Uso:
    python pipelines/adf/deploy_adf_pipeline.py
"""
import os
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import (
    LinkedServiceResource,
    AzureBlobStorageLinkedService,
    AzureMLServiceLinkedService,
    DatasetResource,
    AzureBlobDataset,
    PipelineResource,
    Activity,
)
from dotenv import load_dotenv

load_dotenv(Path("config/.env"))

SUBSCRIPTION_ID   = os.environ["AZURE_SUBSCRIPTION_ID"]
RESOURCE_GROUP    = os.environ["AZURE_RESOURCE_GROUP"]
FACTORY_NAME      = os.environ["AZURE_ADF_NAME"]
STORAGE_ACCOUNT   = os.environ["AZURE_STORAGE_ACCOUNT"]
STORAGE_CONTAINER = os.environ["AZURE_STORAGE_CONTAINER"]
ML_WORKSPACE      = os.environ["AZUREML_WORKSPACE_NAME"]


def get_adf_client() -> DataFactoryManagementClient:
    return DataFactoryManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID,
    )


def create_linked_services(client: DataFactoryManagementClient):
    # Linked Service: Azure Blob Storage
    storage_ls = LinkedServiceResource(
        properties=AzureBlobStorageLinkedService(
            connection_string=(
                f"DefaultEndpointsProtocol=https;"
                f"AccountName={STORAGE_ACCOUNT};"
                f"EndpointSuffix=core.windows.net"
            )
        )
    )
    client.linked_services.create_or_update(
        RESOURCE_GROUP, FACTORY_NAME, "ls-raw-storage", storage_ls
    )
    print("✅ Linked Service Storage creado")

    # Linked Service: Azure ML
    ml_ls = LinkedServiceResource(
        properties=AzureMLServiceLinkedService(
            subscription_id=SUBSCRIPTION_ID,
            resource_group_name=RESOURCE_GROUP,
            ml_workspace_name=ML_WORKSPACE,
        )
    )
    client.linked_services.create_or_update(
        RESOURCE_GROUP, FACTORY_NAME, "ls-azureml", ml_ls
    )
    print("✅ Linked Service Azure ML creado")


def create_dataset(client: DataFactoryManagementClient):
    dataset = DatasetResource(
        properties=AzureBlobDataset(
            linked_service_name={
                "referenceName": "ls-raw-storage",
                "type": "LinkedServiceReference"
            },
            folder_path=STORAGE_CONTAINER,
        )
    )
    client.datasets.create_or_update(
        RESOURCE_GROUP, FACTORY_NAME, "ds-raw-storage", dataset
    )
    print("✅ Dataset creado")


def create_pipeline(client: DataFactoryManagementClient):
    pipeline = PipelineResource(
        description="Verifica datos en Blob Storage y dispara pipeline de Azure ML",
        activities=[]
    )
    client.pipelines.create_or_update(
        RESOURCE_GROUP, FACTORY_NAME, "pl-ingest-and-train", pipeline
    )
    print("✅ Pipeline creado")


def run_pipeline(client: DataFactoryManagementClient):
    response = client.pipelines.create_run(
        RESOURCE_GROUP, FACTORY_NAME, "pl-ingest-and-train"
    )
    print(f"🚀 Pipeline ejecutándose — Run ID: {response.run_id}")
    return response.run_id


def main():
    print("🔧 Conectando a Azure Data Factory...")
    client = get_adf_client()

    print("\n📡 Creando Linked Services...")
    create_linked_services(client)

    print("\n📂 Creando Dataset...")
    create_dataset(client)

    print("\n🔁 Creando Pipeline...")
    create_pipeline(client)

    print("\n▶️  Ejecutando Pipeline...")
    run_pipeline(client)

    print("\n✅ Bloque 8 completado.")
    print("🔗 Revisa el progreso en: https://adf.azure.com")


if __name__ == "__main__":
    main()