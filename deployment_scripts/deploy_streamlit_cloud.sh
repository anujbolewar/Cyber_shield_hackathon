#!/bin/bash

# Streamlit Community Cloud Deployment Script
# Run this script to prepare your app for Streamlit Community Cloud

echo "🚀 Preparing Police AI Monitor for Streamlit Community Cloud deployment..."

# Check if git repository is initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git branch -M main
fi

# Check if GitHub repository exists
echo "Please ensure your GitHub repository is created:"
echo "1. Go to https://github.com/new"
echo "2. Repository name: police-ai-monitor"
echo "3. Make it public for free Streamlit Cloud hosting"
echo "4. Don't initialize with README (we have our own)"

read -p "Press Enter when GitHub repository is created..."

# Add files to git
echo "Adding files to git..."
git add streamlit_app.py
git add requirements_deploy.txt
git add .streamlit/

# Check if streamlit config exists
if [ ! -d ".streamlit" ]; then
    mkdir .streamlit
    cat > .streamlit/config.toml << EOF
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#1e3a8a"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
EOF
fi

# Commit changes
echo "Committing changes..."
git add .
git commit -m "Deploy: Streamlit Community Cloud setup"

echo "📋 Next Steps:"
echo "1. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/police-ai-monitor.git"
echo "   git push -u origin main"
echo ""
echo "2. Deploy on Streamlit Community Cloud:"
echo "   - Go to https://share.streamlit.io"
echo "   - Sign in with GitHub"
echo "   - Click 'Deploy an app'"
echo "   - Repository: YOUR_USERNAME/police-ai-monitor"
echo "   - Branch: main"
echo "   - Main file path: streamlit_app.py"
echo ""
echo "✅ Streamlit Cloud deployment preparation complete!"
