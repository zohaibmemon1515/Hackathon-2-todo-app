from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class NotificationEvent(BaseModel):
    """Model for notification events"""

    event_type: str
    task_id: int                         # Kafka sends int
    user_id: str
    reminder_at: datetime
    title: str                       # Map from message['title']
    timestamp: datetime
    payload: Optional[Dict[str, Any]] = None  # Optional field, default None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Factory to map Kafka message fields to model"""
        return cls(
            event_type=data["event_type"],
            task_id=data["task_id"],
            user_id=data["user_id"],
            reminder_at=data.get("reminder_at") or data.get("reminder_at_str"),
            title=data.get("title", "No Title"),  # Map 'title' -> task_title
            timestamp=data["timestamp"],
            payload=data.get("payload"),
        )


class NotificationLogEntry(BaseModel):
    """Model for notification log entries"""

    log_id: str = str(uuid.uuid4())
    notification_event: NotificationEvent
    delivery_status: str  # "attempted", "failed", "delivered"
    delivery_timestamp: datetime = datetime.now()
    error_message: Optional[str] = None
