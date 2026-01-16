from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


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

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id})>"