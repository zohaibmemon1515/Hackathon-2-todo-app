import unittest
from datetime import datetime
from src.models.notification_event import NotificationEvent, NotificationLogEntry


class TestNotificationService(unittest.TestCase):
    def test_notification_event_creation(self):
        """Test that NotificationEvent can be properly created."""
        event_data = {
            "event_type": "reminder.set",
            "task_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "123e4567-e89b-12d3-a456-426614174001",
            "reminder_time": datetime.now(),
            "task_title": "Test Task",
            "timestamp": datetime.now(),
            "payload": {"test": "data"}
        }

        event = NotificationEvent(**event_data)
        self.assertEqual(event.event_type, "reminder.set")
        self.assertEqual(event.task_id, "123e4567-e89b-12d3-a456-426614174000")

    def test_notification_log_entry_creation(self):
        """Test that NotificationLogEntry can be properly created."""
        event_data = {
            "event_type": "reminder.set",
            "task_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "123e4567-e89b-12d3-a456-426614174001",
            "reminder_time": datetime.now(),
            "task_title": "Test Task",
            "timestamp": datetime.now(),
            "payload": {"test": "data"}
        }

        notification_event = NotificationEvent(**event_data)
        log_entry = NotificationLogEntry(
            notification_event=notification_event,
            delivery_status="attempted"
        )

        self.assertEqual(log_entry.delivery_status, "attempted")
        self.assertEqual(log_entry.notification_event.task_id, notification_event.task_id)


if __name__ == '__main__':
    unittest.main()