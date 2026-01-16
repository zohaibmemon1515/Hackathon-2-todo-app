from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")


class TaskPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")


class TaskListResponse(BaseModel):
    tasks: list[TaskRead]
    total: int
    limit: int
    offset: int