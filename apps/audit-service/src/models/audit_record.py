from pydantic import BaseModel, model_validator
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import os
import json


class TaskEvent(BaseModel):
    """Model for task events"""
    event_type: str
    task_id: str  # will coerce int -> str automatically
    user_id: str
    timestamp: datetime
    previous_state: Optional[Dict[str, Any]] = None
    new_state: Optional[Dict[str, Any]] = None
    payload: Optional[Dict[str, Any]] = None

    @model_validator(mode="before")
    def coerce_types_and_defaults(cls, values: dict) -> dict:
        # Ensure task_id is string
        if "task_id" not in values or values["task_id"] is None:
            raise ValueError("Missing required field: task_id")
        values["task_id"] = str(values["task_id"])

        # Ensure payload exists
        if "payload" not in values or values["payload"] is None:
            values["payload"] = {}

        return values


class AuditRecord(BaseModel):
    """Model for audit records"""
    record_id: str
    event_type: str
    task_id: str
    user_id: str
    timestamp: datetime
    payload: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None

    def __init__(self, **data):
        if "record_id" not in data:
            data["record_id"] = str(uuid.uuid4())
        super().__init__(**data)


class AuditService:
    """Service for handling audit record storage"""

    def __init__(self, log_file_path: str = "./audit_logs/audit.log"):
        self.log_file_path = log_file_path
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    def save_audit_record(self, audit_record: AuditRecord):
        """Save an audit record to file (append-only)"""
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_record.dict(), default=str) + "\n")
        except Exception as e:
            raise Exception(f"Failed to save audit record: {str(e)}")

    def create_audit_record_from_task_event(self, task_event: TaskEvent) -> AuditRecord:
        """Convert TaskEvent -> AuditRecord"""
        return AuditRecord(
            event_type=task_event.event_type,
            task_id=task_event.task_id,
            user_id=task_event.user_id,
            timestamp=task_event.timestamp,
            payload=task_event.payload
        )
