from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

chat_controller = Blueprint('chat', __name__)

def init_chat_controller(chat_service):
    """
    Initialize chat controller.
    
    Args:
        chat_service: Chat service
    """
    
    @chat_controller.route('/chat/<analysis_type>')
    @login_required
    def chat_page(analysis_type):
        """Chat page for different analysis types."""
        # Validate analysis type
        valid_types = ['case-section-analysis', 'bail-analysis', 'human-analysis']
        if analysis_type not in valid_types:
            flash('Invalid analysis type', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Convert URL format to database format
        analysis_mapping = {
            'case-section-analysis': 'Case Section Analysis',
            'bail-analysis': 'Bail Analysis',
            'human-analysis': 'Human Analysis'
        }
        
        # Always create a new session for fresh conversation
        analysis_session = chat_service.create_session(current_user.id, analysis_mapping[analysis_type])
        print(f"DEBUG: Created new session with UUID: {analysis_session.id}")
        
        # Get messages for this session (should be empty for new session)
        messages = chat_service.get_session_messages(analysis_session.id)
        
        print(f"DEBUG: Rendering template with session UUID: {analysis_session.id}, analysis_type: {analysis_type}")
        
        return render_template(
            'chat.html',
            session=analysis_session,
            messages=messages,
            analysis_type=analysis_type,
            session_type=analysis_mapping[analysis_type]
        )
    
    @chat_controller.route('/chat/send', methods=['POST'])
    @login_required
    def send_message():
        """Send a message in a chat session."""
        data = request.json
        session_id = data.get('session_id')
        message = data.get('message')
        
        if not all([session_id, message]):
            return jsonify({'error': 'Missing parameters'}), 400
        
        print(f"DEBUG: Received session_id: {session_id} (type: {type(session_id)})")
        print(f"DEBUG: Received message: {message}")
        print(f"DEBUG: Request data: {data}")
        
        # Check if session_id is a string that looks like an analysis type (shouldn't happen anymore)
        if isinstance(session_id, str) and session_id in ['case-section-analysis', 'bail-analysis', 'human-analysis']:
            print(f"ERROR: Still receiving analysis type '{session_id}' instead of session UUID!")
            return jsonify({'error': f'Invalid session ID: received analysis type "{session_id}" instead of UUID'}), 400
        
        # Convert session_id to string (UUID format)
        session_id = str(session_id)
        print(f"DEBUG: Using session_id as UUID: {session_id}")
        
        # Get the session to understand the context
        session = chat_service.get_session(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Get existing messages to check if this is the first message
        existing_messages = chat_service.get_session_messages(session_id)
        is_first_message = len(existing_messages) == 0
        
        # Determine document type based on session type
        document_type_mapping = {
            'Case Section Analysis': 'Case Section Analysis',
            'Bail Analysis': 'Bail Analysis', 
            'Human Analysis': 'Human Analysis'
        }
        document_type = document_type_mapping.get(session.session_type, None)
        
        print(f"DEBUG: Session type: {session.session_type}, Document type: {document_type}")
        print(f"DEBUG: Is first message: {is_first_message}")
        
        # Process message and get response with sources
        try:
            response_data = chat_service.process_user_message(session_id, message, document_type, is_first_message)
            
            # Handle both old string responses and new dict responses
            if isinstance(response_data, dict):
                response_text = response_data.get('response', response_data)
                sources = response_data.get('sources', [])
            else:
                response_text = response_data
                sources = []
            
            # Get the latest message timestamp
            updated_messages = chat_service.get_session_messages(session_id)
            latest_message = updated_messages[-1] if updated_messages else None
            
            return jsonify({
                'success': True,
                'response': response_text,
                'sources': sources,
                'timestamp': latest_message.timestamp.strftime('%H:%M') if latest_message else None
            })
            
        except Exception as e:
            print(f"ERROR: Failed to process message: {e}")
            return jsonify({'error': 'Failed to process message'}), 500
    
    @chat_controller.route('/chat/history/<session_id>')
    @login_required
    def get_chat_history(session_id):
        """Get chat history for a session."""
        # Get messages for this session (session_id is already a string UUID)
        messages = chat_service.get_session_messages(session_id)
        
        # Format messages for JSON response
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                'id': msg.id,
                'content': msg.message_text,
                'is_user': msg.sender == 'user',
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify(formatted_messages)
    
    @chat_controller.route('/chat/new/<analysis_type>')
    @login_required
    def new_chat_session(analysis_type):
        """Create a new chat session."""
        # Validate analysis type
        valid_types = ['case-section-analysis', 'bail-analysis', 'human-analysis']
        if analysis_type not in valid_types:
            flash('Invalid analysis type', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Convert URL format to database format
        analysis_mapping = {
            'case-section-analysis': 'Case Section Analysis',
            'bail-analysis': 'Bail Analysis',
            'human-analysis': 'Human Analysis'
        }
        
        session_type = analysis_mapping[analysis_type]
        
        # Create new session with analysis type
        session = chat_service.create_session(current_user.id, session_type)
        print(f"DEBUG: Created new session with UUID: {session.id} for {session_type}")
        
        return redirect(url_for('chat.chat_page', analysis_type=analysis_type))
    
    @chat_controller.route('/chat/sources/<session_id>')
    @login_required
    def get_sources(session_id):
        """Get sources from the last AI response."""
        try:
            sources = chat_service.ai_service.get_last_sources()
            return jsonify({'sources': sources})
        except Exception as e:
            print(f"Error getting sources: {e}")
            return jsonify({'sources': []})
    
    @chat_controller.route('/chat/highlight/<int:chunk_id>')
    @login_required
    def get_chunk_highlight(chunk_id):
        """Get highlighted chunk context for source viewing."""
        try:
            chunk_info = chat_service.ai_service.get_chunk_context(chunk_id)
            if chunk_info:
                return jsonify(chunk_info)
            else:
                return jsonify({'error': 'Chunk not found'}), 404
        except Exception as e:
            print(f"Error getting chunk highlight: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @chat_controller.route('/chat/document/<int:document_id>')
    @login_required
    def view_document(document_id):
        """View full document with highlighting capability."""
        try:
            # Get document chunks for highlighting
            from app.models.database import Document, Chunk
            document = chat_service.db_session.query(Document).filter(Document.id == document_id).first()
            
            if not document:
                flash('Document not found', 'error')
                return redirect(url_for('main.dashboard'))
            
            chunks = chat_service.db_session.query(Chunk).filter(
                Chunk.document_id == document_id
            ).order_by(Chunk.chunk_order).all()
            
            return render_template('document_viewer.html', 
                                 document=document, 
                                 chunks=chunks)
        except Exception as e:
            print(f"Error viewing document: {e}")
            flash('Error loading document', 'error')
            return redirect(url_for('main.dashboard'))
    
    return chat_controller