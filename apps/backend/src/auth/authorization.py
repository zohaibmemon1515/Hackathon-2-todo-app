from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..models.user import User
from ..database.database import get_session
from ..auth.jwt import get_current_user


def require_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Require an active user for protected endpoints
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    return current_user


def require_user_ownership(
    db: Session = Depends(get_session),
    current_user: User = Depends(require_active_user)
):
    """
    Verify that the current user has permission to access a resource
    This is a general function that can be used to check ownership of resources
    """
    def check_ownership(resource_user_id: str) -> bool:
        # Check if the resource belongs to the current user
        if str(current_user.id) != resource_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource"
            )
        return True

    return check_ownership


def is_admin_user(current_user: User = Depends(get_current_user)) -> bool:
    """
    Check if the current user has admin privileges
    Note: This assumes there's an 'is_admin' field in the User model which may need to be added
    """
    # This is a placeholder implementation
    # In a real application, you'd check a role or permission field
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return True