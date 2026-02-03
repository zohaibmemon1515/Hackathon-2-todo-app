from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class EnhancedCommandBase(BaseModel):
    command_pattern: str  # regex pattern for the command
    command_type: str     # check_tasks, set_reminder, etc.
    language_support: Optional[List[str]] = ["en"]  # supported languages like ["en", "ur"]
    multi_step_sequence: Optional[str] = "default"  # sequence to execute like "create_schedule_notify"


class EnhancedCommandCreate(EnhancedCommandBase):
    pass


class EnhancedCommandUpdate(BaseModel):
    command_pattern: Optional[str] = None
    command_type: Optional[str] = None
    language_support: Optional[List[str]] = None
    multi_step_sequence: Optional[str] = None
    is_active: Optional[bool] = None


class EnhancedCommandResponse(EnhancedCommandBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True