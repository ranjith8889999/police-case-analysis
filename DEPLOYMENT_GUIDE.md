# 🚀 RAILWAY DEPLOYMENT GUIDE (RECOMMENDED)

## Why Railway?
- ✅ Free PostgreSQL database with pgvector support
- ✅ Easy GitHub integration
- ✅ Automatic deployments
- ✅ $5/month free credits (enough for your app)
- ✅ Built-in domain and HTTPS

## Step-by-Step Deployment

### 1. Prepare Your Code
```bash
# Make sure you're in your project directory
cd "c:\Users\Ranjit\Desktop\Python\Police Case Analysis"

# Create .env file (do this locally, don't commit it)
copy .env.example .env
# Edit .env with your Google API key
```

### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit for deployment"
git branch -M main
git remote add origin https://github.com/yourusername/police-case-analysis.git
git push -u origin main
```

### 3. Deploy on Railway

1. **Go to Railway.app**
   - Visit: https://railway.app
   - Sign up with GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add PostgreSQL Database**
   - In your project dashboard, click "New Service"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically create a PostgreSQL instance

4. **Configure Environment Variables**
   - Go to your web service settings
   - Add these variables:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key
   FLASK_SECRET_KEY=your_super_secret_key_here
   FLASK_ENV=production
   ```
   - DATABASE_URL will be automatically set by Railway

5. **Enable pgvector Extension**
   - Go to PostgreSQL service
   - Click "Query" tab
   - Run: `CREATE EXTENSION IF NOT EXISTS vector;`

6. **Deploy**
   - Railway automatically deploys your app
   - Visit the provided URL

### 4. Initialize Database
After first deployment, run database setup:
- Use Railway's built-in terminal or local connection
- Run your setup scripts

## Environment Variables in Railway:
```
DATABASE_URL=postgresql://... (automatically set)
GOOGLE_API_KEY=your_actual_api_key
FLASK_SECRET_KEY=your_secret_key
FLASK_ENV=production
```

## Estimated Monthly Cost: $0 (within free limits)

---

# 🔄 RENDER DEPLOYMENT GUIDE (ALTERNATIVE)

## Why Render?
- ✅ Free tier available
- ✅ PostgreSQL database
- ✅ Automatic HTTPS
- ✅ GitHub integration

## Step-by-Step Deployment

### 1. Prepare Code (same as Railway)

### 2. Deploy on Render

1. **Go to Render.com**
   - Visit: https://render.com
   - Sign up with GitHub

2. **Create PostgreSQL Database**
   - Click "New" → "PostgreSQL"
   - Choose free tier
   - Note down database details

3. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn run:app`

4. **Set Environment Variables**
   ```
   DATABASE_URL=your_postgres_url_from_render
   GOOGLE_API_KEY=your_google_gemini_api_key
   FLASK_SECRET_KEY=your_secret_key
   FLASK_ENV=production
   ```

5. **Enable pgvector**
   - Connect to your database
   - Run: `CREATE EXTENSION IF NOT EXISTS vector;`

## Estimated Monthly Cost: $0 (free tier)

---

# 🚢 HEROKU DEPLOYMENT GUIDE (CLASSIC)

## Why Heroku?
- ✅ Well-documented
- ✅ Large ecosystem
- ✅ Free PostgreSQL (limited)

## Step-by-Step Deployment

### 1. Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

### 2. Prepare and Deploy
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-police-case-app

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:essential-0

# Set environment variables
heroku config:set GOOGLE_API_KEY=your_api_key
heroku config:set FLASK_SECRET_KEY=your_secret_key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Enable pgvector (if supported)
heroku pg:psql -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## Estimated Monthly Cost: $0-5 (depending on usage)

---

# 🛠️ GENERAL TROUBLESHOOTING

## Common Issues and Solutions

### 1. Database Connection Errors
- Verify DATABASE_URL format
- Check pgvector extension is installed
- Ensure database is accessible

### 2. File Upload Issues
- Check upload folder permissions
- Verify file size limits

### 3. Memory Issues
- Optimize chunk processing
- Consider reducing embedding dimensions

### 4. API Key Issues
- Verify Google Gemini API key is valid
- Check API quotas and limits

## Performance Tips
1. Use database connection pooling
2. Implement caching for frequent queries
3. Optimize file upload handling
4. Monitor memory usage

## Security Recommendations
1. Use environment variables for all secrets
2. Enable HTTPS (automatic on most platforms)
3. Implement proper input validation
4. Regular security updates

---

# 📞 SUPPORT

If you encounter issues:
1. Check platform-specific documentation
2. Review application logs
3. Test database connectivity
4. Verify environment variables

Choose Railway for the easiest setup with the best PostgreSQL support!
