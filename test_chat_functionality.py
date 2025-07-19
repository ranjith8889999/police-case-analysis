#!/usr/bin/env python3

"""
Test script to simulate chat functionality and verify AI service integration
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.models.database import init_db
from app.services.document_service import DocumentService
from app.services.ai_service import AIService
from app.services.chat_service import ChatService

def test_chat_functionality():
    """Test if the full chat functionality works without errors"""
    print("Testing chat functionality...")
    
    try:
        # Initialize database
        db_session = init_db()()
        
        # Initialize services
        document_service = DocumentService(db_session)
        ai_service = AIService(document_service)
        chat_service = ChatService(db_session, ai_service)
        
        print("✓ All services initialized successfully")
        
        # Test document search through AI service
        test_query = "What are the provisions for police case analysis?"
        print(f"Testing AI query: '{test_query}'")
        
        response = ai_service.query_documents(
            query=test_query,
            document_type=None,
            chat_history=[]
        )
        
        print(f"✓ AI query completed successfully")
        print(f"  Response length: {len(response)} characters")
        print(f"  Response preview: {response[:200]}...")
        
        # Test creating a chat session
        print("\nTesting chat session creation...")
        user_id = 1  # Assuming user ID 1 exists
        session = chat_service.create_session(user_id, "Case Section Analysis")
        
        print(f"✓ Chat session created with ID: {session.id}")
        
        # Test processing a message
        print("\nTesting message processing...")
        chat_response = chat_service.process_user_message(
            session.id, 
            "What are the key legal provisions for police investigations?"
        )
        
        print(f"✓ Message processed successfully")
        print(f"  Response preview: {chat_response[:200]}...")
        
        # Test retrieving messages
        messages = chat_service.get_session_messages(session.id)
        print(f"✓ Retrieved {len(messages)} messages from session")
        
        print("\n✓ All chat functionality tests passed!")
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    return True

if __name__ == "__main__":
    success = test_chat_functionality()
    sys.exit(0 if success else 1)
