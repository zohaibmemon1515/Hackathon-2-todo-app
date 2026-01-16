"""
MCP Tools for task management operations
Stateless tools that interact with the database directly
"""
from typing import Dict, Any, Optional, List
from sqlmodel import Session, select
from ..models.task import Task
from ..database.database import get_engine
from ..utils.logging import security_logger


class MCPTaskTools:
    """Collection of MCP tools for managing tasks via natural language."""

    async def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task for the user with an integer task ID.
        """
        try:
            engine = get_engine()
            with Session(engine) as session:

                # Create the new task
                new_task = Task(
                    title=title,
                    description=description,
                    is_completed=False,
                    user_id=user_id  # UUID stays as string
                )

                session.add(new_task)
                session.commit()
                session.refresh(new_task)

                # Ensure task.id is integer (auto-increment)
                task_id = new_task.id

                security_logger.log_tool_usage(
                    user_id=user_id,
                    tool_name="add_task",
                    success=True,
                    details={"task_id": task_id, "task_title": title}
                )

                return {
                    "success": True,
                    "message": f"I've successfully added '{title}' to your task list.",
                    "task_id": task_id,
                    "task": {
                        "id": task_id,
                        "title": title,
                        "description": description,
                        "is_completed": False
                    }
                }
        except Exception as e:
            security_logger.log_tool_usage(
                user_id=user_id,
                tool_name="add_task",
                success=False,
                details={"error": str(e), "attempted_title": title}
            )
            return {"success": False, "message": f"Failed to add task. Error: {str(e)}"}

    async def list_tasks(self, user_id: str) -> Dict[str, Any]:
        """List all tasks for the user, task IDs as integers."""
        try:
            engine = get_engine()
            with Session(engine) as session:
                statement = select(Task).where(Task.user_id == user_id)
                tasks = session.exec(statement).all()

                task_list = []
                for task in tasks:
                    task_list.append({
                        "id": task.id,           # integer ID
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed
                    })

                message = f"Here are your {len(task_list)} tasks:" if task_list else "You don't have any tasks yet."

                return {
                    "success": True,
                    "message": message,
                    "tasks": task_list
                }

        except Exception as e:
            return {"success": False, "message": f"Failed to retrieve tasks. Error: {str(e)}"}

    async def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Mark a task as completed using integer task_id."""
        try:
            engine = get_engine()
            with Session(engine) as session:
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                task = session.exec(statement).first()

                if not task:
                    return {"success": False, "message": "Task not found."}

                task.is_completed = True
                session.add(task)
                session.commit()
                session.refresh(task)

                security_logger.log_tool_usage(
                    user_id=user_id,
                    tool_name="complete_task",
                    success=True,
                    details={"task_id": task_id}
                )

                return {
                    "success": True,
                    "message": f"Task '{task.title}' marked as completed.",
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed
                    }
                }

        except Exception as e:
            return {"success": False, "message": f"Failed to complete task. Error: {str(e)}"}

    async def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Delete a task using integer task_id."""
        try:
            engine = get_engine()
            with Session(engine) as session:
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                task = session.exec(statement).first()

                if not task:
                    return {"success": False, "message": "Task not found."}

                session.delete(task)
                session.commit()

                return {
                    "success": True,
                    "message": f"Task '{task.title}' deleted successfully."
                }

        except Exception as e:
            return {"success": False, "message": f"Failed to delete task. Error: {str(e)}"}

    async def update_task(self, user_id: str, task_id: int, **updates) -> Dict[str, Any]:
        """Update a task using integer task_id."""
        try:
            engine = get_engine()
            with Session(engine) as session:
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                task = session.exec(statement).first()

                if not task:
                    return {"success": False, "message": "Task not found."}

                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)

                session.add(task)
                session.commit()
                session.refresh(task)

                return {
                    "success": True,
                    "message": f"Task '{task.title}' updated successfully.",
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed
                    }
                }

        except Exception as e:
            return {"success": False, "message": f"Failed to update task. Error: {str(e)}"}
