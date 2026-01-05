from sqlmodel import select
from src.database.database import get_session
from src.models.user import User

def test_db():
    try:
        with next(get_session()) as session:
            # Try to count users
            statement = select(User)
            users = session.exec(statement).all()
            print(f'Number of users: {len(users)}')
            print('Database connection is working')
            return True
    except Exception as e:
        print(f'Database connection error: {e}')
        return False

if __name__ == "__main__":
    test_db()