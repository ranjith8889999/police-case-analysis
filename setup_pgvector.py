"""
Database setup script to ensure pgvector extension is enabled.
Run this once to set up your database properly.
"""

import psycopg2
import urllib.parse

def setup_pgvector():
    """Enable pgvector extension in PostgreSQL database."""
    try:
        # Connection parameters
        username = "postgres"
        password = urllib.parse.quote_plus("123456@rR")
        host = "db.dsrysmorxbcuftrwulpa.supabase.co"
        port = "5432"
        database = "postgres"
        
        connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
        
        # Connect to database
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
        
        cursor = conn.cursor()
        
        # Enable pgvector extension
        print("Enabling pgvector extension...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("✅ pgvector extension enabled successfully!")
        
        # Check if extension is installed
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        result = cursor.fetchone()
        
        if result:
            print(f"✅ pgvector extension is active: {result}")
        else:
            print("❌ pgvector extension not found")
        
        cursor.close()
        conn.close()
        
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    setup_pgvector()
