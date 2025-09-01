#!/bin/bash

# Azure Container Instances Deployment Script
# Prerequisites: Azure CLI installed and logged in

echo "🚀 Deploying Police AI Monitor to Azure Container Instances..."

# Variables (customize these)
RESOURCE_GROUP="police-ai-monitor-rg"
CONTAINER_NAME="police-ai-monitor"
REGISTRY_NAME="policeaimonitoracr"
LOCATION="eastus"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Please install it first:"
    echo "https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
echo "Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $REGISTRY_NAME --sku Basic --admin-enabled true

# Get ACR credentials
ACR_SERVER=$(az acr show --name $REGISTRY_NAME --resource-group $RESOURCE_GROUP --query "loginServer" --output tsv)
ACR_USERNAME=$(az acr credential show --name $REGISTRY_NAME --resource-group $RESOURCE_GROUP --query "username" --output tsv)
ACR_PASSWORD=$(az acr credential show --name $REGISTRY_NAME --resource-group $RESOURCE_GROUP --query "passwords[0].value" --output tsv)

# Build and push image
echo "Building and pushing Docker image..."
docker build -t $ACR_SERVER/police-ai-monitor:latest -f Dockerfile_deploy .
docker login $ACR_SERVER --username $ACR_USERNAME --password $ACR_PASSWORD
docker push $ACR_SERVER/police-ai-monitor:latest

# Deploy to Azure Container Instances
echo "Deploying to Azure Container Instances..."
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --image $ACR_SERVER/police-ai-monitor:latest \
    --registry-login-server $ACR_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --dns-name-label police-ai-monitor-$(date +%s) \
    --ports 8501 \
    --cpu 1 \
    --memory 1.5 \
    --restart-policy Always

# Get public IP
PUBLIC_IP=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn --output tsv)

echo "✅ Deployment complete!"
echo "🌐 Your app is available at: http://$PUBLIC_IP:8501"
