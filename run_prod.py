from app import create_app
import os

# Create the Flask app
app = create_app()

# Production optimizations
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.config['DEBUG'] = False

# Security settings for production
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

if __name__ == "__main__":
    # This is for local testing only
    # In production, gunicorn will handle this
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
