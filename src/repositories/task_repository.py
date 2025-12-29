"""
In-memory task storage with auto-incrementing IDs
"""
from typing import Dict, List, Optional
import sys
import os
# Add the src directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from models.task import Task


class TaskRepository:
    """
    In-memory task repository that manages task storage and retrieval
    with auto-incrementing task IDs
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, task: Task) -> int:
        """
        Add a new task to the repository
        Auto-generate ID if task.id is 0 or negative
        """
        if task.id <= 0:
            task.id = self._next_id
            self._next_id += 1
        elif task.id >= self._next_id:
            # If a task is added with a higher ID, update the next_id
            self._next_id = task.id + 1

        self._tasks[task.id] = task
        return task.id

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the repository
        """
        return list(self._tasks.values())

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by ID
        """
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, **updates) -> bool:
        """
        Update specific task fields
        Only updates fields that exist in the Task model
        """
        if task_id not in self._tasks:
            return False

        task = self._tasks[task_id]

        # Only allow updating valid Task fields
        valid_fields = {'title', 'description', 'completed'}
        for field, value in updates.items():
            if field in valid_fields and hasattr(task, field):
                setattr(task, field, value)

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the repository
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_task_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task
        """
        if task_id not in self._tasks:
            return False

        task = self._tasks[task_id]
        task.completed = not task.completed
        return True