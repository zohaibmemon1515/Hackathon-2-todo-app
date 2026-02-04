from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class CommandMappingBase(SQLModel):
    original_command: str  # English command pattern
    urdu_equivalent: Optional[str] = Field(default=None)  # Roman Urdu equivalent
    agent_tool_id: Optional[str] = Field(default=None)  # Reference to agent tool
    is_active: bool = Field(default=True)


class CommandMapping(CommandMappingBase, table=True):
    """
    Maps command patterns between different languages (English and Urdu)
    and associates them with specific agent tools for processing.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<CommandMapping(id={self.id}, original='{self.original_command}')>"

    @property
    def has_urdu_equivalent(self) -> bool:
        """Check if this command mapping has a Roman Urdu equivalent."""
        return bool(self.urdu_equivalent and self.urdu_equivalent.strip())