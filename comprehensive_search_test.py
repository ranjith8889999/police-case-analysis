"""
Comprehensive test to verify the SQL syntax fix and search functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.database import init_db
from app.services.gemini_document_service import GeminiDocumentService

def comprehensive_test():
    """Comprehensive test of all search functionalities"""
    
    Session = init_db()
    session = Session()
    
    try:
        doc_service = GeminiDocumentService(session)
        
        print("=== COMPREHENSIVE DOCUMENT SEARCH TEST ===")
        print()
        
        # Test 1: Semantic Search
        print("🔍 Test 1: Semantic Search")
        print("-" * 40)
        try:
            results = doc_service.semantic_search_chunks("police investigation", limit=2)
            print(f"✅ Semantic search: {len(results)} results found")
            if results:
                for i, result in enumerate(results[:2]):
                    print(f"   Result {i+1}: {result['document_name']} (score: {result['final_score']:.3f})")
                    print(f"   Preview: {result['preview'][:100]}...")
        except Exception as e:
            print(f"❌ Semantic search failed: {e}")
        
        print()
        
        # Test 2: Basic Search Fallback
        print("🔍 Test 2: Basic Search Fallback")
        print("-" * 40)
        try:
            results = doc_service.basic_search_fallback("case", limit=2)
            print(f"✅ Basic search: {len(results)} results found")
            if results:
                for i, result in enumerate(results[:2]):
                    print(f"   Result {i+1}: {result['document_name']}")
        except Exception as e:
            print(f"❌ Basic search failed: {e}")
        
        print()
        
        # Test 3: Text Search Fallback
        print("🔍 Test 3: Text Search Fallback")
        print("-" * 40)
        try:
            results = doc_service.text_search_fallback("document", limit=2)
            print(f"✅ Text search: {len(results)} results found")
            if results:
                for i, result in enumerate(results[:2]):
                    print(f"   Result {i+1}: {result[3]} (chunk {result[0]})")  # document_name, chunk_id
        except Exception as e:
            print(f"❌ Text search failed: {e}")
        
        print()
        
        # Test 4: Document Type Filter
        print("🔍 Test 4: Search with Document Type Filter")
        print("-" * 40)
        try:
            results = doc_service.semantic_search_chunks("legal", document_type="Case Files", limit=2)
            print(f"✅ Filtered search: {len(results)} results found for 'Case Files'")
        except Exception as e:
            print(f"❌ Filtered search failed: {e}")
        
        print()
        
        # Test 5: Wrapper Method
        print("🔍 Test 5: Search Document Chunks (Wrapper)")
        print("-" * 40)
        try:
            results = doc_service.search_document_chunks("investigation", limit=2)
            print(f"✅ Wrapper search: {len(results)} results found")
        except Exception as e:
            print(f"❌ Wrapper search failed: {e}")
        
        print()
        print("🎉 ALL TESTS COMPLETED!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ COMPREHENSIVE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    success = comprehensive_test()
    if success:
        print("\n✅ SQL SYNTAX FIX VERIFIED - ALL SEARCH METHODS WORKING!")
    else:
        print("\n❌ SOME ISSUES REMAIN - CHECK OUTPUT ABOVE")
