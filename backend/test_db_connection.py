"""
Test script to verify database connection
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import engine
from sqlalchemy import text

def test_db_connection():
    """Test if the database connection is working."""
    print("Testing database connection...")
    
    try:
        # Try to connect to the database
        with engine.connect() as conn:
            # Execute a simple query
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful!")
            print(f"✓ Query result: {result.fetchone()}")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"✓ Available tables: {tables}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    if success:
        print("\nDatabase connection test passed!")
    else:
        print("\nDatabase connection test failed!")
        sys.exit(1)