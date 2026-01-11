"""
Migration script to add conversation models to the database
"""

import sys
import os

# Add the backend/src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from sqlmodel import SQLModel
from src.database.database import engine
from src.models.conversation import Conversation, ConversationMessage
from src.models.user import User  # User model from Phase II
from src.models.todo import Todo  # Todo model from Phase II

def migrate():
    print("Creating tables for conversation models...")

    # Create the tables
    SQLModel.metadata.create_all(engine)

    print("Tables created successfully!")

if __name__ == "__main__":
    migrate()