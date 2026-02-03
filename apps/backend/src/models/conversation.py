from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import json
from sqlalchemy import Column, Text


class ConversationBase(SQLModel):
    user_id: str
    title: Optional[str] = Field(default=None)


class Conversation(ConversationBase, table=True):
    """
    Represents a persistent conversation session between a user and the AI chatbot,
    containing metadata like creation time and user association.
    """
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Renamed from 'metadata' to avoid SQLAlchemy reserved name
    metadata_field: Optional[str] = Field(
        default="{}",
        sa_column=Column("metadata", Text, nullable=False)
    )  # JSON string for AI context, language preference, etc.

    active_context: Optional[str] = Field(
        default="{}",
        sa_column=Column(Text, nullable=False)
    )  # JSON string for current conversation context

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id})>"

    @property
    def parsed_metadata(self) -> dict:
        try:
            return json.loads(self.metadata_field or "{}")
        except json.JSONDecodeError:
            return {}

    @property
    def parsed_active_context(self) -> dict:
        try:
            return json.loads(self.active_context or "{}")
        except json.JSONDecodeError:
            return {}
