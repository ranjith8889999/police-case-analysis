# 🎯 QUICK START GUIDE - After Deployment

## 📋 Post-Deployment Checklist

### ✅ 1. Access Your Application
- Visit your deployed URL
- Test the health endpoint: `https://your-app-url/health`
- Should see: `{"status": "healthy", "message": "Police Case Analysis System is running"}`

### ✅ 2. Initialize Database
Run these SQL commands in your PostgreSQL database:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify tables are created
\dt

-- Check if admin user exists (optional)
SELECT * FROM users WHERE username = 'admin';
```

### ✅ 3. Create Admin User
If no admin user exists, create one:

```python
# Run this in your deployment platform's console or locally
python create_default_users.py
```

### ✅ 4. Test Core Functionality

1. **Login Test**
   - Go to `/login`
   - Use admin credentials or create new account

2. **Upload Test**
   - Login to dashboard
   - Try uploading a small PDF file
   - Check if file appears in document management

3. **Chat Test**
   - Go to any analysis section
   - Ask a simple question
   - Verify AI response (even if "no documents found")

4. **Database Test**
   - Check if documents are stored in database
   - Verify embeddings are generated

### ✅ 5. Configure Environment Variables

Make sure these are set on your platform:

```
# Required
GOOGLE_API_KEY=your_new_google_gemini_api_key
DATABASE_URL=postgresql://... (auto-set by platform)

# Recommended
FLASK_SECRET_KEY=your_secure_random_key
FLASK_ENV=production

# Optional
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=app/static/uploads
```

### ✅ 6. Security Setup

1. **Revoke Old API Key**
   - Go to Google AI Studio
   - Revoke the exposed API key: `AIzaSyC2tznCdJX-y9YzEuE_USCA3BVUuo1-av4`
   - Create new API key

2. **Set Secure Secret Key**
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```
   Use output as FLASK_SECRET_KEY

3. **Enable HTTPS**
   - Most platforms auto-enable this
   - Verify SSL certificate is working

### ✅ 7. Performance Optimization

1. **Database Connection Pooling**
   - Already configured in `database.py`
   - Monitor connection usage

2. **File Upload Limits**
   - Default: 16MB max file size
   - Adjust if needed for your use case

3. **Memory Management**
   - Monitor app memory usage
   - Consider upgrading plan if needed

### ✅ 8. Monitoring Setup

1. **Check Logs**
   - Platform dashboard → Logs
   - Look for any errors or warnings

2. **Database Monitoring**
   - Check database usage
   - Monitor query performance

3. **API Usage**
   - Monitor Google Gemini API usage
   - Set up billing alerts if needed

### 🚨 Troubleshooting Common Issues

#### Database Connection Errors
```
- Check DATABASE_URL format
- Verify pgvector extension is installed
- Check database permissions
```

#### API Key Errors
```
- Verify GOOGLE_API_KEY is set correctly
- Check API key permissions in Google Cloud
- Monitor API quotas and limits
```

#### File Upload Failures
```
- Check upload directory permissions
- Verify file size limits
- Check available disk space
```

#### Memory Issues
```
- Monitor app memory usage
- Consider reducing chunk size
- Upgrade to higher tier plan
```

### 📞 Getting Help

1. **Check Application Logs**
   - Platform dashboard → Logs section
   - Look for Python stack traces

2. **Database Issues**
   - Use platform's database console
   - Run diagnostic queries

3. **Performance Issues**
   - Check resource usage metrics
   - Consider plan upgrades

### 🎉 Success Indicators

Your deployment is successful when:
- ✅ Health check returns HTTP 200
- ✅ Login page loads correctly
- ✅ File upload works (even if no AI response yet)
- ✅ Database queries execute without errors
- ✅ No critical errors in application logs

---

## 🚀 Your Application URLs

Replace `your-app-name` with your actual deployment URL:

- **Main App**: `https://your-app-name.railway.app/`
- **Health Check**: `https://your-app-name.railway.app/health`
- **Login**: `https://your-app-name.railway.app/login`
- **Dashboard**: `https://your-app-name.railway.app/dashboard`

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Google Gemini API Docs](https://ai.google.dev/)

---

**Congratulations! Your Police Case Analysis System is now deployed! 🎉**
