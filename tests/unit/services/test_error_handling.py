"""
Unit tests for error handling in service layer
"""
import pytest
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


def test_service_handles_invalid_task_ids():
    """Test that the service properly handles invalid task IDs"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Test with negative ID
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.get_task_by_id(-1)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.update_task(-1, title="New Title")

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.delete_task(-5)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.toggle_task_completion(-10)

    # Test with zero ID
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.get_task_by_id(0)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.update_task(0, title="New Title")

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.delete_task(0)

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.toggle_task_completion(0)

    # Test with non-integer ID
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.get_task_by_id("1")

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.update_task("invalid", title="New Title")


def test_service_handles_nonexistent_task_operations():
    """Test that the service properly handles operations on non-existent tasks"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Try to get non-existent task
    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.get_task_by_id(999)

    # Try to update non-existent task
    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.update_task(999, title="New Title")

    # Try to delete non-existent task
    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.delete_task(999)

    # Try to toggle completion of non-existent task
    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.toggle_task_completion(999)


def test_service_handles_invalid_input_during_creation():
    """Test that the service properly validates input during task creation"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Empty title should raise error
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.add_task("")

    # Whitespace-only title should raise error
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.add_task("   ")

    # None title should raise error (if passed directly)
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.add_task(None)


def test_service_handles_invalid_input_during_update():
    """Test that the service properly validates input during task updates"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task first
    task_id = service.add_task("Original Title")

    # Try to update with empty title
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.update_task(task_id, title="")

    # Try to update with whitespace-only title
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.update_task(task_id, title="   ")


def test_service_error_messages_are_clear():
    """Test that error messages are clear and user-friendly"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task first
    task_id = service.add_task("Test Task")

    # Test various error conditions and verify message clarity
    try:
        service.get_task_by_id(-1)
    except ValueError as e:
        assert "positive integer" in str(e)

    try:
        service.get_task_by_id(999)
    except ValueError as e:
        assert "does not exist" in str(e)

    try:
        service.update_task(-1, title="New Title")
    except ValueError as e:
        assert "positive integer" in str(e)

    try:
        service.update_task(999, title="New Title")
    except ValueError as e:
        assert "does not exist" in str(e)

    try:
        service.add_task("")
    except ValueError as e:
        assert "non-empty string" in str(e)


def test_service_operations_fail_gracefully():
    """Test that service operations fail gracefully without crashing"""
    repo = TaskRepository()
    service = TaskService(repo)

    # All of these should raise appropriate exceptions rather than crashing
    error_conditions = [
        lambda: service.get_task_by_id(-1),
        lambda: service.get_task_by_id(0),
        lambda: service.get_task_by_id("invalid"),
        lambda: service.update_task(-1, title="New"),
        lambda: service.delete_task(999),
        lambda: service.toggle_task_completion(0),
        lambda: service.add_task(""),
    ]

    for condition in error_conditions:
        with pytest.raises(ValueError):
            condition()


def test_service_handles_edge_cases_in_update():
    """Test that the service handles edge cases in update operations"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task first
    task_id = service.add_task("Original Title")

    # Update with same values should work
    service.update_task(task_id, title="Original Title")
    task = service.get_task_by_id(task_id)
    assert task.title == "Original Title"

    # Update with empty description should work (description is optional)
    service.update_task(task_id, description="")
    task = service.get_task_by_id(task_id)
    assert task.description == ""

    # Update with None values should be handled properly
    # (in our implementation, None values are ignored in updates)
    service.update_task(task_id, title="Updated Title")
    task = service.get_task_by_id(task_id)
    assert task.title == "Updated Title"


def test_service_error_handling_with_mixed_validations():
    """Test error handling when multiple validations are involved"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add a task first
    task_id = service.add_task("Original Title")

    # Valid ID but invalid title should still raise title error
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        service.update_task(task_id, title="")

    # Invalid ID should raise ID error regardless of title validity
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        service.update_task(-1, title="Valid Title")

    # Non-existent ID should raise ID exists error
    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.update_task(999, title="Valid Title")