"""
Unit tests for TaskService
"""
import pytest
from src.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


def test_add_task_with_valid_data():
    """Test adding a task with valid title and description"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Test Task", "Test Description")

    assert task_id == 1
    task = service.get_task_by_id(task_id)
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False


def test_add_task_with_title_only():
    """Test adding a task with only a title"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Test Task")

    assert task_id == 1
    task = service.get_task_by_id(task_id)
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.completed is False


def test_add_task_with_empty_title_raises_error():
    """Test that adding a task with empty title raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.add_task("")


def test_add_task_with_whitespace_only_title_raises_error():
    """Test that adding a task with whitespace-only title raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.add_task("   ")


def test_get_all_tasks_empty():
    """Test getting all tasks when no tasks exist"""
    repo = TaskRepository()
    service = TaskService(repo)

    tasks = service.get_all_tasks()

    assert tasks == []


def test_get_all_tasks_with_tasks():
    """Test getting all tasks when tasks exist"""
    repo = TaskRepository()
    service = TaskService(repo)

    service.add_task("Task 1", "Description 1")
    service.add_task("Task 2", "Description 2")

    tasks = service.get_all_tasks()

    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_get_task_by_id_existing():
    """Test getting a task by existing ID"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Test Task", "Test Description")
    task = service.get_task_by_id(task_id)

    assert task.title == "Test Task"
    assert task.description == "Test Description"


def test_get_task_by_id_non_existing():
    """Test getting a task by non-existing ID raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.get_task_by_id(999)


def test_get_task_by_id_invalid():
    """Test getting a task by invalid ID raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.get_task_by_id(-1)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.get_task_by_id(0)


def test_update_task_title():
    """Test updating a task's title"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Original Title", "Original Description")
    service.update_task(task_id, title="New Title")

    updated_task = service.get_task_by_id(task_id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "Original Description"


def test_update_task_description():
    """Test updating a task's description"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Original Title", "Original Description")
    service.update_task(task_id, description="New Description")

    updated_task = service.get_task_by_id(task_id)
    assert updated_task.title == "Original Title"
    assert updated_task.description == "New Description"


def test_update_task_both_fields():
    """Test updating both title and description"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Original Title", "Original Description")
    service.update_task(task_id, title="New Title", description="New Description")

    updated_task = service.get_task_by_id(task_id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"


def test_update_task_invalid_id():
    """Test updating a task with invalid ID raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.update_task(-1, title="New Title")

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.update_task(0, title="New Title")


def test_update_task_non_existing():
    """Test updating a non-existing task raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.update_task(999, title="New Title")


def test_update_task_with_empty_title():
    """Test updating a task with empty title raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Original Title", "Original Description")

    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.update_task(task_id, title="")


def test_delete_task_existing():
    """Test deleting an existing task"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Test Task", "Test Description")
    result = service.delete_task(task_id)

    assert result is True
    with pytest.raises(ValueError, match="Task with ID 1 does not exist"):
        service.get_task_by_id(task_id)


def test_delete_task_non_existing():
    """Test deleting a non-existing task raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.delete_task(999)


def test_delete_task_invalid_id():
    """Test deleting a task with invalid ID raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.delete_task(-1)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.delete_task(0)


def test_toggle_task_completion():
    """Test toggling task completion status"""
    repo = TaskRepository()
    service = TaskService(repo)

    task_id = service.add_task("Test Task", "Test Description")

    # Initially should be False
    task = service.get_task_by_id(task_id)
    assert task.completed is False

    # Toggle to True
    result = service.toggle_task_completion(task_id)
    assert result is True
    task = service.get_task_by_id(task_id)
    assert task.completed is True

    # Toggle back to False
    result = service.toggle_task_completion(task_id)
    assert result is True
    task = service.get_task_by_id(task_id)
    assert task.completed is False


def test_toggle_task_completion_invalid_id():
    """Test toggling completion status with invalid ID raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.toggle_task_completion(-1)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.toggle_task_completion(0)


def test_toggle_task_completion_non_existing():
    """Test toggling completion status of non-existing task raises ValueError"""
    repo = TaskRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.toggle_task_completion(999)