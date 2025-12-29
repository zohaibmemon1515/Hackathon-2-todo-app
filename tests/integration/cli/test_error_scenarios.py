"""
Integration tests for error scenarios in CLI
"""
import io
import sys
from contextlib import redirect_stdout
from unittest.mock import patch
import pytest
from src.main import TodoApp


def test_cli_handles_invalid_task_ids():
    """Test that CLI properly handles invalid task IDs"""
    app = TodoApp()

    # Test invalid ID in get_task_by_id
    with pytest.raises(ValueError):
        app.service.get_task_by_id(-1)

    with pytest.raises(ValueError):
        app.service.get_task_by_id(0)

    with pytest.raises(ValueError):
        app.service.get_task_by_id("invalid")


def test_cli_add_task_with_invalid_input():
    """Test CLI behavior when adding task with invalid input"""
    app = TodoApp()

    # Try to add task with empty title
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        app.service.add_task("")


def test_cli_update_task_with_invalid_input():
    """Test CLI behavior when updating task with invalid input"""
    app = TodoApp()

    # Add a task first
    task_id = app.service.add_task("Original Title")

    # Try to update with empty title
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        app.service.update_task(task_id, title="")


def test_cli_handles_nonexistent_tasks():
    """Test that CLI properly handles operations on non-existent tasks"""
    app = TodoApp()

    # Try operations on non-existent task
    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        app.service.get_task_by_id(999)

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        app.service.update_task(999, title="New Title")

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        app.service.delete_task(999)

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        app.service.toggle_task_completion(999)


def test_cli_error_handling_in_methods():
    """Test error handling within CLI methods"""
    app = TodoApp()

    # Add a task
    task_id = app.service.add_task("Test Task")

    # Test view_all_tasks with no errors
    tasks = app.service.get_all_tasks()
    assert len(tasks) == 1

    # Test get_task_by_id with valid ID
    task = app.service.get_task_by_id(task_id)
    assert task.title == "Test Task"

    # Test error case for get_task_by_id
    try:
        app.service.get_task_by_id(999)
        assert False, "Expected ValueError was not raised"
    except ValueError as e:
        assert "does not exist" in str(e)


def test_cli_user_input_validation():
    """Test that CLI validates user input properly"""
    app = TodoApp()

    # Test that the CLI methods validate input before processing
    # This tests the validation at the service level which is called by CLI

    # Invalid ID handling in CLI context
    with pytest.raises(ValueError):
        app.service.get_task_by_id(-5)

    # Invalid title handling
    with pytest.raises(ValueError, match="Task title must be non-empty string"):
        app.service.add_task("")


def test_cli_error_messages_are_user_friendly():
    """Test that error messages are appropriate for CLI context"""
    app = TodoApp()

    # Capture error messages to verify they are user-friendly
    try:
        app.service.get_task_by_id(-1)
    except ValueError as e:
        error_msg = str(e)
        assert "positive integer" in error_msg

    try:
        app.service.get_task_by_id(999)
    except ValueError as e:
        error_msg = str(e)
        assert "does not exist" in error_msg

    try:
        app.service.add_task("")
    except ValueError as e:
        error_msg = str(e)
        assert "non-empty string" in error_msg


def test_cli_does_not_crash_on_invalid_input():
    """Test that CLI handles invalid input without crashing"""
    app = TodoApp()

    # These operations should raise appropriate exceptions rather than crash
    invalid_operations = [
        lambda: app.service.get_task_by_id(-1),
        lambda: app.service.get_task_by_id(0),
        lambda: app.service.get_task_by_id("invalid"),
        lambda: app.service.update_task(-1, title="New"),
        lambda: app.service.delete_task(999),
        lambda: app.service.toggle_task_completion(0),
        lambda: app.service.add_task(""),
    ]

    for operation in invalid_operations:
        with pytest.raises(ValueError):
            operation()


def test_cli_menu_method_error_handling():
    """Test error handling in CLI menu methods"""
    app = TodoApp()

    # Add a task to work with
    task_id = app.service.add_task("Test Task")

    # Test error handling in update_task method when called directly
    # with invalid parameters
    try:
        app.service.update_task(999, title="New Title")  # Non-existent task
    except ValueError as e:
        assert "does not exist" in str(e)

    try:
        app.service.update_task(-1, title="New Title")  # Invalid ID
    except ValueError as e:
        assert "positive integer" in str(e)


def test_cli_add_task_method_validation():
    """Test validation in CLI add_task method"""
    app = TodoApp()

    # Test that empty title is rejected
    try:
        app.service.add_task("")
        assert False, "Expected ValueError was not raised for empty title"
    except ValueError as e:
        assert "non-empty string" in str(e)

    # Test that whitespace-only title is rejected
    try:
        app.service.add_task("   ")
        assert False, "Expected ValueError was not raised for whitespace-only title"
    except ValueError as e:
        assert "non-empty string" in str(e)


def test_cli_repository_error_propagation():
    """Test that repository errors are properly propagated through the CLI layers"""
    app = TodoApp()

    # Add a task
    task_id = app.service.add_task("Test Task")

    # Test that repository-level errors (like non-existent tasks)
    # are properly handled and converted to appropriate service-level errors
    try:
        app.service.get_task_by_id(9999)  # Much higher ID that doesn't exist
    except ValueError as e:
        assert "does not exist" in str(e)

    try:
        app.service.update_task(9999, title="New Title")
    except ValueError as e:
        assert "does not exist" in str(e)

    try:
        app.service.delete_task(9999)
    except ValueError as e:
        assert "does not exist" in str(e)