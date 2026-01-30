from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

# ------------------ TASK-TAG LINK MODEL ------------------
class TaskTagLink(SQLModel, table=True):
    __tablename__ = "task_tag_link"  # Match migration table name

    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tag.id", primary_key=True)

# ------------------ TAG MODEL ------------------
class TagBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    user_id: uuid.UUID = Field(index=True)

class Tag(TagBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    color: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship with tasks through TaskTagLink
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)

    class Config:
        arbitrary_types_allowed = True

# ------------------ TASK BASE ------------------
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = None
    priority: str = Field(default="medium", regex="^(low|medium|high)$")
    reminder_at: Optional[datetime] = None
    

# ------------------ TASK MODEL ------------------
class Task(TaskBase, table=True):
    __tablename__ = "task"  # Explicit table name

    id: int = Field(default=None, primary_key=True)  # auto-increment integer ID
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTagLink)

    def to_dict(self):
        """Convert task to dictionary for easy serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_completed": self.is_completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "reminder_at": self.reminder_at.isoformat() if self.reminder_at else None,
            "user_id": str(self.user_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

# ------------------ TASK SCHEMAS ------------------
class TaskCreate(TaskBase):
    tags: Optional[List[str]] = []  # Include tags in creation

class TaskRead(TaskBase):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[str]] = []

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default=None, regex="^(low|medium|high)$")
    reminder_at: Optional[datetime] = None
    tags: Optional[List[str]] = None  # Include tags in update

class TaskPatch(TaskUpdate):
    pass

# ------------------ Fix forward references ------------------
Task.update_forward_refs()
Tag.update_forward_refs()
