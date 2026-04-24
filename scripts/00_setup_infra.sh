#!/bin/bash
# =============================================================================
# Script de setup de infraestructura base en Azure
# Ejecutar una sola vez después de `az login`
# =============================================================================

set -e  # Detenerse ante cualquier error

# Cargar variables del .env
if [ ! -f "config/.env" ]; then
    echo "❌ Error: no existe config/.env. Copia config/.env.example primero."
    exit 1
fi
export $(grep -v '^#' config/.env | xargs)

echo "🚀 Creando infraestructura en Azure..."
echo "   Suscripción: $AZURE_SUBSCRIPTION_ID"
echo "   Resource Group: $AZURE_RESOURCE_GROUP"
echo "   Location: $AZURE_LOCATION"

# 1. Resource Group
echo ""
echo "📦 Paso 1: Resource Group"
az group create \
    --name "$AZURE_RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --output table

# 2. Storage Account (para el dataset)
echo ""
echo "📦 Paso 2: Storage Account"
az storage account create \
    --name "$AZURE_STORAGE_ACCOUNT" \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --sku Standard_LRS \
    --output table

# 3. Container dentro del Storage
STORAGE_KEY=$(az storage account keys list \
    --account-name "$AZURE_STORAGE_ACCOUNT" \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --query "[0].value" -o tsv)

az storage container create \
    --name "$AZURE_STORAGE_CONTAINER" \
    --account-name "$AZURE_STORAGE_ACCOUNT" \
    --account-key "$STORAGE_KEY" \
    --output table

# 4. Azure Machine Learning Workspace
echo ""
echo "📦 Paso 3: Azure ML Workspace (tarda 3-5 min)"
az ml workspace create \
    --name "$AZUREML_WORKSPACE_NAME" \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --output table

# 5. Compute cluster (apagado cuando no se usa, barato)
echo ""
echo "📦 Paso 4: Compute cluster"
az ml compute create \
    --name "$AZUREML_COMPUTE_NAME" \
    --type AmlCompute \
    --min-instances 0 \
    --max-instances 2 \
    --size Standard_DS3_v2 \
    --idle-time-before-scale-down 300 \
    --workspace-name "$AZUREML_WORKSPACE_NAME" \
    --resource-group "$AZURE_RESOURCE_GROUP"

echo ""
echo "✅ Infraestructura base creada."
echo ""
echo "⚠️  IMPORTANTE: Azure OpenAI y Azure Data Factory los crearás en los días correspondientes (4 y 7)."
echo ""
echo "Siguiente paso: abrir Azure ML Studio en https://ml.azure.com"
