"""
Test script to verify the SQL syntax fix for document search
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.database import init_db
from app.services.gemini_document_service import GeminiDocumentService

def test_search_functionality():
    """Test the document search to ensure SQL syntax is fixed"""
    
    # Create database session
    Session = init_db()
    session = Session()
    
    try:
        # Initialize the document service
        doc_service = GeminiDocumentService(session)
        
        print("Testing document search functionality...")
        
        # Test basic search fallback (this should work even without embeddings)
        print("1. Testing basic search fallback...")
        results = doc_service.basic_search_fallback("test query", limit=3)
        print(f"   Basic search returned {len(results)} results")
        
        # Test semantic search (this will test the vector SQL syntax)
        print("2. Testing semantic search...")
        try:
            results = doc_service.semantic_search_chunks("police case", limit=3)
            print(f"   Semantic search returned {len(results)} results")
            print("   ✅ SQL syntax fix successful!")
        except Exception as e:
            print(f"   ❌ Semantic search failed: {e}")
            return False
        
        print("3. Testing text search fallback...")
        results = doc_service.text_search_fallback("document", limit=3)
        print(f"   Text search returned {len(results)} results")
        
        print("\n✅ All search methods working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    success = test_search_functionality()
    if success:
        print("\n🎉 SQL syntax fix confirmed - all tests passed!")
    else:
        print("\n⚠️  Some tests failed - check the errors above")
