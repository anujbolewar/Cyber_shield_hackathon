#!/bin/bash

# Heroku Deployment Script
# Prerequisites: Heroku CLI installed and logged in

echo "🚀 Deploying Police AI Monitor to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "Please log in to Heroku first:"
    heroku login
fi

# Create Heroku app
echo "Creating Heroku app..."
APP_NAME="police-ai-monitor-$(date +%s)"
heroku create $APP_NAME

# Set environment variables
echo "Setting environment variables..."
heroku config:set STREAMLIT_SERVER_PORT=\$PORT -a $APP_NAME
heroku config:set STREAMLIT_SERVER_ADDRESS=0.0.0.0 -a $APP_NAME

# Deploy to Heroku
echo "Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

echo "✅ Deployment complete!"
echo "🌐 Your app is available at: https://$APP_NAME.herokuapp.com"
echo ""
echo "📊 To view logs: heroku logs --tail -a $APP_NAME"
echo "⚙️ To open app: heroku open -a $APP_NAME"
