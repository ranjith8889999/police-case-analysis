#!/usr/bin/env python3

"""
Database health check script to test connection stability.
"""

import sys
import os
import time
sys.path.insert(0, os.path.abspath('.'))

from app.models.database import init_db
from app.services.auth_service import AuthService
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

def test_database_connection():
    """Test database connection and retry logic."""
    print("Testing database connection stability...")
    
    try:
        # Initialize database
        session_factory = init_db()
        
        # Test multiple operations
        for i in range(5):
            print(f"\n--- Test {i+1} ---")
            session = session_factory()
            
            try:
                # Test basic query
                result = session.execute(text("SELECT 1 as test"))
                print(f"✓ Basic query successful: {result.fetchone()}")
                
                # Test user query (the one that was failing)
                result = session.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.fetchone()[0]
                print(f"✓ User count query successful: {user_count} users")
                
                # Test auth service
                auth_service = AuthService(session)
                user = auth_service.get_user_by_email('test@example.com')
                print(f"✓ Auth service query successful: {user}")
                
                session.close()
                
            except OperationalError as e:
                print(f"✗ Database connection error: {e}")
                session.close()
                return False
            except Exception as e:
                print(f"✗ Other error: {e}")
                session.close()
                return False
            
            # Wait between tests
            if i < 4:
                time.sleep(2)
        
        print("\n✓ All database connection tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during database testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
