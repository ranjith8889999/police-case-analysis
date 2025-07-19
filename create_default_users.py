#!/usr/bin/env python3
"""
Script to create default users for the Police Case Management System.
Run this script to create default user accounts.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.models.database import init_db, User
from werkzeug.security import generate_password_hash

def create_default_users():
    """Create default users for the system."""
    
    # Initialize database
    Session = init_db()
    session = Session()
    
    # Default users with their credentials
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
    
    try:
        for user_data in default_users:
            # Check if user already exists
            existing_user = session.query(User).filter_by(email=user_data['email']).first()
            
            if not existing_user:
                # Create new user
                hashed_password = generate_password_hash(user_data['password'])
                new_user = User(
                    email=user_data['email'],
                    password=hashed_password
                )
                
                session.add(new_user)
                print(f"Created user: {user_data['email']}")
            else:
                print(f"User already exists: {user_data['email']}")
        
        session.commit()
        print("\nDefault users created successfully!")
        print("\nLogin Credentials:")
        print("==================")
        for user_data in default_users:
            print(f"Email: {user_data['email']}")
            print(f"Password: {user_data['password']}")
            print("-" * 40)
        
    except Exception as e:
        session.rollback()
        print(f"Error creating users: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    create_default_users()
