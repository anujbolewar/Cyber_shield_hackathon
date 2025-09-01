#!/bin/bash

# Google Cloud Run Deployment Script
# Prerequisites: gcloud CLI installed and configured

echo "🚀 Deploying Police AI Monitor to Google Cloud Run..."

# Variables (customize these)
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="police-ai-monitor"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Check if gcloud is configured
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Please configure gcloud first:"
    echo "gcloud auth login"
    echo "gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and push image using Cloud Build
echo "Building image with Cloud Build..."
gcloud builds submit --tag $IMAGE_NAME -f Dockerfile_deploy .

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8501 \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10

echo "✅ Deployment complete!"
echo "🌐 Your app is available at:"
gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'
