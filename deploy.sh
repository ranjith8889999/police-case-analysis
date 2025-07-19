#!/bin/bash

# Police Case Analysis - Quick Deployment Script
# This script helps you deploy to Railway, Render, or Heroku

echo "🚀 Police Case Analysis - Deployment Helper"
echo "==========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
    git branch -M main
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "Choose your deployment platform:"
echo "1. Railway (Recommended - Best PostgreSQL support)"
echo "2. Render (Good alternative)"
echo "3. Heroku (Classic option)"
echo "4. Just prepare files (no deployment)"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🚂 Railway Deployment Selected"
        echo ""
        echo "Next steps:"
        echo "1. Go to https://railway.app"
        echo "2. Sign up with your GitHub account"
        echo "3. Create new project from GitHub repo"
        echo "4. Add PostgreSQL database service"
        echo "5. Set environment variables:"
        echo "   - GOOGLE_API_KEY=your_gemini_api_key"
        echo "   - FLASK_SECRET_KEY=your_secret_key"
        echo "6. Enable pgvector: CREATE EXTENSION IF NOT EXISTS vector;"
        echo ""
        echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;
    2)
        echo "🎨 Render Deployment Selected"
        echo ""
        echo "Next steps:"
        echo "1. Go to https://render.com"
        echo "2. Sign up with your GitHub account"
        echo "3. Create PostgreSQL database first"
        echo "4. Create web service from GitHub repo"
        echo "5. Set environment variables"
        echo "6. Enable pgvector extension"
        echo ""
        echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;
    3)
        echo "⚡ Heroku Deployment Selected"
        echo ""
        if command -v heroku &> /dev/null; then
            echo "✅ Heroku CLI found"
            echo "Run these commands:"
            echo "heroku login"
            echo "heroku create your-app-name"
            echo "heroku addons:create heroku-postgresql:essential-0"
            echo "heroku config:set GOOGLE_API_KEY=your_api_key"
            echo "heroku config:set FLASK_SECRET_KEY=your_secret_key"
            echo "git push heroku main"
        else
            echo "❌ Heroku CLI not found"
            echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
        fi
        echo ""
        echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;
    4)
        echo "📝 Files prepared for deployment"
        echo "All deployment configuration files are ready"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🔧 Important: Don't forget to:"
echo "1. Create a new Google Gemini API key (revoke the exposed one)"
echo "2. Set up your environment variables on the platform"
echo "3. Enable pgvector extension in your PostgreSQL database"
echo "4. Run database initialization after first deployment"
echo ""
echo "📚 For detailed guides, check DEPLOYMENT_GUIDE.md"
echo "✅ Deployment preparation complete!"
