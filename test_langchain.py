"""
Test LangChain integration with Gemini - Simple and Clean!
"""

import sys
sys.path.append('.')

from app.services.gemini_document_service import GeminiDocumentService
from app.services.ai_service import AIService
from app.models.database import init_db

def test_langchain_integration():
    """Test the simplified LangChain integration."""
    print("🔍 Testing LangChain + Gemini Integration...")
    
    try:
        # Initialize database
        Session = init_db()
        session = Session()
        
        # Test document service with LangChain
        print("\n1. Testing LangChain Document Service...")
        doc_service = GeminiDocumentService(session)
        
        test_text = "This is a test document about police case analysis using LangChain."
        embedding = doc_service.generate_embedding(test_text)
        
        print(f"✅ LangChain embeddings working!")
        print(f"   - Dimensions: {len(embedding)}")
        print(f"   - Normalized: {abs(sum(x*x for x in embedding)**0.5 - 1.0) < 0.001}")
        
        # Test AI service with LangChain
        print("\n2. Testing LangChain AI Service...")
        ai_service = AIService(doc_service)
        
        response = ai_service.direct_query("What is police case analysis? Answer in one sentence.")
        print(f"✅ LangChain AI working!")
        print(f"   - Response: {response[:100]}...")
        
        session.close()
        print("\n🎉 LangChain integration successful! Much cleaner and easier to understand!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_langchain_integration()
