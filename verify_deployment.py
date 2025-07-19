"""
Quick verification script to test the application before deployment.
Run this to ensure everything is working properly.
"""

import os
import sys
import importlib.util

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'sqlalchemy', 'psycopg2', 'langchain',
        'google.generativeai', 'pgvector', 'gunicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'google.generativeai':
                import google.generativeai
            elif package == 'psycopg2':
                import psycopg2
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_environment_variables():
    """Check if required environment variables are set."""
    print("\n🔍 Checking environment variables...")
    
    required_vars = ['GOOGLE_API_KEY', 'DATABASE_URL']
    optional_vars = ['FLASK_SECRET_KEY', 'FLASK_ENV']
    
    missing_required = []
    
    for var in required_vars:
        if os.environ.get(var):
            print(f"  ✅ {var} is set")
        else:
            print(f"  ❌ {var} is missing")
            missing_required.append(var)
    
    for var in optional_vars:
        if os.environ.get(var):
            print(f"  ✅ {var} is set")
        else:
            print(f"  ⚠️  {var} is not set (optional)")
    
    if missing_required:
        print(f"\n⚠️  Missing required variables: {', '.join(missing_required)}")
        print("Create a .env file with these variables.")
        return False
    
    print("✅ Required environment variables are set!")
    return True

def check_database_connection():
    """Test database connection."""
    print("\n🔍 Testing database connection...")
    
    try:
        from app.models.database import init_db
        from sqlalchemy import text
        Session = init_db()
        session = Session()
        
        # Test basic query
        result = session.execute(text("SELECT 1")).fetchone()
        session.close()
        
        print("✅ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Check your DATABASE_URL and ensure PostgreSQL is running.")
        return False

def check_api_keys():
    """Test API keys."""
    print("\n🔍 Testing API keys...")
    
    try:
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        # Test a simple query
        response = ai_service.direct_query("Hello")
        
        if response and "error" not in response.lower():
            print("✅ Google Gemini API key is working!")
            return True
        else:
            print("❌ Google Gemini API key test failed")
            return False
            
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

def main():
    """Run all checks."""
    print("🚀 Police Case Analysis - Pre-deployment Verification")
    print("=" * 55)
    
    checks = [
        check_dependencies,
        check_environment_variables,
        check_database_connection,
        check_api_keys
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 55)
    
    if all_passed:
        print("🎉 All checks passed! Your application is ready for deployment.")
        print("\nNext steps:")
        print("1. Run deploy.bat (Windows) or deploy.sh (Linux/Mac)")
        print("2. Choose your deployment platform")
        print("3. Follow the platform-specific instructions")
    else:
        print("❌ Some checks failed. Please fix the issues before deploying.")
        print("\nCommon solutions:")
        print("- Run: pip install -r requirements.txt")
        print("- Create .env file with required variables")
        print("- Check database connection settings")
        print("- Verify Google Gemini API key")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
