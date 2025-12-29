"""
Unit tests for task data integrity
"""
import pytest
from src.models.task import Task


def test_task_creation_with_required_fields():
    """Test that required fields are properly validated"""
    # Valid creation
    task = Task(id=1, title="Valid Title")
    assert task.id == 1
    assert task.title == "Valid Title"
    assert task.description == ""
    assert task.completed is False


def test_task_creation_with_all_fields():
    """Test that all fields can be set during creation"""
    task = Task(id=1, title="Test Title", description="Test Description", completed=True)
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.completed is True


def test_task_creation_with_default_values():
    """Test that default values are properly applied"""
    task = Task(id=1, title="Test Title", description="Test Description")
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.completed is False  # Default value


def test_task_title_cannot_be_empty():
    """Test that empty title raises ValueError"""
    with pytest.raises(ValueError, match="Task title must be non-empty"):
        Task(id=1, title="")


def test_task_title_cannot_be_whitespace_only():
    """Test that whitespace-only title raises ValueError"""
    with pytest.raises(ValueError, match="Task title must be non-empty"):
        Task(id=1, title="   ")


def test_task_title_cannot_be_none():
    """Test that None title raises ValueError"""
    with pytest.raises(ValueError, match="Task title must be non-empty"):
        Task(id=1, title=None)


def test_task_id_must_be_positive_integer():
    """Test that invalid IDs raise ValueError"""
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id=0, title="Valid Title")

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id=-1, title="Valid Title")

    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id="1", title="Valid Title")


def test_task_completed_must_be_boolean():
    """Test that non-boolean completed status raises ValueError"""
    with pytest.raises(ValueError, match="Task completed status must be a boolean"):
        Task(id=1, title="Valid Title", completed="true")

    with pytest.raises(ValueError, match="Task completed status must be a boolean"):
        Task(id=1, title="Valid Title", completed=1)

    with pytest.raises(ValueError, match="Task completed status must be a boolean"):
        Task(id=1, title="Valid Title", completed="False")


def test_task_description_can_be_empty():
    """Test that empty description is allowed"""
    task = Task(id=1, title="Valid Title", description="")
    assert task.description == ""


def test_task_description_defaults_to_empty_string():
    """Test that description defaults to empty string when not provided"""
    task = Task(id=1, title="Valid Title")
    assert task.description == ""


def test_task_completed_defaults_to_false():
    """Test that completed defaults to False when not provided"""
    task = Task(id=1, title="Valid Title")
    assert task.completed is False


def test_task_field_immutability_after_creation():
    """Test that task fields can be modified after creation"""
    task = Task(id=1, title="Original Title", description="Original Description", completed=False)

    # Modify fields
    task.title = "New Title"
    task.description = "New Description"
    task.completed = True

    assert task.title == "New Title"
    assert task.description == "New Description"
    assert task.completed is True


def test_task_data_consistency():
    """Test that task data remains consistent after operations"""
    original_id = 1
    original_title = "Original Title"
    original_description = "Original Description"
    original_completed = False

    task = Task(id=original_id, title=original_title, description=original_description, completed=original_completed)

    # Verify initial values
    assert task.id == original_id
    assert task.title == original_title
    assert task.description == original_description
    assert task.completed == original_completed

    # Change values
    task.id = 2
    task.title = "Updated Title"
    task.description = "Updated Description"
    task.completed = True

    # Verify updated values
    assert task.id == 2
    assert task.title == "Updated Title"
    assert task.description == "Updated Description"
    assert task.completed is True