from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from ..models.database import User
from ..utils.db_utils import retry_db_operation

class AuthService:
    def __init__(self, db_session):
        """
        Initialize the authentication service.
          Args:
            db_session: SQLAlchemy session for database operations
        """
        self.db_session = db_session
        
    def register_user(self, username, email, password):
        """
        Register a new user.
        
        Args:
            username (str): Username
            email (str): User email
            password (str): User password
            
        Returns:
            User, str: Created user object and message
        """
        # Check if user already exists by email
        existing_user = self.db_session.query(User).filter_by(email=email).first()
        if existing_user:
            return None, "Email already registered"
        
        # Check if username already exists
        existing_username = self.db_session.query(User).filter_by(username=username).first()
        if existing_username:
            return None, "Username already taken"
        
        # Hash password
        hashed_password = generate_password_hash(password)
          # Create new user
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            self.db_session.add(new_user)
            self.db_session.commit()
            return new_user, "Registration successful"
        except Exception as e:
            self.db_session.rollback()
            return None, f"Registration failed: {str(e)}"
    
    def authenticate(self, email, password):
        """
        Authenticate a user.
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            User, str: User object if authentication successful and message
        """
        # Retry logic for database connection issues
        user = None
        for attempt in range(3):
            try:
                user = self.db_session.query(User).filter_by(email=email).first()
                break
            except Exception as e:
                print(f"DB query attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    import time
                    time.sleep(0.5)
                    continue
                else:
                    return None, "Database connection failed"
        
        if not user:
            return None, "User not found"
        
        if check_password_hash(user.password, password):
            return user, "Authentication successful"
        else:
            return None, "Incorrect password"
    
    def get_user_by_id(self, user_id):
        """
        Get a user by ID.
        
        Args:
            user_id (int): User ID
            
        Returns:
            User: User object
        """
        return self.db_session.query(User).filter_by(id=user_id).first()
    
    def get_user_by_email(self, email):
        """
        Get a user by email.
        
        Args:
            email (str): User email
            
        Returns:
            User: User object
        """
        return self.db_session.query(User).filter_by(email=email).first()

# Flask-Login User class    
class UserLogin(UserMixin):
    def __init__(self, user_id, email):
        self.id = user_id
        self.email = email

def setup_login_manager(app, auth_service):
    """
    Setup Flask-Login manager.
    
    Args:
        app: Flask application
        auth_service: Authentication service
        
    Returns:
        LoginManager: Configured login manager
    """
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    @login_manager.user_loader
    def load_user(user_id):
        user = auth_service.get_user_by_id(user_id)
        if not user:
            return None
        return UserLogin(user.id, user.email)
    
    return login_manager
