from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List
import uuid

class EnhancedCommandBase(SQLModel):
    command_pattern: str  # regex pattern for the command
    command_type: str     # check_tasks, set_reminder, etc.
    language_support: Optional[str] = Field(default='["en"]')  # JSON string of supported languages
    multi_step_sequence: Optional[str] = Field(default="default")  # sequence to execute like "create_schedule_notify"
    is_active: bool = Field(default=True)


class EnhancedCommand(EnhancedCommandBase, table=True):
    """
    Represents an enhanced command pattern that extends the AI agent's capabilities.
    Stores command patterns, supported languages, and associated multi-step sequences.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<EnhancedCommand(id={self.id}, command_type={self.command_type})>"

    @property
    def supported_languages(self) -> List[str]:
        """Parse the language_support JSON string into a list of languages."""
        import json
        try:
            return json.loads(self.language_support or '["en"]')
        except:
            return ["en"]