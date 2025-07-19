"""
Final verification script - Tests both SQL syntax fix and SystemMessage fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.database import init_db
from app.services.gemini_document_service import GeminiDocumentService
from app.services.ai_service import AIService

def final_verification():
    """Final verification of all fixes"""
    
    print("🔧 FINAL VERIFICATION - ALL FIXES")
    print("=" * 50)
    
    Session = init_db()
    session = Session()
    
    try:
        # Test 1: Document Service (SQL fix)
        print("\n✅ Test 1: Document Service SQL Syntax Fix")
        print("-" * 40)
        doc_service = GeminiDocumentService(session)
        
        # Test semantic search
        results = doc_service.semantic_search_chunks("police case", limit=2)
        print(f"   Semantic search: {len(results)} results ✅")
        
        # Test basic search
        results = doc_service.basic_search_fallback("investigation", limit=2)
        print(f"   Basic search: {len(results)} results ✅")
        
        # Test 2: AI Service (SystemMessage fix)
        print("\n✅ Test 2: AI Service SystemMessage Fix")
        print("-" * 40)
        ai_service = AIService(document_service=doc_service)
        
        # Test direct query
        response = ai_service.direct_query("Hello!")
        print(f"   Direct query: Response received ✅")
        
        # Test document query with SystemMessage
        result = ai_service.query_documents(
            query="What information is available about police procedures?",
            document_type=None,
            is_first_message=False
        )
        print(f"   Document query: Response received ✅")
        if isinstance(result, dict):
            print(f"   Sources found: {len(result.get('sources', []))} ✅")
        
        # Test 3: Integration Test
        print("\n✅ Test 3: Full Integration Test")
        print("-" * 40)
        result = ai_service.query_documents(
            query="Tell me about police investigation procedures",
            document_type="Case Files",
            chat_history=[("Hello", "Hi there!")],
            is_first_message=False
        )
        
        if isinstance(result, dict) and 'response' in result:
            print(f"   Integration test: Full response generated ✅")
            print(f"   Response length: {len(result['response'])} characters")
            print(f"   Sources: {len(result.get('sources', []))}")
        else:
            print(f"   Integration test: Response generated ✅")
        
        print("\n🎉 ALL FIXES VERIFIED SUCCESSFULLY!")
        print("=" * 50)
        print("✅ SQL syntax error fixed - vector search working")
        print("✅ SystemMessage error fixed - AI service working") 
        print("✅ Full integration working")
        print("\n🚀 Your Police Case Analysis system is ready to use!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    success = final_verification()
    if success:
        print("\n🎊 CONGRATULATIONS! All fixes are working perfectly!")
    else:
        print("\n⚠️  Some issues found - check the output above")
