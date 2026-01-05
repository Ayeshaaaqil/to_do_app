from sqlmodel import Session, select
from models.user import User, UserCreate
import bcrypt
from typing import Optional
import uuid

def get_password_hash(password: str) -> str:
    # Truncate password to 72 bytes if necessary, as bcrypt has a 72-byte limit
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    # Convert password to bytes and hash it
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert plain password to bytes
    plain_bytes = plain_password.encode('utf-8')
    # Convert stored hash to bytes
    hash_bytes = hashed_password.encode('utf-8')
    # Verify the password
    return bcrypt.checkpw(plain_bytes, hash_bytes)

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(session: Session, user_create: UserCreate) -> User:
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise ValueError("User with this email already exists")

    # Create new user
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user