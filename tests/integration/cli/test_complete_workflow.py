"""
Comprehensive integration tests for complete workflow
"""
import io
import sys
from contextlib import redirect_stdout
from unittest.mock import patch
from src.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService
from src.main import TodoApp


def test_complete_task_workflow():
    """Test the complete workflow of adding, viewing, updating, and deleting tasks"""
    app = TodoApp()

    # Initial state: no tasks
    initial_tasks = app.service.get_all_tasks()
    assert len(initial_tasks) == 0

    # Add a task
    task_id = app.service.add_task("Test Task", "Test Description")
    assert task_id == 1

    # Verify task was added
    tasks = app.service.get_all_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False

    # Get the specific task
    retrieved_task = app.service.get_task_by_id(task_id)
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.description == "Test Description"
    assert retrieved_task.completed is False

    # Update the task
    app.service.update_task(task_id, title="Updated Task", description="Updated Description")

    # Verify update
    updated_task = app.service.get_task_by_id(task_id)
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed is False

    # Toggle completion status
    app.service.toggle_task_completion(task_id)

    # Verify completion toggle
    toggled_task = app.service.get_task_by_id(task_id)
    assert toggled_task.completed is True

    # Toggle completion status back
    app.service.toggle_task_completion(task_id)

    # Verify completion toggle back to False
    toggled_task = app.service.get_task_by_id(task_id)
    assert toggled_task.completed is False

    # Delete the task
    result = app.service.delete_task(task_id)
    assert result is True

    # Verify task was deleted
    final_tasks = app.service.get_all_tasks()
    assert len(final_tasks) == 0

    # Verify task cannot be retrieved after deletion
    try:
        app.service.get_task_by_id(task_id)
        assert False, "Expected ValueError was not raised"
    except ValueError:
        pass  # Expected


def test_multiple_tasks_workflow():
    """Test workflow with multiple tasks"""
    app = TodoApp()

    # Add multiple tasks
    id1 = app.service.add_task("Task 1", "Description 1")
    id2 = app.service.add_task("Task 2", "Description 2")
    id3 = app.service.add_task("Task 3", "Description 3")

    # Verify all tasks were added
    all_tasks = app.service.get_all_tasks()
    assert len(all_tasks) == 3

    # Verify each task
    task1 = app.service.get_task_by_id(id1)
    assert task1.title == "Task 1"
    assert task1.description == "Description 1"

    task2 = app.service.get_task_by_id(id2)
    assert task2.title == "Task 2"
    assert task2.description == "Description 2"

    task3 = app.service.get_task_by_id(id3)
    assert task3.title == "Task 3"
    assert task3.description == "Description 3"

    # Update one task
    app.service.update_task(id2, title="Updated Task 2")
    updated_task2 = app.service.get_task_by_id(id2)
    assert updated_task2.title == "Updated Task 2"

    # Toggle completion of another task
    app.service.toggle_task_completion(id3)
    toggled_task3 = app.service.get_task_by_id(id3)
    assert toggled_task3.completed is True

    # Delete one task
    app.service.delete_task(id1)

    # Verify remaining tasks
    remaining_tasks = app.service.get_all_tasks()
    assert len(remaining_tasks) == 2

    # Verify the right task was deleted
    try:
        app.service.get_task_by_id(id1)
        assert False, "Expected ValueError was not raised for deleted task"
    except ValueError:
        pass  # Expected

    # Verify other tasks still exist
    assert app.service.get_task_by_id(id2).title == "Updated Task 2"
    assert app.service.get_task_by_id(id3).completed is True


def test_empty_repository_behavior():
    """Test behavior when repository is empty"""
    app = TodoApp()

    # Verify initial state
    tasks = app.service.get_all_tasks()
    assert len(tasks) == 0

    # Verify appropriate errors for operations on empty repository
    try:
        app.service.get_task_by_id(1)
        assert False, "Expected ValueError was not raised"
    except ValueError:
        pass  # Expected


def test_task_completion_workflow():
    """Test the complete task completion workflow"""
    app = TodoApp()

    # Add a task
    task_id = app.service.add_task("Completion Test Task")

    # Initially should be incomplete
    task = app.service.get_task_by_id(task_id)
    assert task.completed is False

    # Toggle to complete
    app.service.toggle_task_completion(task_id)
    task = app.service.get_task_by_id(task_id)
    assert task.completed is True

    # Toggle back to incomplete
    app.service.toggle_task_completion(task_id)
    task = app.service.get_task_by_id(task_id)
    assert task.completed is False


def test_service_layer_integration():
    """Test integration between service layer components"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add task via service
    task_id = service.add_task("Service Test Task", "Service Test Description")
    assert task_id > 0

    # Retrieve via service
    task = service.get_task_by_id(task_id)
    assert task.title == "Service Test Task"
    assert task.description == "Service Test Description"

    # Update via service
    service.update_task(task_id, title="Updated Service Task")
    updated_task = service.get_task_by_id(task_id)
    assert updated_task.title == "Updated Service Task"

    # Toggle via service
    service.toggle_task_completion(task_id)
    toggled_task = service.get_task_by_id(task_id)
    assert toggled_task.completed is True

    # Delete via service
    result = service.delete_task(task_id)
    assert result is True

    # Verify deletion
    try:
        service.get_task_by_id(task_id)
        assert False, "Expected ValueError was not raised"
    except ValueError:
        pass  # Expected


def test_repository_service_data_consistency():
    """Test that data remains consistent across repository and service layers"""
    repo = TaskRepository()
    service = TaskService(repo)

    # Add task
    task_id = service.add_task("Consistency Test", "Checking data consistency")

    # Verify via repository directly
    direct_task = repo.get_task_by_id(task_id)
    assert direct_task.title == "Consistency Test"
    assert direct_task.description == "Checking data consistency"
    assert direct_task.completed is False

    # Update via service
    service.update_task(task_id, description="Updated description", completed=True)

    # Verify via repository directly
    direct_task = repo.get_task_by_id(task_id)
    assert direct_task.description == "Updated description"
    assert direct_task.completed is True

    # Toggle via service
    service.toggle_task_completion(task_id)

    # Verify via repository directly
    direct_task = repo.get_task_by_id(task_id)
    assert direct_task.completed is False  # Should be toggled back to False


def test_error_handling_integration():
    """Test that error handling works across the entire stack"""
    app = TodoApp()

    # Test error propagation from repository through service to CLI
    try:
        app.service.get_task_by_id(999)
        assert False, "Expected ValueError was not raised"
    except ValueError as e:
        assert "does not exist" in str(e)

    try:
        app.service.update_task(999, title="New Title")
        assert False, "Expected ValueError was not raised"
    except ValueError as e:
        assert "does not exist" in str(e)

    try:
        app.service.delete_task(999)
        assert False, "Expected ValueError was not raised"
    except ValueError as e:
        assert "does not exist" in str(e)

    try:
        app.service.toggle_task_completion(999)
        assert False, "Expected ValueError was not raised"
    except ValueError as e:
        assert "does not exist" in str(e)

    # Test validation error propagation
    try:
        app.service.add_task("")
        assert False, "Expected ValueError was not raised"
    except ValueError as e:
        assert "non-empty string" in str(e)


def test_cli_app_integration():
    """Test full CLI application integration"""
    app = TodoApp()

    # Test the app's main components work together
    assert hasattr(app, 'service')
    assert hasattr(app, 'repository')
    assert hasattr(app, 'display_menu')
    assert hasattr(app, 'add_task')
    assert hasattr(app, 'view_all_tasks')
    assert hasattr(app, 'update_task')
    assert hasattr(app, 'delete_task')
    assert hasattr(app, 'toggle_task_completion')

    # Perform a series of operations to test integration
    # Add task
    task_id = app.service.add_task("CLI Integration Task")

    # View tasks
    tasks = app.service.get_all_tasks()
    assert len(tasks) == 1

    # Update task
    app.service.update_task(task_id, description="Integration test description")

    # Check updated task
    updated_task = app.service.get_task_by_id(task_id)
    assert updated_task.description == "Integration test description"

    # Toggle completion
    app.service.toggle_task_completion(task_id)
    toggled_task = app.service.get_task_by_id(task_id)
    assert toggled_task.completed is True

    # Delete task
    app.service.delete_task(task_id)

    # Verify deletion
    final_tasks = app.service.get_all_tasks()
    assert len(final_tasks) == 0


def test_workflow_with_edge_cases():
    """Test workflow with edge cases handled properly"""
    app = TodoApp()

    # Add task with minimal data (only required fields)
    task_id = app.service.add_task("Minimal Task")
    task = app.service.get_task_by_id(task_id)
    assert task.title == "Minimal Task"
    assert task.description == ""  # Default value
    assert task.completed is False  # Default value

    # Update only the description
    app.service.update_task(task_id, description="Only description updated")
    updated_task = app.service.get_task_by_id(task_id)
    assert updated_task.title == "Minimal Task"  # Should remain unchanged
    assert updated_task.description == "Only description updated"
    assert updated_task.completed is False  # Should remain unchanged

    # Update only the completion status via toggle
    app.service.toggle_task_completion(task_id)
    toggled_task = app.service.get_task_by_id(task_id)
    assert toggled_task.completed is True

    # Update only the title
    app.service.update_task(task_id, title="Updated Minimal Task")
    title_updated_task = app.service.get_task_by_id(task_id)
    assert title_updated_task.title == "Updated Minimal Task"
    assert title_updated_task.description == "Only description updated"  # Should remain unchanged
    assert title_updated_task.completed is True  # Should remain unchanged