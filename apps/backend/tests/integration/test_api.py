import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from apps.backend.src.main import app
from apps.backend.src.database.database import engine, get_session
from apps.backend.src.models import user, task  # Import models to register them with SQLModel
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from typing import Generator
from apps.backend.src.auth.jwt import create_access_token
from datetime import timedelta
import uuid


# Create an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a test database session"""
    # Create an in-memory SQLite database for testing
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=test_engine)

    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client(db_session: Session) -> TestClient:
    """Create a test client with dependency overrides"""
    def get_test_session():
        return db_session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client

    # Clean up the override
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session):
    """Create a test user"""
    from apps.backend.src.models.user import User
    from apps.backend.src.auth.utils import get_password_hash

    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "hashed_password": get_password_hash("password123"),
        "is_active": True
    }

    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def auth_token(test_user) -> str:
    """Create an authentication token for the test user"""
    access_token_expires = timedelta(minutes=30)
    token_data = {"sub": test_user.email}
    return create_access_token(data=token_data, expires_delta=access_token_expires)


class TestAuthAPI:
    """Integration tests for authentication API endpoints"""

    def test_register_user_success(self, client: TestClient):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "password123",
                "first_name": "New",
                "last_name": "User"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["first_name"] == "New"
        assert data["user"]["last_name"] == "User"

    def test_register_user_duplicate_email(self, client: TestClient, test_user):
        """Test registration with duplicate email"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": test_user.email,
                "password": "password123",
                "first_name": "New",
                "last_name": "User"
            }
        )

        assert response.status_code == 409
        data = response.json()
        assert data["detail"] == "Email already registered"

    def test_login_user_success(self, client: TestClient, test_user):
        """Test successful user login"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "password123"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user.email

    def test_login_user_invalid_credentials(self, client: TestClient, test_user):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Incorrect email or password"

    def test_get_user_profile(self, client: TestClient, test_user, auth_token):
        """Test getting user profile with valid token"""
        response = client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["email"] == test_user.email
        assert data["first_name"] == test_user.first_name
        assert data["last_name"] == test_user.last_name

    def test_get_user_profile_unauthorized(self, client: TestClient):
        """Test getting user profile without valid token"""
        response = client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": "Bearer invalid-token"}
        )

        assert response.status_code == 401

    def test_refresh_token(self, client: TestClient, test_user, auth_token):
        """Test token refresh functionality"""
        response = client.post(
            "/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user.email
        # Ensure new token is different from old one
        assert data["access_token"] != auth_token


class TestTasksAPI:
    """Integration tests for tasks API endpoints"""

    def test_get_tasks_empty(self, client: TestClient, test_user, auth_token):
        """Test getting tasks for user with no tasks"""
        response = client.get(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "tasks" in data
        assert "total" in data
        assert data["total"] == 0
        assert len(data["tasks"]) == 0

    def test_create_task(self, client: TestClient, test_user, auth_token):
        """Test creating a new task"""
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2023-12-31T23:59:59Z",
            "priority": "medium"
        }

        response = client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["is_completed"] is False
        assert data["priority"] == task_data["priority"]
        assert str(test_user.id) == str(data["user_id"])

    def test_get_tasks_with_created_task(self, client: TestClient, test_user, auth_token):
        """Test getting tasks after creating one"""
        # First create a task
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2023-12-31T23:59:59Z",
            "priority": "medium"
        }

        client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task_data
        )

        # Then get tasks
        response = client.get(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["total"] == 1
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == task_data["title"]

    def test_get_specific_task(self, client: TestClient, test_user, auth_token):
        """Test getting a specific task"""
        # First create a task
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2023-12-31T23:59:59Z",
            "priority": "medium"
        }

        create_response = client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task_data
        )

        assert create_response.status_code == 200
        created_task = create_response.json()
        task_id = created_task["id"]

        # Then get the specific task
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == task_id
        assert data["title"] == task_data["title"]

    def test_get_nonexistent_task(self, client: TestClient, test_user, auth_token):
        """Test getting a non-existent task"""
        fake_task_id = str(uuid.uuid4())

        response = client.get(
            f"/api/v1/tasks/{fake_task_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Task not found"

    def test_update_task(self, client: TestClient, test_user, auth_token):
        """Test updating a task"""
        # First create a task
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2023-12-31T23:59:59Z",
            "priority": "medium"
        }

        create_response = client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task_data
        )

        assert create_response.status_code == 200
        created_task = create_response.json()
        task_id = created_task["id"]

        # Then update the task
        update_data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "is_completed": True,
            "priority": "high"
        }

        response = client.put(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=update_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["is_completed"] == update_data["is_completed"]
        assert data["priority"] == update_data["priority"]

    def test_patch_task(self, client: TestClient, test_user, auth_token):
        """Test partially updating a task"""
        # First create a task
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2023-12-31T23:59:59Z",
            "priority": "medium"
        }

        create_response = client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task_data
        )

        assert create_response.status_code == 200
        created_task = create_response.json()
        task_id = created_task["id"]

        # Then patch the task
        patch_data = {
            "is_completed": True
        }

        response = client.patch(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=patch_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["is_completed"] == patch_data["is_completed"]
        # Other fields should remain unchanged
        assert data["title"] == task_data["title"]

    def test_delete_task(self, client: TestClient, test_user, auth_token):
        """Test deleting a task"""
        # First create a task
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2023-12-31T23:59:59Z",
            "priority": "medium"
        }

        create_response = client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task_data
        )

        assert create_response.status_code == 200
        created_task = create_response.json()
        task_id = created_task["id"]

        # Then delete the task
        response = client.delete(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["message"] == "Task deleted successfully"

        # Verify the task is gone
        get_response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert get_response.status_code == 404

    def test_get_tasks_with_filters(self, client: TestClient, test_user, auth_token):
        """Test getting tasks with completion filter"""
        # Create two tasks: one completed, one not
        task1_data = {
            "title": "Completed Task",
            "description": "Test Description",
            "due_date": "2023-12-31T23:59:59Z",
            "priority": "medium"
        }

        task2_data = {
            "title": "Incomplete Task",
            "description": "Test Description",
            "due_date": "2023-12-31T23:59:59Z",
            "priority": "medium"
        }

        client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task1_data
        )

        create_response = client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task2_data
        )

        # Update one task to be completed
        created_task = create_response.json()
        task_id = created_task["id"]

        client.patch(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"is_completed": True}
        )

        # Get completed tasks only
        response = client.get(
            "/api/v1/tasks?completed=true",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["total"] == 1
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["is_completed"] is True

        # Get incomplete tasks only
        response = client.get(
            "/api/v1/tasks?completed=false",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["total"] == 1
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["is_completed"] is False