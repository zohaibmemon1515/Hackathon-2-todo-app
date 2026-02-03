import json
from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger()


def deserialize_event(message_value: bytes) -> Optional[Dict[str, Any]]:
    """
    Deserialize a Kafka message value from JSON bytes to dictionary.

    Args:
        message_value: Raw bytes from Kafka message

    Returns:
        Deserialized event dictionary or None if deserialization fails
    """
    try:
        event_dict = json.loads(message_value.decode('utf-8'))
        return event_dict
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error("Failed to deserialize event", error=str(e))
        return None


def validate_reminder_event(event: Dict[str, Any]) -> bool:
    """
    Validate that an event is a proper reminder event.
    """
    required_fields = ['event_type', 'task_id', 'user_id', 'reminder_at', 'timestamp']  # <- notice reminder_at

    for field in required_fields:
        if field not in event:
            logger.error(f"Missing required field in reminder event: {field}")
            return False

    if event['event_type'] != 'reminder.set':
        logger.error(f"Invalid event type for reminder consumer: {event['event_type']}")
        return False

    return True

