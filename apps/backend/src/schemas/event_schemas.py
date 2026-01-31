"""Event Schemas Module

This module defines Pydantic schemas for Kafka events.
These schemas are used for validation and documentation purposes.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class EventType(str, Enum):
    """Enumeration of all possible event types."""
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_DELETED = "task.deleted"
    REMINDER_SET = "reminder.set"
    TASK_SYNC = "task.sync"


class BaseEventSchema(BaseModel):
    """Base schema for all events."""
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None


class TaskEventSchema(BaseEventSchema):
    """Schema for task-related events."""
    task_id: int
    user_id: str
    title: str
    priority: str = "medium"
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None
    tags: List[str] = []
    is_completed: bool = False

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class ReminderEventSchema(BaseEventSchema):
    """Schema for reminder events."""
    task_id: int
    user_id: str
    reminder_at: datetime
    due_date: Optional[datetime] = None
    title: str

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class UISyncEventSchema(BaseEventSchema):
    """Schema for UI synchronization events."""
    task_id: int
    user_id: str
    action: str
    payload: Dict[str, Any]

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


# Convenience functions for creating events
def create_task_event(event_type: EventType, task_data: Dict[str, Any]) -> TaskEventSchema:
    """Create a task event from task data."""
    return TaskEventSchema(
        event_type=event_type,
        task_id=task_data.get('id'),
        user_id=str(task_data.get('user_id')),
        title=task_data.get('title'),
        priority=task_data.get('priority', 'medium'),
        due_date=task_data.get('due_date'),
        reminder_at=task_data.get('reminder_at'),
        tags=task_data.get('tags', []),
        is_completed=task_data.get('is_completed', False)
    )


def create_reminder_event(task_data: Dict[str, Any]) -> ReminderEventSchema:
    """Create a reminder event from task data."""
    return ReminderEventSchema(
        event_type=EventType.REMINDER_SET,
        task_id=task_data.get('id'),
        user_id=str(task_data.get('user_id')),
        reminder_at=task_data['reminder_at'],  # This should exist for reminder events
        due_date=task_data.get('due_date'),
        title=task_data.get('title')
    )


def create_ui_sync_event(action: str, task_data: Dict[str, Any]) -> UISyncEventSchema:
    """Create a UI sync event from task data."""
    return UISyncEventSchema(
        event_type=EventType.TASK_SYNC,
        task_id=task_data.get('id'),
        user_id=str(task_data.get('user_id')),
        action=action,
        payload={
            'id': task_data.get('id'),
            'title': task_data.get('title'),
            'is_completed': task_data.get('is_completed', False),
            'due_date': task_data.get('due_date'),
            'updated_at': task_data.get('updated_at')
        }
    )