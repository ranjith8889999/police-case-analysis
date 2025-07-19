from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user

main_controller = Blueprint('main', __name__)

def init_main_controller():
    """Initialize main controller."""
    
    @main_controller.route('/health')
    def health_check():
        """Health check endpoint for deployment platforms."""
        return jsonify({
            'status': 'healthy',
            'message': 'Police Case Analysis System is running'
        }), 200
    
    @main_controller.route('/')
    def index():
        """Home page."""        # Redirect to dashboard if user is logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
            
        return render_template('index.html')
    
    @main_controller.route('/dashboard')
    @login_required
    def dashboard():
        """Dashboard page."""
        return render_template('dashboard.html')
    
    @main_controller.route('/case-section-analysis')
    @login_required
    def case_section_analysis():
        """Case Section Analysis page."""
        return redirect(url_for('chat.chat_page', analysis_type='case-section-analysis'))
    
    @main_controller.route('/bail-analysis')
    @login_required
    def bail_analysis():
        """Bail Analysis page."""
        return redirect(url_for('chat.chat_page', analysis_type='bail-analysis'))
    
    @main_controller.route('/human-analysis')
    @login_required
    def human_analysis():
        """Human Analysis page."""
        return redirect(url_for('chat.chat_page', analysis_type='human-analysis'))
    
    return main_controller
