from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from ..services.auth_service import UserLogin
from ..models.database import User

auth_controller = Blueprint('auth', __name__)

def init_auth_controller(auth_service):
    """
    Initialize authentication controller.
    
    Args:
        auth_service: Authentication service
    """
    
    @auth_controller.route('/login', methods=['GET', 'POST'])
    def login():
        """Handle login requests."""
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
            
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            # List of authorized emails - Add others as needed
            authorized_emails = [
                'kuncharapuranjith@gmail.com',
                'ranjith888999@gmail.com'
            ]
            
            # Check if email is authorized
            if email not in authorized_emails:
                flash('This email is not authorized to access the system.', 'danger')
                return render_template('login.html')
                
            # Authenticate user
            user, message = auth_service.authenticate(email, password)
            
            if user:
                # Create login user object for Flask-Login
                login_user(UserLogin(user.id, user.email))
                flash('Login successful!', 'success')
                
                # Redirect to intended page or dashboard
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.dashboard'))
            else:
                flash(message, 'danger')
        
        return render_template('login.html')
    
    @auth_controller.route('/signup', methods=['GET', 'POST'])
    def signup():
        """Handle signup requests."""
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validate inputs
            if not all([username, email, password, confirm_password]):
                flash('All fields are required.', 'danger')
                return render_template('signup.html')
                
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('signup.html')
                
            # List of authorized emails - Add others as needed
            authorized_emails = [
                'kuncharapuranjith@gmail.com',
                'ranjith888999@gmail.com'
            ]
            
            # Check if email is authorized
            if email not in authorized_emails:
                flash('This email is not authorized to register.', 'danger')
                return render_template('signup.html')
              # Register user
            user, message = auth_service.register_user(username, email, password)
            
            if user:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash(message, 'danger')
        
        return render_template('signup.html')
    
    @auth_controller.route('/logout')
    @login_required
    def logout():
        """Handle logout requests."""
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('auth.login'))
    
    return auth_controller
