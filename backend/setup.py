from setuptools import setup, find_packages

setup(
    name="todo-api-backend",
    version="1.0.0",
    description="Backend API for Todo application with AI assistant",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "sqlmodel==0.0.16",
        "pydantic==2.5.0",
        "uvicorn==0.24.0",
        "psycopg2-binary==2.9.9",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "asyncpg==0.29.0",
        "passlib==1.7.4",
        "bcrypt==4.0.1",
        "pyjwt==2.8.0",
        "openai==1.12.0",
        "gradio==4.12.0",
        "pyngrok==4.1.1",
        "requests==2.31.0",
        "torch==2.1.2",
        "transformers==4.36.0",
        "accelerate==0.25.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ]
    },
    entry_points={
        "console_scripts": [
            "todo-api=app:main",
        ],
    },
)