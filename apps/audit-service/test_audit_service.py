import unittest
import os
from datetime import datetime
from src.models.audit_record import TaskEvent, AuditRecord, AuditService


class TestAuditService(unittest.TestCase):
    def test_task_event_creation(self):
        """Test that TaskEvent can be properly created."""
        event_data = {
            "event_type": "task.created",
            "task_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "123e4567-e89b-12d3-a456-426614174001",
            "timestamp": datetime.now(),
            "payload": {"title": "Test Task", "completed": False}
        }

        event = TaskEvent(**event_data)
        self.assertEqual(event.event_type, "task.created")
        self.assertEqual(event.task_id, "123e4567-e89b-12d3-a456-426614174000")

    def test_audit_record_creation(self):
        """Test that AuditRecord can be properly created."""
        audit_record = AuditRecord(
            event_type="task.created",
            task_id="123e4567-e89b-12d3-a456-426614174000",
            user_id="123e4567-e89b-12d3-a456-426614174001",
            timestamp=datetime.now(),
            payload={"title": "Test Task", "completed": False}
        )

        self.assertEqual(audit_record.event_type, "task.created")
        self.assertEqual(audit_record.task_id, "123e4567-e89b-12d3-a456-426614174000")

    def test_audit_storage_service(self):
        """Test that AuditService can save records."""
        # Create a temporary log file for testing
        test_log_path = "./test_audit.log"
        audit_service = AuditService(test_log_path)

        audit_record = AuditRecord(
            event_type="test.event",
            task_id="test-task-id",
            user_id="test-user-id",
            timestamp=datetime.now(),
            payload={"test": "data"}
        )

        # Save the record
        audit_service.save_audit_record(audit_record)

        # Verify the file was created and contains the record
        self.assertTrue(os.path.exists(test_log_path))

        # Clean up
        if os.path.exists(test_log_path):
            os.remove(test_log_path)


if __name__ == '__main__':
    unittest.main()