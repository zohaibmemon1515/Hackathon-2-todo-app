from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models.user import User, UserCreate
from ..schemas.user import UserRead, UserLogin, UserToken
from ..auth.jwt import create_access_token
from datetime import timedelta
from ..utils.logging import get_security_logger
import logging
import hashlib
import os

# Salt length in bytes
SALT_LENGTH = 16

class AuthService:
    logger = logging.getLogger(__name__)
    security_logger = get_security_logger()

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256 + random salt.
        Returns a hex string combining salt + hash.
        """
        salt = os.urandom(SALT_LENGTH)
        hashed = hashlib.sha256(salt + password.encode("utf-8")).hexdigest()
        return salt.hex() + hashed  # store salt+hash together

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a SHA-256 + salt hash.
        """
        try:
            salt_hex = hashed_password[:SALT_LENGTH*2]  # first 16 bytes as hex
            salt = bytes.fromhex(salt_hex)
            expected_hash = hashlib.sha256(salt + plain_password.encode("utf-8")).hexdigest()
            return (salt_hex + expected_hash) == hashed_password
        except Exception as e:
            AuthService.logger.error(f"Password verification error: {str(e)}")
            return False

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user or not AuthService.verify_password(password, user.hashed_password):
                AuthService.security_logger.log_auth_attempt(email, success=False)
                return None
            AuthService.security_logger.log_auth_attempt(email, success=True)
            return user
        except Exception as e:
            AuthService.logger.error(f"Error authenticating user {email}: {str(e)}")
            AuthService.security_logger.log_auth_attempt(email, success=False)
            return None

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> UserRead:
        try:
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )

            hashed_password = AuthService.hash_password(user_data.password)
            db_user = User(
                email=user_data.email,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                hashed_password=hashed_password
            )

            try:
                db.add(db_user)
                db.commit()
                db.refresh(db_user)

                AuthService.security_logger.log_sensitive_operation(
                    "USER_REGISTRATION",
                    str(db_user.id),
                    {"email": db_user.email}
                )

                return UserRead.from_orm(db_user) if hasattr(UserRead, 'from_orm') else UserRead.model_validate(db_user)
            except IntegrityError:
                db.rollback()
                AuthService.logger.warning(f"User registration failed due to duplicate email: {user_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )
        except HTTPException:
            raise
        except Exception as e:
            AuthService.logger.error(f"Error registering user {user_data.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during registration"
            )

    @staticmethod
    def login_user(db: Session, user_login: UserLogin) -> UserToken:
        try:
            user = AuthService.authenticate_user(db, user_login.email, user_login.password)
            if not user:
                AuthService.logger.warning(f"Failed login attempt for email: {user_login.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not user.is_active:
                AuthService.logger.warning(f"Login attempt for inactive user: {user.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Inactive user",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(
                data={"sub": user.email},
                expires_delta=access_token_expires
            )

            user_read = UserRead.from_orm(user) if hasattr(UserRead, 'from_orm') else UserRead.model_validate(user)

            AuthService.security_logger.log_sensitive_operation(
                "USER_LOGIN",
                str(user.id),
                {"email": user.email}
            )

            return UserToken(
                access_token=access_token,
                token_type="bearer",
                user=user_read
            )
        except HTTPException:
            raise
        except Exception as e:
            AuthService.logger.error(f"Error during login for user {user_login.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during login"
            )

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        try:
            user = db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            AuthService.logger.error(f"Error retrieving user by email {email}: {str(e)}")
            return None
