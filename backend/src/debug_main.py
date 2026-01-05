import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from api import auth, todos
    from database.database import engine
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    app = FastAPI(title="Todo API", version="0.1.0")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
    )

    # Create database tables
    @app.on_event("startup")
    def on_startup():
        from sqlmodel import SQLModel, Relationship
        # Import all models to register them with SQLModel
        from models.user import User
        from models.todo import Todo

        # Add relationships after both models are defined to avoid circular imports
        User.todos = Relationship(back_populates="user")
        Todo.user = Relationship(back_populates="todos")

        SQLModel.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

    # Include routers
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Todo API"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    if __name__ == "__main__":
        import uvicorn
        logger.info("Starting server...")
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
except Exception as e:
    logger.error(f"Error occurred: {str(e)}")
    logger.exception("Full traceback:")
    sys.exit(1)