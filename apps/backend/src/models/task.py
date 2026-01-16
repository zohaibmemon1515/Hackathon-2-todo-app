from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid


# ------------------ BASE ------------------
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = None
    priority: str = Field(default="medium", regex="^(low|medium|high)$")


# ------------------ DB MODEL ------------------
class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)  # auto-increment integer ID

    user_id: uuid.UUID = Field(
        foreign_key="user.id",
        index=True
    )

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # relationship
    user: Optional["User"] = Relationship(back_populates="tasks")

    def to_dict(self):
        """Convert task to dictionary for easy serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_completed": self.is_completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "user_id": str(self.user_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


# ------------------ SCHEMAS ------------------
class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int  # integer task ID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default=None, regex="^(low|medium|high)$")


class TaskPatch(TaskUpdate):
    pass
