from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class MessageBase(BaseModel):
    user_id: str
    conversation_id: int
    role: str  # "user", "assistant"
    content: str
    original_content: Optional[str] = None  # Original input before processing (e.g., Urdu)
    processed_content: Optional[str] = None  # Processed content (e.g., translated to English)
    language_detected: Optional[str] = None  # Detected language like "en", "ur"
    command_metadata: Optional[Dict[str, Any]] = {}  # Command-specific metadata
    extra_info: Optional[Dict[str, Any]] = {}  # Additional metadata (alias: metadata)


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    original_content: Optional[str] = None
    processed_content: Optional[str] = None
    language_detected: Optional[str] = None
    command_metadata: Optional[Dict[str, Any]] = None
    extra_info: Optional[Dict[str, Any]] = None


class MessageResponse(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True