"""
Database utilities for handling connection issues and retries.
"""

import time
import functools
from sqlalchemy.exc import OperationalError, DisconnectionError
from sqlalchemy.orm.exc import StaleDataError

def retry_db_operation(max_retries=3, delay=1, backoff=2):
    """
    Decorator to retry database operations on connection failures.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        delay (float): Initial delay between retries in seconds
        backoff (float): Multiplier for delay after each retry
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            current_delay = delay
            
            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                except (OperationalError, DisconnectionError, StaleDataError) as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        print(f"Database operation failed after {max_retries} attempts: {e}")
                        raise
                    
                    print(f"Database connection error (attempt {retry_count}/{max_retries}): {e}")
                    print(f"Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_delay *= backoff
                    
                    # Try to rollback the session if it exists
                    if hasattr(args[0], 'db_session') and args[0].db_session:
                        try:
                            args[0].db_session.rollback()
                        except:
                            pass
                            
                except Exception as e:
                    # For non-connection errors, raise immediately
                    raise
                    
            return None
        return wrapper
    return decorator

class DatabaseManager:
    """
    Database manager to handle connection issues and session management.
    """
    
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session = None
    
    @property
    def session(self):
        """Get or create a database session."""
        if self._session is None or not self._session.is_active:
            self._session = self.session_factory()
        return self._session
    
    def refresh_session(self):
        """Refresh the database session."""
        if self._session:
            try:
                self._session.close()
            except:
                pass
        self._session = self.session_factory()
        return self._session
    
    def close_session(self):
        """Close the database session."""
        if self._session:
            try:
                self._session.close()
            except:
                pass
            self._session = None
    
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def execute_with_retry(self, operation, *args, **kwargs):
        """
        Execute a database operation with retry logic.
        
        Args:
            operation: Function to execute
            *args: Arguments to pass to the operation
            **kwargs: Keyword arguments to pass to the operation
        """
        try:
            return operation(self.session, *args, **kwargs)
        except (OperationalError, DisconnectionError, StaleDataError):
            # Refresh session on connection error
            self.refresh_session()
            raise
