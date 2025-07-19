from ..models.database import Conversation, Message
from datetime import datetime
import uuid
from ..utils.database_utils import retry_db_operation

class ChatService:
    def __init__(self, db_session, ai_service):
        """
        Initialize chat service.
        
        Args:
            db_session: SQLAlchemy session for database operations
            ai_service: AI service for answering questions
        """
        self.db_session = db_session
        self.ai_service = ai_service
        
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def create_session(self, user_id, session_type=None):
        """
        Create a new chat session.
        
        Args:
            user_id (int): User ID
            session_type (str): Type of analysis session
            
        Returns:
            Conversation: Created conversation
        """
        session = Conversation(
            user_id=user_id,
            session_type=session_type
        )
        
        self.db_session.add(session)
        self.db_session.commit()
        
        return session
        
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def add_message(self, session_id, message, is_user=True):
        """
        Add a message to a chat session.
        
        Args:
            session_id (str): Chat session UUID
            message (str): Message content
            is_user (bool): Whether the message is from the user (True) or AI (False)
            
        Returns:
            Message: Created message
        """
        chat_message = Message(
            conversation_id=str(session_id),
            sender='user' if is_user else 'assistant',
            message_text=message
        )
        
        self.db_session.add(chat_message)
        self.db_session.commit()
        
        return chat_message
    
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def get_session(self, session_id):
        """
        Get a chat session by ID.
        
        Args:
            session_id (str): Chat session UUID
            
        Returns:
            Conversation: Chat session
        """
        return self.db_session.query(Conversation).filter_by(id=str(session_id)).first()
    
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def get_session_messages(self, session_id):
        """
        Get all messages in a chat session.
        
        Args:
            session_id (str): Chat session UUID
            
        Returns:
            list: List of Message objects
        """
        return self.db_session.query(Message).filter_by(conversation_id=str(session_id)).order_by(Message.timestamp).all()
    
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def get_user_sessions(self, user_id):
        """
        Get all chat sessions for a user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            list: List of Conversation objects
        """
        return self.db_session.query(Conversation).filter_by(user_id=user_id).order_by(Conversation.started_at.desc()).all()
    
    def process_user_message(self, session_id, message, document_type=None, is_first_message=False):
        """
        Process a user message and generate an AI response.
        
        Args:
            session_id (str): Chat session UUID
            message (str): User message
            document_type (str): Type of documents to search
            is_first_message (bool): Whether this is the first message in the conversation
            
        Returns:
            str: AI response
        """
        # Ensure session_id is a string
        session_id = str(session_id)
        
        # Get session
        session = self.get_session(session_id)
        if not session:
            return "Error: Session not found"
        
        # Add user message to history
        self.add_message(session_id, message, is_user=True)
        
        # Get previous messages to build chat history (excluding the current message)
        messages = self.get_session_messages(session_id)
        chat_history = []
        
        # Build chat history from previous messages (excluding the current one)
        for i in range(len(messages) - 1):  # -1 to exclude the current message
            msg = messages[i]
            if msg.sender == 'user':
                # Find the corresponding AI response
                if i + 1 < len(messages) and messages[i + 1].sender == 'assistant':
                    chat_history.append((msg.message_text, messages[i + 1].message_text))
        
        # Prepare context message for first interaction
        context_message = ""
        if is_first_message:
            context_messages = {
                'Case Section Analysis': "I'm here to help you analyze legal cases and sections. You can ask me about specific legal provisions, case studies, or legal procedures related to police cases.",
                'Bail Analysis': "I'm here to help you with bail-related analysis. You can ask me about bail procedures, bail conditions, or legal provisions related to bail in criminal cases.",
                'Human Analysis': "I'm here to help you with human rights analysis in legal cases. You can ask me about human rights violations, legal protections, or related legal provisions."
            }
            context_message = context_messages.get(session.session_type, "I'm here to help you with legal analysis.")
        
        # Generate AI response
        try:
            response_data = self.ai_service.query_documents(
                query=message,
                document_type=document_type,
                chat_history=chat_history,
                context_message=context_message,
                is_first_message=is_first_message
            )
            
            # Handle both dictionary and string responses
            if isinstance(response_data, dict):
                response_text = response_data.get('response', 'No response generated')
                sources = response_data.get('sources', [])
            else:
                response_text = response_data
                sources = []
                
        except Exception as e:
            print(f"Error generating AI response: {e}")
            response_text = "I apologize, but I'm having trouble processing your request right now. Please try again."
            sources = []

        # Add AI response to history  
        self.add_message(session_id, response_text, is_user=False)
        
        # Return both response and sources
        return {
            'response': response_text,
            'sources': sources
        }
    
    def delete_session(self, session_id):
        """
        Delete a chat session and all its messages.
        
        Args:
            session_id (str): Chat session UUID
            
        Returns:
            bool: Success status
        """
        session_id = str(session_id)
        session = self.get_session(session_id)
        
        if session:
            # Delete associated messages
            self.db_session.query(Message).filter_by(conversation_id=session_id).delete()
            
            # Delete session
            self.db_session.delete(session)
            self.db_session.commit()
            
            return True
        
        return False