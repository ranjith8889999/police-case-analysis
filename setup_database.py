#!/usr/bin/env python3
"""
Database setup script to recreate tables with correct schema and add default users
"""
import os
import sys
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.models.database import Base, User

def recreate_database():
    """Recreate the database with correct schema"""
    try:
        # Connection string for SQL Server LocalDB
        conn_str = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;DATABASE=CrimeAnalysis;Trusted_Connection=yes;'
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
        
        print("Dropping existing tables...")
        # Drop all tables
        Base.metadata.drop_all(engine)
        
        print("Creating tables with updated schema...")
        # Create all tables with new schema
        Base.metadata.create_all(engine)
        
        print("Database schema recreated successfully!")
        return engine
        
    except Exception as e:
        print(f"Error recreating database schema: {e}")
        raise

def add_default_users(engine):
    """Add default users to the database"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Default users with authorized email addresses
        default_users = [
            {
                'email': 'kuncharapuranjith@gmail.com',
                'password': 'admin123'
            },
            {
                'email': 'ranjith888999@gmail.com', 
                'password': 'admin123'
            }
        ]
        
        for user_data in default_users:
            # Check if user already exists
            existing_user = session.query(User).filter_by(email=user_data['email']).first()
            if not existing_user:
                hashed_password = generate_password_hash(user_data['password'])
                new_user = User(
                    email=user_data['email'],
                    password=hashed_password
                )
                session.add(new_user)
                print(f"Added user: {user_data['email']}")
            else:
                print(f"User already exists: {user_data['email']}")
        
        session.commit()
        session.close()
        print("Default users added successfully!")
        
    except Exception as e:
        print(f"Error adding default users: {e}")
        raise

def main():
    """Main function to setup database"""
    print("Setting up Police Case Management System Database...")
    print("=" * 50)
    
    try:
        # Recreate database schema
        engine = recreate_database()
        
        # Add default users
        add_default_users(engine)
        
        print("\n" + "=" * 50)
        print("Database setup completed successfully!")
        print("\nLogin Credentials:")
        print("Email: kuncharapuranjith@gmail.com")
        print("Password: admin123")
        print("\nEmail: ranjith888999@gmail.com") 
        print("Password: admin123")
        print("\nYou can now run the Flask application and login with these credentials.")
        
    except Exception as e:
        print(f"\nDatabase setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
