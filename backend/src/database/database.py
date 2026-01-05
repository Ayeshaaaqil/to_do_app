from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment variables
# Using SQLite for development to avoid connection issues
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE_URL", "sqlite:///./todoapp.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session