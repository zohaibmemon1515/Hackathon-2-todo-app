"""
Input validation utilities
"""


def validate_task_title(title: str) -> bool:
    """
    Validate that task title is non-empty string
    """
    if not title:
        return False
    if not isinstance(title, str):
        return False
    if not title.strip():
        return False
    return True


def validate_task_description(description: str) -> bool:
    """
    Validate that task description is a string (optional field)
    """
    if description is None:
        return True
    if not isinstance(description, str):
        return False
    return True


def validate_task_completed(completed: bool) -> bool:
    """
    Validate that completed status is a boolean
    """
    return isinstance(completed, bool)


def validate_task_id(task_id: int) -> bool:
    """
    Validate that task ID is a positive integer
    """
    if not isinstance(task_id, int):
        return False
    if task_id <= 0:
        return False
    return True