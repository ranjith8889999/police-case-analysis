from app import create_app
import os

if __name__ == "__main__":
    app = create_app()
    
    # Performance optimization settings
    app.config['TEMPLATES_AUTO_RELOAD'] = False  # Disable auto-reloading templates in production
    
    # Use production server when not debugging
    if os.environ.get('FLASK_ENV') != 'development':
        app.config['DEBUG'] = False
        app.run(host='0.0.0.0', port=5000, threaded=True)
    else:
        # Development mode
        app.run(debug=True, port=5000)
