import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.task import Task as TaskModel, TaskCreate, TaskUpdate, TaskPatch
from src.schemas.task import TaskRead
import uuid
from src.services.task_service import (
    get_user_tasks,
    get_task_by_id,
    create_task,
    update_task,
    patch_task,
    delete_task
)


class TestTaskService:
    """Unit tests for task service functions"""

    def test_get_user_tasks_success(self):
        """Test successful retrieval of user tasks"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.uuid4()
        mock_task.title = "Test Task"
        mock_task.description = "Test Description"
        mock_task.is_completed = False
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.updated_at = "2023-01-01T00:00:00Z"
        mock_task.due_date = "2023-12-31T23:59:59Z"
        mock_task.priority = "medium"
        mock_task.user_id = uuid.uuid4()

        mock_db.query.return_value.filter.return_value.count.return_value = 1
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [mock_task]

        user_id = uuid.uuid4()

        with patch('src.utils.logging.get_security_logger') as mock_logger:
            mock_security_logger = Mock()
            mock_logger.return_value = mock_security_logger

            tasks, total = get_user_tasks(mock_db, user_id, completed=None, limit=50, offset=0)

            assert len(tasks) == 1
            assert total == 1
            mock_security_logger.log_sensitive_operation.assert_called_once_with(
                "GET_USER_TASKS",
                str(user_id),
                {"count": 1, "filter_completed": None}
            )

    def test_get_user_tasks_with_filter(self):
        """Test retrieval of user tasks with completion filter"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.uuid4()
        mock_task.title = "Test Task"
        mock_task.is_completed = True
        mock_task.user_id = uuid.uuid4()

        mock_db.query.return_value.filter.return_value.filter.return_value.count.return_value = 1
        mock_db.query.return_value.filter.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [mock_task]

        user_id = uuid.uuid4()

        with patch('src.utils.logging.get_security_logger') as mock_logger:
            mock_security_logger = Mock()
            mock_logger.return_value = mock_security_logger

            tasks, total = get_user_tasks(mock_db, user_id, completed=True, limit=50, offset=0)

            assert len(tasks) == 1
            assert total == 1
            # Verify that filter was applied twice (user filter + completion filter)
            assert mock_db.query.return_value.filter.call_count >= 2

    def test_get_user_tasks_database_error(self):
        """Test retrieval of user tasks when database error occurs"""
        # Mock database session to raise SQLAlchemyError
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.count.side_effect = SQLAlchemyError("DB Error")

        user_id = uuid.uuid4()

        with pytest.raises(SQLAlchemyError):
            get_user_tasks(mock_db, user_id, completed=None, limit=50, offset=0)

    def test_get_task_by_id_success(self):
        """Test successful retrieval of task by ID"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.uuid4()
        mock_task.title = "Test Task"
        mock_task.description = "Test Description"
        mock_task.is_completed = False
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.updated_at = "2023-01-01T00:00:00Z"
        mock_task.due_date = "2023-12-31T23:59:59Z"
        mock_task.priority = "medium"
        mock_task.user_id = uuid.uuid4()

        mock_db.query.return_value.filter.return_value.first.return_value = mock_task

        user_id = uuid.uuid4()
        task_id = str(mock_task.id)

        with patch('src.utils.logging.get_security_logger') as mock_logger:
            mock_security_logger = Mock()
            mock_logger.return_value = mock_security_logger

            result = get_task_by_id(mock_db, task_id, user_id)

            assert result is not None
            assert result.title == "Test Task"
            mock_security_logger.log_sensitive_operation.assert_called_once_with(
                "GET_TASK_BY_ID",
                str(user_id),
                {"task_id": str(mock_task.id)}
            )

    def test_get_task_by_id_invalid_uuid(self):
        """Test retrieval of task by invalid UUID"""
        mock_db = Mock(spec=Session)

        user_id = uuid.uuid4()
        task_id = "invalid-uuid-format"

        result = get_task_by_id(mock_db, task_id, user_id)

        assert result is None

    def test_get_task_by_id_not_found(self):
        """Test retrieval of non-existent task"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        user_id = uuid.uuid4()
        task_id = str(uuid.uuid4())

        result = get_task_by_id(mock_db, task_id, user_id)

        assert result is None

    def test_get_task_by_id_database_error(self):
        """Test retrieval of task when database error occurs"""
        # Mock database session to raise SQLAlchemyError
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.side_effect = SQLAlchemyError("DB Error")

        user_id = uuid.uuid4()
        task_id = str(uuid.uuid4())

        with pytest.raises(SQLAlchemyError):
            get_task_by_id(mock_db, task_id, user_id)

    def test_create_task_success(self):
        """Test successful task creation"""
        # Mock database session
        mock_db = Mock(spec=Session)

        user_id = uuid.uuid4()
        task_data = TaskCreate(
            title="New Task",
            description="Task Description",
            due_date="2023-12-31T23:59:59Z",
            priority="medium"
        )

        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.uuid4()
        mock_task.title = task_data.title
        mock_task.description = task_data.description
        mock_task.is_completed = False
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.updated_at = "2023-01-01T00:00:00Z"
        mock_task.due_date = task_data.due_date
        mock_task.priority = task_data.priority
        mock_task.user_id = user_id

        # Mock the TaskModel creation
        with patch('src.models.task.Task') as mock_task_class:
            mock_task_instance = Mock()
            mock_task_class.return_value = mock_task_instance
            mock_task_instance.id = uuid.uuid4()
            mock_task_instance.title = task_data.title
            mock_task_instance.description = task_data.description
            mock_task_instance.is_completed = False
            mock_task_instance.created_at = "2023-01-01T00:00:00Z"
            mock_task_instance.updated_at = "2023-01-01T00:00:00Z"
            mock_task_instance.due_date = task_data.due_date
            mock_task_instance.priority = task_data.priority
            mock_task_instance.user_id = user_id

            def mock_refresh(obj):
                obj.id = uuid.uuid4()
                obj.created_at = "2023-01-01T00:00:00Z"
                obj.updated_at = "2023-01-01T00:00:00Z"

            mock_db.refresh.side_effect = mock_refresh

            with patch('src.utils.logging.get_security_logger') as mock_logger:
                mock_security_logger = Mock()
                mock_logger.return_value = mock_security_logger

                result = create_task(mock_db, user_id, task_data)

                assert result is not None
                assert result.title == task_data.title
                mock_db.add.assert_called_once_with(mock_task_instance)
                mock_db.commit.assert_called_once()
                mock_security_logger.log_sensitive_operation.assert_called_once_with(
                    "CREATE_TASK",
                    str(user_id),
                    {"task_id": str(mock_task_instance.id), "title": task_data.title}
                )

    def test_create_task_database_error(self):
        """Test task creation when database error occurs"""
        # Mock database session to raise SQLAlchemyError
        mock_db = Mock(spec=Session)
        mock_db.commit.side_effect = SQLAlchemyError("DB Error")

        user_id = uuid.uuid4()
        task_data = TaskCreate(
            title="New Task",
            description="Task Description",
            due_date="2023-12-31T23:59:59Z",
            priority="medium"
        )

        # Mock the TaskModel creation
        with patch('src.models.task.Task') as mock_task_class:
            mock_task_instance = Mock()
            mock_task_class.return_value = mock_task_instance

            with pytest.raises(SQLAlchemyError):
                create_task(mock_db, user_id, task_data)

            mock_db.rollback.assert_called_once()

    def test_update_task_success(self):
        """Test successful task update"""
        # Mock database session
        mock_db = Mock(spec=Session)

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()
        task_data = TaskUpdate(
            title="Updated Task",
            description="Updated Description",
            is_completed=True
        )

        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.UUID(task_id)
        mock_task.title = "Original Task"
        mock_task.description = "Original Description"
        mock_task.is_completed = False
        mock_task.created_at = "2023-01-01T00:00:00Z"
        mock_task.updated_at = "2023-01-01T00:00:00Z"
        mock_task.due_date = "2023-12-31T23:59:59Z"
        mock_task.priority = "medium"
        mock_task.user_id = user_id

        mock_db.query.return_value.filter.return_value.first.return_value = mock_task

        with patch('src.utils.logging.get_security_logger') as mock_logger:
            mock_security_logger = Mock()
            mock_logger.return_value = mock_security_logger

            result = update_task(mock_db, task_id, user_id, task_data)

            assert result is not None
            assert result.title == "Updated Task"
            assert result.is_completed is True
            mock_db.commit.assert_called_once()
            mock_security_logger.log_sensitive_operation.assert_called_once_with(
                "UPDATE_TASK",
                str(user_id),
                {"task_id": task_id, "updated_fields": ["title", "description", "is_completed"]}
            )

    def test_update_task_invalid_uuid(self):
        """Test task update with invalid UUID"""
        mock_db = Mock(spec=Session)

        task_id = "invalid-uuid-format"
        user_id = uuid.uuid4()
        task_data = TaskUpdate(title="Updated Task")

        result = update_task(mock_db, task_id, user_id, task_data)

        assert result is None

    def test_update_task_not_found(self):
        """Test update of non-existent task"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()
        task_data = TaskUpdate(title="Updated Task")

        result = update_task(mock_db, task_id, user_id, task_data)

        assert result is None

    def test_update_task_database_error(self):
        """Test task update when database error occurs"""
        # Mock database session
        mock_db = Mock(spec=Session)

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()
        task_data = TaskUpdate(title="Updated Task")

        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.UUID(task_id)
        mock_task.user_id = user_id

        mock_db.query.return_value.filter.return_value.first.return_value = mock_task
        mock_db.commit.side_effect = SQLAlchemyError("DB Error")

        with pytest.raises(SQLAlchemyError):
            update_task(mock_db, task_id, user_id, task_data)

        mock_db.rollback.assert_called_once()

    def test_patch_task_success(self):
        """Test successful task patch"""
        # Mock database session
        mock_db = Mock(spec=Session)

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()
        task_data = TaskPatch(is_completed=True)

        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.UUID(task_id)
        mock_task.title = "Original Task"
        mock_task.is_completed = False
        mock_task.user_id = user_id

        mock_db.query.return_value.filter.return_value.first.return_value = mock_task

        with patch('src.utils.logging.get_security_logger') as mock_logger:
            mock_security_logger = Mock()
            mock_logger.return_value = mock_security_logger

            result = patch_task(mock_db, task_id, user_id, task_data)

            assert result is not None
            assert result.is_completed is True
            mock_db.commit.assert_called_once()
            mock_security_logger.log_sensitive_operation.assert_called_once_with(
                "PATCH_TASK",
                str(user_id),
                {"task_id": task_id, "updated_fields": ["is_completed"]}
            )

    def test_patch_task_invalid_uuid(self):
        """Test task patch with invalid UUID"""
        mock_db = Mock(spec=Session)

        task_id = "invalid-uuid-format"
        user_id = uuid.uuid4()
        task_data = TaskPatch(is_completed=True)

        result = patch_task(mock_db, task_id, user_id, task_data)

        assert result is None

    def test_patch_task_not_found(self):
        """Test patch of non-existent task"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()
        task_data = TaskPatch(is_completed=True)

        result = patch_task(mock_db, task_id, user_id, task_data)

        assert result is None

    def test_patch_task_database_error(self):
        """Test task patch when database error occurs"""
        # Mock database session
        mock_db = Mock(spec=Session)

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()
        task_data = TaskPatch(is_completed=True)

        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.UUID(task_id)
        mock_task.user_id = user_id

        mock_db.query.return_value.filter.return_value.first.return_value = mock_task
        mock_db.commit.side_effect = SQLAlchemyError("DB Error")

        with pytest.raises(SQLAlchemyError):
            patch_task(mock_db, task_id, user_id, task_data)

        mock_db.rollback.assert_called_once()

    def test_delete_task_success(self):
        """Test successful task deletion"""
        # Mock database session
        mock_db = Mock(spec=Session)

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()

        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.UUID(task_id)
        mock_task.user_id = user_id

        mock_db.query.return_value.filter.return_value.first.return_value = mock_task

        with patch('src.utils.logging.get_security_logger') as mock_logger:
            mock_security_logger = Mock()
            mock_logger.return_value = mock_security_logger

            result = delete_task(mock_db, task_id, user_id)

            assert result is True
            mock_db.delete.assert_called_once_with(mock_task)
            mock_db.commit.assert_called_once()
            mock_security_logger.log_sensitive_operation.assert_called_once_with(
                "DELETE_TASK",
                str(user_id),
                {"task_id": task_id}
            )

    def test_delete_task_invalid_uuid(self):
        """Test task deletion with invalid UUID"""
        mock_db = Mock(spec=Session)

        task_id = "invalid-uuid-format"
        user_id = uuid.uuid4()

        result = delete_task(mock_db, task_id, user_id)

        assert result is False

    def test_delete_task_not_found(self):
        """Test deletion of non-existent task"""
        # Mock database session
        mock_db = Mock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()

        result = delete_task(mock_db, task_id, user_id)

        assert result is False

    def test_delete_task_database_error(self):
        """Test task deletion when database error occurs"""
        # Mock database session
        mock_db = Mock(spec=Session)

        task_id = str(uuid.uuid4())
        user_id = uuid.uuid4()

        mock_task = Mock(spec=TaskModel)
        mock_task.id = uuid.UUID(task_id)
        mock_task.user_id = user_id

        mock_db.query.return_value.filter.return_value.first.return_value = mock_task
        mock_db.commit.side_effect = SQLAlchemyError("DB Error")

        with pytest.raises(SQLAlchemyError):
            delete_task(mock_db, task_id, user_id)

        mock_db.rollback.assert_called_once()