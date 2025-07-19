from flask import Flask, render_template
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'police-case-analysis-secret-key123')
    
    # Initialize database
    from .models.database import init_db
    db_session = init_db()()
    
    # Initialize services
    from .services.auth_service import AuthService, setup_login_manager
    from .services.ai_service import AIService
    from .services.gemini_document_service import GeminiDocumentService
    from .services.chat_service import ChatService
    auth_service = AuthService(db_session)
    login_manager = setup_login_manager(app, auth_service)
    document_service = GeminiDocumentService(db_session)
    ai_service = AIService(document_service)
    chat_service = ChatService(db_session, ai_service)
    
    # Initialize controllers
    from .controllers.auth_controller import init_auth_controller
    from .controllers.admin_controller import init_admin_controller
    from .controllers.chat_controller import init_chat_controller
    from .controllers.main_controller import init_main_controller
    from .controllers.document_controller import init_document_controller
    
    app.register_blueprint(init_auth_controller(auth_service))
    app.register_blueprint(init_admin_controller(document_service))
    app.register_blueprint(init_chat_controller(chat_service))
    app.register_blueprint(init_main_controller())
    
    # Add document controller for source highlighting
    from .controllers.document_controller import init_document_controller
    app.register_blueprint(init_document_controller(db_session))    
    # Template context processor
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Cleanup database session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.close()
    
    return app
