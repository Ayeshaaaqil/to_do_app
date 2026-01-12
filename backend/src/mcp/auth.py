"""
Authentication Middleware for MCP Tools

This module provides authentication functionality for MCP tools,
ensuring that only authenticated users can access todo operations.
"""
from typing import Optional
import uuid
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

security = HTTPBearer()

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"


def authenticate_user_from_token(token: str) -> Optional[uuid.UUID]:
    """
    Extract user ID from JWT token for MCP tools.
    Decode the JWT and return the user ID.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials for MCP tool"
            )
        return uuid.UUID(user_id)
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials for MCP tool"
        )


def validate_user_access(user_id: uuid.UUID, required_user_id: uuid.UUID) -> bool:
    """
    Validate that the authenticated user has access to the requested resource.
    """
    return user_id == required_user_id


# Example usage in an MCP tool:
# 
# async def some_mcp_tool(user_token: str, todo_user_id: uuid.UUID):
#     authenticated_user_id = authenticate_user_from_token(user_token)
#     if not validate_user_access(authenticated_user_id, todo_user_id):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Access denied: Insufficient permissions"
#         )
#     # Proceed with the tool operation