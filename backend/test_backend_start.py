"""
Simple test to verify backend can start without errors
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test importing the essential modules
    from src.database.database import engine, get_session
    from sqlmodel import SQLModel, select
    from src.models.user import User
    from src.models.todo import Todo
    from src.models.conversation import Conversation, ConversationMessage

    print("[SUCCESS] All modules imported successfully")

    # Test creating tables
    SQLModel.metadata.create_all(bind=engine)
    print("[SUCCESS] Database tables created successfully")

    # Test database session
    from sqlalchemy.exc import SQLAlchemyError
    try:
        with next(get_session()) as session:
            # Try a simple query
            result = session.exec(select(User).limit(1))
            print("[SUCCESS] Database session working correctly")
    except SQLAlchemyError as e:
        print(f"[ERROR] Database session error: {e}")
        sys.exit(1)

    print("\nBackend startup test passed!")

except Exception as e:
    print(f"Backend startup test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)