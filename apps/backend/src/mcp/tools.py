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

    async def add_task(self, user_id: str, title: str, description: Optional[str] = None, reminder_at: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task. 
        REQUIRED: title (What needs to be done).
        OPTIONAL: description (Extra details), reminder_at (Time/Date for reminder).
        
        If the user hasn't provided a title, the assistant must ask for it.
        """
        # Basic Validation: Agar title nahi hai toh task nahi ban sakta
        if not title or title.strip() == "":
            return {
                "success": False, 
                "message": "I need a title for the task. What is the task about?",
                "requires_input": "title"
            }

        try:
            engine = get_engine()
            with Session(engine) as session:
                # Task create karna aur reminder_at save karna
                new_task = Task(
                    title=title,
                    description=description,
                    is_completed=False,
                    user_id=user_id,
                    reminder_at=reminder_at  # DB mein time save ho raha hai
                )

                session.add(new_task)
                session.commit()
                session.refresh(new_task)

                task_id = new_task.id

                security_logger.log_tool_usage(
                    user_id=user_id,
                    tool_name="add_task",
                    success=True,
                    details={"task_id": task_id, "task_title": title, "reminder_at": reminder_at}
                )

                # Response message mein details include karna
                msg = f"Task '{title}' has been added."
                if reminder_at:
                    msg += f" I've also set a reminder for {reminder_at}."

                return {
                    "success": True,
                    "message": msg,
                    "task_id": task_id,
                    "task": {
                        "id": task_id,
                        "title": title,
                        "description": description,
                        "reminder_at": reminder_at,
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
        """List all tasks for the user."""
        try:
            engine = get_engine()
            with Session(engine) as session:
                statement = select(Task).where(Task.user_id == user_id)
                tasks = session.exec(statement).all()

                task_list = []
                for task in tasks:
                    task_list.append({
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "reminder_at": getattr(task, 'reminder_at', None),
                        "is_completed": task.is_completed
                    })

                return {
                    "success": True,
                    "message": f"You have {len(task_list)} tasks.",
                    "tasks": task_list
                }
        except Exception as e:
            return {"success": False, "message": f"Failed to retrieve tasks: {str(e)}"}

    async def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Mark a task as completed."""
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

                return {
                    "success": True,
                    "message": f"Task '{task.title}' completed.",
                    "task": {"id": task.id, "is_completed": True}
                }
        except Exception as e:
            return {"success": False, "message": str(e)}

    async def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Delete a task."""
        try:
            engine = get_engine()
            with Session(engine) as session:
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                task = session.exec(statement).first()
                if not task: return {"success": False, "message": "Task not found."}
                session.delete(task)
                session.commit()
                return {"success": True, "message": "Task deleted."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    async def update_task(self, user_id: str, task_id: int, **updates) -> Dict[str, Any]:
        """Update any field of a task."""
        try:
            engine = get_engine()
            with Session(engine) as session:
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                task = session.exec(statement).first()
                if not task: return {"success": False, "message": "Task not found."}

                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)

                session.add(task)
                session.commit()
                session.refresh(task)
                return {"success": True, "message": "Task updated."}
        except Exception as e:
            return {"success": False, "message": str(e)}