"""
Unit tests for Task model
"""
import pytest
from src.models.task import Task


def test_task_creation_with_valid_data():
    """Test creating a task with valid data"""
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False


def test_task_creation_with_defaults():
    """Test creating a task with default values"""
    task = Task(id=1, title="Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.completed is False


def test_task_creation_with_completed_true():
    """Test creating a task with completed status as True"""
    task = Task(id=1, title="Test Task", completed=True)
    assert task.completed is True


def test_task_creation_with_empty_title_raises_error():
    """Test that creating a task with empty title raises ValueError"""
    with pytest.raises(ValueError, match="Task title must be non-empty"):
        Task(id=1, title="")


def test_task_creation_with_whitespace_only_title_raises_error():
    """Test that creating a task with whitespace-only title raises ValueError"""
    with pytest.raises(ValueError, match="Task title must be non-empty"):
        Task(id=1, title="   ")


def test_task_creation_with_negative_id_raises_error():
    """Test that creating a task with negative ID raises ValueError"""
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id=-1, title="Test Task")


def test_task_creation_with_zero_id_raises_error():
    """Test that creating a task with zero ID raises ValueError"""
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id=0, title="Test Task")


def test_task_creation_with_non_integer_id_raises_error():
    """Test that creating a task with non-integer ID raises ValueError"""
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id="1", title="Test Task")


def test_task_completed_non_boolean_raises_error():
    """Test that creating a task with non-boolean completed status raises ValueError"""
    with pytest.raises(ValueError, match="Task completed status must be a boolean"):
        Task(id=1, title="Test Task", completed="true")