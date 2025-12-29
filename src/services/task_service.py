"""
Business logic for task operations
"""
from typing import List, Optional
import sys
import os
# Add the src directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from models.task import Task
from repositories.task_repository import TaskRepository
from lib.validators import validate_task_title


class TaskService:
    """
    Service layer that handles business logic for task operations
    """

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_task(self, title: str, description: str = "") -> int:
        """
        Add a new task with validation
        - title (str, required): Non-empty task title
        - description (str, optional): Task description (default: "")
        Returns: int - Unique task ID
        """
        # Validate title
        if not validate_task_title(title):
            raise ValueError("Task title must be non-empty string")

        # Create task instance
        task = Task(id=0, title=title.strip(), description=description or "")
        task_id = self.repository.add_task(task)
        return task_id

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the repository
        Returns: List[Task] - List of all tasks in the system
        """
        return self.repository.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by ID
        - task_id (int, required): Unique task identifier
        Returns: Task - Task object with id, title, description, completed status
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        task = self.repository.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} does not exist")

        return task

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update specific task fields
        - task_id (int, required): Unique task identifier
        - title (str, optional): New task title (if provided)
        - description (str, optional): New task description (if provided)
        Returns: bool - True if update was successful
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        # Validate title if provided
        if title is not None:
            if not validate_task_title(title):
                raise ValueError("Task title must be non-empty string")

        # Prepare updates
        updates = {}
        if title is not None:
            updates['title'] = title.strip()
        if description is not None:
            updates['description'] = description

        # Perform update
        success = self.repository.update_task(task_id, **updates)
        if not success:
            raise ValueError(f"Task with ID {task_id} does not exist")

        return success

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID
        - task_id (int, required): Unique task identifier
        Returns: bool - True if deletion was successful
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        success = self.repository.delete_task(task_id)
        if not success:
            raise ValueError(f"Task with ID {task_id} does not exist")

        return success

    def toggle_task_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task
        - task_id (int, required): Unique task identifier
        Returns: bool - True if toggle was successful
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        success = self.repository.toggle_task_completion(task_id)
        if not success:
            raise ValueError(f"Task with ID {task_id} does not exist")

        return success