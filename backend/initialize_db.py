"""
Database Initialization Script

This script initializes the database tables for the Todo application.
Run this script to ensure all required tables are created.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import engine
from src.models.user import User
from src.models.todo import Todo
from src.models.conversation import Conversation, ConversationMessage
from sqlmodel import SQLModel

def initialize_database():
    """Initialize the database with all required tables."""
    print("Initializing database...")

    try:
        # Create all tables
        SQLModel.metadata.create_all(bind=engine)
        print("[SUCCESS] Database tables created successfully!")

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"Tables in database: {tables}")

        required_tables = ['user', 'todo', 'conversations', 'conversation_messages']
        missing_tables = []

        for table in required_tables:
            if table not in tables:
                missing_tables.append(table)

        if missing_tables:
            print(f"[WARNING] Missing tables: {missing_tables}")
        else:
            print("[SUCCESS] All required tables are present!")

        return True

    except Exception as e:
        print(f"[ERROR] Error initializing database: {str(e)}")
        return False

if __name__ == "__main__":
    success = initialize_database()
    if success:
        print("\nDatabase initialization completed successfully!")
    else:
        print("\nDatabase initialization failed!")
        sys.exit(1)