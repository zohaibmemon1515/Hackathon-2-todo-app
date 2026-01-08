from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List
from datetime import datetime
from sqlalchemy import DateTime, String
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """
    User database model
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """
    Schema for creating a new user
    """
    password: str


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information)
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """
    Schema for updating user information
    """
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None