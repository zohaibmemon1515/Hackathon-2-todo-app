import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from src.models.user import User, UserCreate
from src.schemas.user import UserLogin, UserToken
from src.services.auth_service import AuthService


class TestAuthService:
    """Unit tests for AuthService methods"""

    def test_verify_password_success(self):
        """Test password verification with correct password"""
        with patch('src.auth.utils.verify_password') as mock_verify:
            mock_verify.return_value = True

            result = AuthService.verify_password("plain_password", "hashed_password")

            assert result is True
            mock_verify.assert_called_once_with("plain_password", "hashed_password")

    def test_verify_password_failure(self):
        """Test password verification with incorrect password"""
        with patch('src.auth.utils.verify_password') as mock_verify:
            mock_verify.return_value = False

            result = AuthService.verify_password("plain_password", "hashed_password")

            assert result is False
            mock_verify.assert_called_once_with("plain_password", "hashed_password")

    def test_get_password_hash(self):
        """Test password hashing"""
        with patch('src.auth.utils.get_password_hash') as mock_hash:
            mock_hash.return_value = "hashed_password"

            result = AuthService.get_password_hash("plain_password")

            assert result == "hashed_password"
            mock_hash.assert_called_once_with("plain_password")

    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_user = Mock(spec=User)
        mock_user.hashed_password = "hashed_password"
        mock_user.email = "test@example.com"

        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        with patch.object(AuthService, 'verify_password', return_value=True):
            with patch('src.utils.logging.get_security_logger') as mock_logger:
                mock_security_logger = Mock()
                mock_logger.return_value = mock_security_logger

                result = AuthService.authenticate_user(mock_db, "test@example.com", "password")

                assert result == mock_user
                mock_security_logger.log_auth_attempt.assert_called_once_with("test@example.com", success=True)

    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_user = Mock(spec=User)
        mock_user.hashed_password = "hashed_password"
        mock_user.email = "test@example.com"

        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        with patch.object(AuthService, 'verify_password', return_value=False):
            with patch('src.utils.logging.get_security_logger') as mock_logger:
                mock_security_logger = Mock()
                mock_logger.return_value = mock_security_logger

                result = AuthService.authenticate_user(mock_db, "test@example.com", "wrong_password")

                assert result is None
                mock_security_logger.log_auth_attempt.assert_called_once_with("test@example.com", success=False)

    def test_authenticate_user_not_found(self):
        """Test authentication with non-existent user"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with patch('src.utils.logging.get_security_logger') as mock_logger:
            mock_security_logger = Mock()
            mock_logger.return_value = mock_security_logger

            result = AuthService.authenticate_user(mock_db, "nonexistent@example.com", "password")

            assert result is None
            mock_security_logger.log_auth_attempt.assert_called_once_with("nonexistent@example.com", success=False)

    def test_authenticate_user_exception(self):
        """Test authentication when database query fails"""
        # Mock database session to raise exception
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.side_effect = Exception("DB Error")

        with patch('src.utils.logging.get_security_logger') as mock_logger:
            mock_security_logger = Mock()
            mock_logger.return_value = mock_security_logger

            result = AuthService.authenticate_user(mock_db, "test@example.com", "password")

            assert result is None
            mock_security_logger.log_auth_attempt.assert_called_once_with("test@example.com", success=False)

    def test_register_user_success(self):
        """Test successful user registration"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None  # No existing user

        # Create user data
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        # Mock the hashed password
        with patch.object(AuthService, 'get_password_hash', return_value="hashed_password123"):
            with patch('src.utils.logging.get_security_logger') as mock_logger:
                mock_security_logger = Mock()
                mock_logger.return_value = mock_security_logger

                # Mock the user object that will be returned
                mock_user = Mock(spec=User)
                mock_user.id = "user-id-123"
                mock_user.email = "test@example.com"
                mock_user.first_name = "Test"
                mock_user.last_name = "User"
                mock_user.hashed_password = "hashed_password123"

                # Mock the User model creation
                with patch('src.models.user.User') as mock_user_class:
                    mock_user_instance = Mock()
                    mock_user_class.return_value = mock_user_instance
                    mock_user_instance.email = "test@example.com"
                    mock_user_instance.first_name = "Test"
                    mock_user_instance.last_name = "User"
                    mock_user_instance.hashed_password = "hashed_password123"

                    # Mock the refresh to update the mock_user_instance with an id
                    def mock_refresh(obj):
                        obj.id = "user-id-123"
                        obj.is_active = True
                        obj.created_at = "2023-01-01T00:00:00Z"
                        obj.updated_at = "2023-01-01T00:00:00Z"

                    mock_db.refresh.side_effect = mock_refresh

                    # Call the method
                    result = AuthService.register_user(mock_db, user_data)

                    # Verify the calls
                    mock_db.add.assert_called_once_with(mock_user_instance)
                    mock_db.commit.assert_called_once()
                    mock_security_logger.log_sensitive_operation.assert_called_once_with(
                        "USER_REGISTRATION",
                        "user-id-123",
                        {"email": "test@example.com"}
                    )

    def test_register_user_already_exists(self):
        """Test registration with already existing email"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_existing_user = Mock(spec=User)
        mock_existing_user.email = "existing@example.com"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_user

        user_data = UserCreate(
            email="existing@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        with pytest.raises(HTTPException) as exc_info:
            AuthService.register_user(mock_db, user_data)

        assert exc_info.value.status_code == status.HTTP_409_CONFLICT
        assert exc_info.value.detail == "Email already registered"

    def test_register_user_integrity_error(self):
        """Test registration when database integrity error occurs"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None  # No existing user

        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        with patch.object(AuthService, 'get_password_hash', return_value="hashed_password123"):
            with patch('src.models.user.User') as mock_user_class:
                mock_user_instance = Mock()
                mock_user_class.return_value = mock_user_instance

                # Make the commit raise an IntegrityError
                mock_db.commit.side_effect = IntegrityError("statement", "params", Mock())

                with pytest.raises(HTTPException) as exc_info:
                    AuthService.register_user(mock_db, user_data)

                assert exc_info.value.status_code == status.HTTP_409_CONFLICT
                assert exc_info.value.detail == "Email already registered"
                mock_db.rollback.assert_called_once()

    def test_register_user_general_exception(self):
        """Test registration when general exception occurs"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None  # No existing user

        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        # Make the query raise an exception
        mock_db.query.return_value.filter.return_value.first.side_effect = Exception("DB Error")

        with pytest.raises(HTTPException) as exc_info:
            AuthService.register_user(mock_db, user_data)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.detail == "Internal server error during registration"

    def test_login_user_success(self):
        """Test successful user login"""
        # Mock database session
        mock_db = Mock(spec=Session)

        # Mock user
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.id = "user-id-123"
        mock_user.is_active = True

        # Mock user login data
        user_login = UserLogin(email="test@example.com", password="password123")

        with patch.object(AuthService, 'authenticate_user', return_value=mock_user):
            with patch('src.auth.jwt.create_access_token', return_value="mocked-jwt-token"):
                with patch('src.utils.logging.get_security_logger') as mock_logger:
                    mock_security_logger = Mock()
                    mock_logger.return_value = mock_security_logger

                    result = AuthService.login_user(mock_db, user_login)

                    assert isinstance(result, UserToken)
                    assert result.access_token == "mocked-jwt-token"
                    assert result.token_type == "bearer"
                    assert result.user.email == "test@example.com"

                    mock_security_logger.log_sensitive_operation.assert_called_once_with(
                        "USER_LOGIN",
                        "user-id-123",
                        {"email": "test@example.com"}
                    )

    def test_login_user_authentication_failure(self):
        """Test login with authentication failure"""
        # Mock database session
        mock_db = Mock(spec=Session)

        # Mock user login data
        user_login = UserLogin(email="test@example.com", password="wrong_password")

        with patch.object(AuthService, 'authenticate_user', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                AuthService.login_user(mock_db, user_login)

            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Incorrect email or password"

    def test_login_user_inactive(self):
        """Test login with inactive user"""
        # Mock database session
        mock_db = Mock(spec=Session)

        # Mock inactive user
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.is_active = False

        # Mock user login data
        user_login = UserLogin(email="test@example.com", password="password123")

        with patch.object(AuthService, 'authenticate_user', return_value=mock_user):
            with pytest.raises(HTTPException) as exc_info:
                AuthService.login_user(mock_db, user_login)

            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Inactive user"

    def test_login_user_general_exception(self):
        """Test login when general exception occurs"""
        # Mock database session
        mock_db = Mock(spec=Session)

        # Mock user login data
        user_login = UserLogin(email="test@example.com", password="password123")

        # Make authenticate_user raise an exception
        with patch.object(AuthService, 'authenticate_user', side_effect=Exception("Auth Error")):
            with pytest.raises(HTTPException) as exc_info:
                AuthService.login_user(mock_db, user_login)

            assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert exc_info.value.detail == "Internal server error during login"

    def test_get_user_by_email_success(self):
        """Test getting user by email successfully"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        result = AuthService.get_user_by_email(mock_db, "test@example.com")

        assert result == mock_user

    def test_get_user_by_email_not_found(self):
        """Test getting user by email when not found"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = AuthService.get_user_by_email(mock_db, "nonexistent@example.com")

        assert result is None

    def test_get_user_by_email_exception(self):
        """Test getting user by email when exception occurs"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.side_effect = Exception("DB Error")

        result = AuthService.get_user_by_email(mock_db, "test@example.com")

        assert result is None