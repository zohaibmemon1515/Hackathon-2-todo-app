from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import json
from sqlalchemy import Column, Text

class MessageBase(SQLModel):
    user_id: str
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str  # "user", "assistant"
    content: str

    # Enhanced fields for language support
    original_content: Optional[str] = Field(default=None)  # Original input before processing (e.g., Urdu)
    processed_content: Optional[str] = Field(default=None)  # Processed content (e.g., translated to English)
    language_detected: Optional[str] = Field(default=None)  # Detected language like "en", "ur"
    command_metadata: Optional[str] = Field(default="{}", sa_column=Column(Text, nullable=False))  # Command-specific metadata as JSON string

    # Stored as TEXT in DB, always JSON string
    extra_info: Optional[str] = Field(
        default="{}",
        sa_column=Column(Text, nullable=False),
        alias="metadata"
    )


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<Message id={self.id} role={self.role}>"

    @property
    def parsed_metadata(self) -> dict:
        try:
            return json.loads(self.extra_info or "{}")
        except json.JSONDecodeError:
            return {}
