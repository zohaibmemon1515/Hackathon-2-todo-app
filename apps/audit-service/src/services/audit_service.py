import asyncio
from typing import Optional
import structlog
import json
import os
from datetime import datetime

from ..models.audit_record import TaskEvent, AuditRecord, AuditService as AuditStorageService
from ..utils.logger import get_logger


class AuditProcessingService:
    def __init__(self, log_file_path: str = "./audit_logs/audit.log"):
        self.logger = get_logger()
        self.storage_service = AuditStorageService(log_file_path)

    async def process_task_event(self, event_data: dict) -> Optional[AuditRecord]:
        """
        Process a task event and create an audit record.

        Args:
            event_data: Dictionary containing the task event data

        Returns:
            AuditRecord if successful, None otherwise
        """
        try:
            # Create a TaskEvent from the raw data
            task_event = TaskEvent(**event_data)

            # Create an audit record from the task event
            audit_record = self.storage_service.create_audit_record_from_task_event(task_event)

            # Save the audit record to persistent storage
            self.storage_service.save_audit_record(audit_record)

            self.logger.info("Task event processed and audit record saved",
                           record_id=audit_record.record_id,
                           event_type=audit_record.event_type,
                           task_id=audit_record.task_id)

            return audit_record

        except Exception as e:
            self.logger.error("Error processing task event", error=str(e), event_data=event_data)

            # Create an audit record for the error
            error_audit_record = AuditRecord(
                event_type="audit.error",
                task_id=event_data.get('task_id', 'unknown'),
                user_id=event_data.get('user_id', 'unknown'),
                timestamp=datetime.now(),
                payload={
                    "original_event": event_data,
                    "error_message": str(e)
                }
            )

            # Attempt to save the error record
            try:
                self.storage_service.save_audit_record(error_audit_record)
            except Exception as save_error:
                self.logger.error("Failed to save error audit record", error=str(save_error))

            return error_audit_record

    async def handle_malformed_event(self, raw_data: bytes, error: Exception) -> AuditRecord:
        """
        Handle a malformed event by creating an appropriate audit record.

        Args:
            raw_data: The raw event data that caused the error
            error: The exception that occurred during processing

        Returns:
            AuditRecord with error details
        """
        self.logger.error("Malformed event detected",
                         raw_data=raw_data.decode('utf-8', errors='ignore'),
                         error=str(error))

        # Create an audit record for the malformed event
        error_audit_record = AuditRecord(
            event_type="event.malformed",
            task_id="unknown",
            user_id="unknown",
            timestamp=datetime.now(),
            payload={
                "raw_data": raw_data.decode('utf-8', errors='ignore'),
                "error_message": f"Malformed event: {str(error)}"
            }
        )

        # Attempt to save the error record
        try:
            self.storage_service.save_audit_record(error_audit_record)
        except Exception as save_error:
            self.logger.error("Failed to save malformed event audit record", error=str(save_error))

        return error_audit_record

    async def get_audit_records(self, limit: int = 100) -> list:
        """
        Retrieve audit records from storage.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of audit records
        """
        try:
            records = []
            if os.path.exists(self.storage_service.log_file_path):
                with open(self.storage_service.log_file_path, 'r', encoding='utf-8') as log_file:
                    lines = log_file.readlines()[-limit:]  # Get last 'limit' lines
                    for line in lines:
                        if line.strip():  # Skip empty lines
                            record_data = json.loads(line.strip())
                            records.append(AuditRecord(**record_data))

            self.logger.info("Retrieved audit records", count=len(records))
            return records
        except Exception as e:
            self.logger.error("Error retrieving audit records", error=str(e))
            return []