"""
Task domain model with validation
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Core entity representing a to-do item with attributes:
    id (integer, auto-generated and unique),
    title (string, required and non-empty),
    description (string, optional),
    completed (boolean, default false)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self):
        """Validate required fields after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Task title must be non-empty")
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("Task ID must be a positive integer")
        if not isinstance(self.completed, bool):
            raise ValueError("Task completed status must be a boolean")