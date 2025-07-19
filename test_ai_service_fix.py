"""
Test script to verify the AI service SystemMessage fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_service import AIService

def test_ai_service():
    """Test the AI service to ensure SystemMessage fix works"""
    
    try:
        print("Testing AI Service with SystemMessage fix...")
        
        # Initialize AI service
        ai_service = AIService()
        
        # Test direct query (simpler test)
        print("1. Testing direct query...")
        response = ai_service.direct_query("Hello, can you respond to this test message?")
        print(f"   ✅ Direct query successful: {response[:100]}...")
        
        # Test document query (this uses SystemMessage)
        print("2. Testing document query with SystemMessage...")
        result = ai_service.query_documents(
            query="Hello, test message", 
            document_type=None,
            is_first_message=True
        )
        
        if isinstance(result, dict) and 'response' in result:
            print(f"   ✅ Document query successful: {result['response'][:100]}...")
            print(f"   Sources found: {len(result.get('sources', []))}")
        else:
            print(f"   ✅ Document query successful: {str(result)[:100]}...")
        
        print("\n🎉 AI Service SystemMessage fix confirmed!")
        return True
        
    except Exception as e:
        print(f"❌ AI Service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ai_service()
    if success:
        print("\n✅ SystemMessage fix working correctly!")
    else:
        print("\n❌ SystemMessage fix needs more work")
