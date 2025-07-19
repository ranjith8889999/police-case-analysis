"""
Database utility with retry logic for handling connection issues
"""

import time
import random
from functools import wraps
from sqlalchemy.exc import OperationalError, DisconnectionError
import psycopg2

def retry_db_operation(max_retries=3, backoff_factor=0.3, backoff_max=2):
    """
    Decorator to retry database operations on connection failures
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (OperationalError, DisconnectionError, psycopg2.OperationalError) as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    # Calculate backoff delay
                    delay = min(backoff_max, backoff_factor * (2 ** attempt))
                    delay += random.uniform(0, delay * 0.1)  # Add jitter
                    
                    print(f"Database operation failed (attempt {attempt + 1}/{max_retries}): {e}")
                    print(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    
            return None
        return wrapper
    return decorator

def execute_with_retry(db_session, query, params=None, max_retries=3):
    """
    Execute a database query with retry logic
    """
    for attempt in range(max_retries):
        try:
            if params:
                result = db_session.execute(query, params)
            else:
                result = db_session.execute(query)
            return result
        except (OperationalError, DisconnectionError, psycopg2.OperationalError) as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = min(2, 0.3 * (2 ** attempt))
            print(f"Query failed (attempt {attempt + 1}/{max_retries}): {e}")
            print(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
            
            # Try to rollback and refresh the session
            try:
                db_session.rollback()
            except:
                pass
