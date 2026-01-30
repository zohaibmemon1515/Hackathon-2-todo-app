from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    # Fields added by migration
    reminder_at: Optional[datetime] = None
    # Additional fields for advanced features
    tags: Optional[List[str]] = []


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[str]] = []

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")
    reminder_at: Optional[datetime] = None
    tags: Optional[List[str]] = None  # Include tags in update


class TaskPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")
    reminder_at: Optional[datetime] = None
    tags: Optional[List[str]] = None  # Include tags in patch


class TaskListResponse(BaseModel):
    tasks: list[TaskRead]
    total: int
    limit: int
    offset: int