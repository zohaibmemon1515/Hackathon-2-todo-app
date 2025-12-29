"""
Unit tests for task validation in service layer
"""
import pytest
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


def test_service_add_task_validates_title():
    """Test that the service validates task title when adding"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Valid title should work
    task_id = service.add_task("Valid Title")
    assert task_id == 1

    # Empty title should raise ValueError
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.add_task("")

    # Whitespace-only title should raise ValueError
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.add_task("   ")


def test_service_update_task_validates_title():
    """Test that the service validates task title when updating"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task first
    task_id = service.add_task("Original Title")

    # Valid title update should work
    service.update_task(task_id, title="New Valid Title")
    updated_task = service.get_task_by_id(task_id)
    assert updated_task.title == "New Valid Title"

    # Empty title update should raise ValueError
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.update_task(task_id, title="")


def test_service_add_task_handles_description():
    """Test that the service properly handles optional description"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add task with description
    task_id1 = service.add_task("Title", "Description")
    task1 = service.get_task_by_id(task_id1)
    assert task1.description == "Description"

    # Add task without description
    task_id2 = service.add_task("Title")
    task2 = service.get_task_by_id(task_id2)
    assert task2.description == ""


def test_service_validates_task_ids():
    """Test that the service validates task IDs"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task first
    task_id = service.add_task("Test Title")

    # Valid positive integer IDs should work
    service.get_task_by_id(task_id)
    service.update_task(task_id, title="Updated")
    service.delete_task(task_id)

    # Invalid IDs should raise ValueError
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.get_task_by_id(0)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.get_task_by_id(-1)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.update_task(0, title="New Title")

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.delete_task(-5)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.toggle_task_completion(0)


def test_service_handles_nonexistent_tasks():
    """Test that the service properly handles operations on non-existent tasks"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Operations on non-existent tasks should raise ValueError
    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.get_task_by_id(999)

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.update_task(999, title="New Title")

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.delete_task(999)

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.toggle_task_completion(999)


def test_service_enforces_data_integrity():
    """Test that the service enforces data integrity across operations"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task
    task_id = service.add_task("Original Title", "Original Description")
    original_task = service.get_task_by_id(task_id)
    assert original_task.title == "Original Title"
    assert original_task.description == "Original Description"
    assert original_task.completed is False

    # Update only the title
    service.update_task(task_id, title="Updated Title")
    updated_task = service.get_task_by_id(task_id)
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Original Description"  # Should remain unchanged
    assert updated_task.completed is False  # Should remain unchanged

    # Update only the description
    service.update_task(task_id, description="Updated Description")
    updated_task = service.get_task_by_id(task_id)
    assert updated_task.title == "Updated Title"  # Should remain unchanged
    assert updated_task.description == "Updated Description"
    assert updated_task.completed is False  # Should remain unchanged

    # Update completion status
    service.toggle_task_completion(task_id)
    updated_task = service.get_task_by_id(task_id)
    assert updated_task.completed is True


def test_service_validation_on_update_partial_fields():
    """Test that the service properly validates partial updates"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task
    task_id = service.add_task("Original Title", "Original Description")

    # Update only description (title should remain)
    service.update_task(task_id, description="New Description")
    task = service.get_task_by_id(task_id)
    assert task.title == "Original Title"
    assert task.description == "New Description"

    # Update only title (description should remain)
    service.update_task(task_id, title="New Title")
    task = service.get_task_by_id(task_id)
    assert task.title == "New Title"
    assert task.description == "New Description"


def test_service_validation_on_empty_updates():
    """Test that the service handles empty update requests appropriately"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task
    task_id = service.add_task("Original Title", "Original Description")

    # Try to update with no changes (should not cause error in the service itself)
    # The service should allow updates even if no fields change
    original_task = service.get_task_by_id(task_id)
    service.update_task(task_id, title=original_task.title)  # Update with same value
    updated_task = service.get_task_by_id(task_id)
    assert updated_task.title == original_task.title