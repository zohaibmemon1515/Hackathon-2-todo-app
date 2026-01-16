"""
Authentication middleware and utilities for AI Chatbot feature
"""
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta


# Initialize security scheme
security = HTTPBearer()


def verify_token(token: str) -> Optional[dict]:
    """
    Verify the JWT token and return the payload if valid.
    """
    try:
        secret_key = os.getenv("JWT_SECRET", "your-default-secret-key")
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Get current user from the token in the request.
    """
    token = credentials.credentials
    user_payload = verify_token(token)

    if not user_payload:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_payload


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a new access token with the provided data.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)  # Default 30 minutes

    to_encode.update({"exp": expire})

    secret_key = os.getenv("JWT_SECRET", "your-default-secret-key")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def require_user_access(user_id_from_token: str, requested_user_id: str) -> bool:
    """
    Check if the user has access to the requested resource.
    For the chatbot feature, users can only access their own conversations and tasks.
    """
    return user_id_from_token == requested_user_id


def require_same_user_or_admin(current_user: dict, target_user_id: str) -> bool:
    """
    Check if current user is the same as target user or is an admin.
    """
    user_id_from_token = current_user.get("user_id") or current_user.get("sub")

    # Check if it's the same user
    if user_id_from_token == target_user_id:
        return True

    # Check if user is admin (if applicable)
    is_admin = current_user.get("role") == "admin"
    return is_admin