from fastapi import APIRouter, Depends, Request, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database.database import get_session
from ..models.user import UserCreate, UserRead
from ..schemas.user import UserLogin, UserToken
from ..services.auth_service import AuthService
from ..auth.jwt import get_current_active_user, create_access_token
from ..database.config import settings

# SlowAPI limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/auth/register", response_model=UserToken)
async def register_user(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_session)
):
    """
    Register a new user and return JWT token
    """
    user_read = AuthService.register_user(db, user_data)
    if not user_read:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")

    # Create JWT token
    access_token = create_access_token(
        data={"sub": user_read.email},
        expires_delta=timedelta(minutes=30)
    )

    return UserToken(
        access_token=access_token,
        token_type="bearer",
        user=user_read
    )




@router.post("/auth/login", response_model=UserToken)
@limiter.limit("10/minute")
async def login_user(
    request: Request,
    user_login: UserLogin,
    db: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token
    """
    token = AuthService.login_user(db, user_login)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return token


@router.get("/auth/profile", response_model=UserRead)
async def get_user_profile(
    current_user: UserRead = Depends(get_current_active_user)
):
    """
    Get authenticated user profile
    """
    return current_user


@router.post("/auth/refresh", response_model=UserToken)
@limiter.limit("30/minute")
async def refresh_token(
    request: Request,
    current_user: UserRead = Depends(get_current_active_user)
):
    """
    Refresh JWT token
    """
    access_token_expires = timedelta(minutes=settings.jwt_expiration_minutes)

    access_token = create_access_token(
        data={"sub": current_user.email},
        expires_delta=access_token_expires
    )

    return UserToken(
        access_token=access_token,
        token_type="bearer",
        user=current_user
    )
