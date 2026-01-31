import logging
from datetime import datetime
import json
from typing import Dict, Any


class StructuredLogger:
    """
    A structured logger for application events including Kafka events
    """

    def __init__(self):
        self.app_logger = logging.getLogger("app")
        self.event_logger = logging.getLogger("events")

        # Setup app logger if not already configured
        if not self.app_logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.app_logger.addHandler(handler)
            self.app_logger.setLevel(logging.INFO)

        # Setup event logger for structured event logging
        if not self.event_logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.event_logger.addHandler(handler)
            self.event_logger.setLevel(logging.INFO)

    def log_kafka_event_published(self, topic: str, event_type: str, task_id: int, user_id: str):
        """Log when a Kafka event is published"""
        log_entry = {
            "event": "kafka_event_published",
            "timestamp": datetime.utcnow().isoformat(),
            "topic": topic,
            "event_type": event_type,
            "task_id": task_id,
            "user_id": user_id
        }
        self.event_logger.info(json.dumps(log_entry))

    def log_kafka_event_failed(self, topic: str, event_type: str, error_message: str):
        """Log when a Kafka event publishing fails"""
        log_entry = {
            "event": "kafka_event_failed",
            "timestamp": datetime.utcnow().isoformat(),
            "topic": topic,
            "event_type": event_type,
            "error": error_message
        }
        self.event_logger.error(json.dumps(log_entry))

    def log_kafka_connection_status(self, status: str, details: Dict[str, Any] = None):
        """Log Kafka connection status changes"""
        log_entry = {
            "event": "kafka_connection_status",
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "details": details or {}
        }
        self.event_logger.info(json.dumps(log_entry))

    def log_performance_metric(self, operation: str, duration_ms: float, details: Dict[str, Any] = None):
        """Log performance metrics for operations"""
        log_entry = {
            "event": "performance_metric",
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "duration_ms": duration_ms,
            "details": details or {}
        }
        self.event_logger.info(json.dumps(log_entry))


class SecurityLogger:
    """
    A security-focused logger for sensitive operations
    """

    def __init__(self):
        self.logger = logging.getLogger("security")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def log_auth_attempt(self, email: str, success: bool, ip_address: str = None, user_agent: str = None):
        """Log authentication attempts for security monitoring"""
        self.logger.info(f"AUTH_ATTEMPT - Email: {email}, Success: {success}, IP: {ip_address}, User-Agent: {user_agent}")

    def log_sensitive_operation(self, operation: str, user_id: str, details: Dict[str, Any] = None):
        """Log sensitive operations for audit trail"""
        self.logger.info(f"SENSITIVE_OP - Operation: {operation}, User: {user_id}, Details: {details}")

    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events"""
        self.logger.warning(f"SECURITY_EVENT - Type: {event_type}, Details: {details}")

    def log_tool_usage(self, user_id: str, tool_name: str, success: bool, details: Dict[str, Any] = None):
        """Log tool usage for audit purposes"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "tool_name": tool_name,
            "success": success,
            "details": details or {}
        }
        self.logger.info(f"TOOL_USAGE - {json.dumps(log_entry)}")


# Initialize loggers
structured_logger = StructuredLogger()
security_logger = SecurityLogger()


def setup_logging():
    """
    Setup application logging
    """
    # Setup general logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Return loggers
    return structured_logger, security_logger


def get_structured_logger():
    """
    Get the structured logger instance
    """
    return structured_logger


def get_security_logger():
    """
    Get the security logger instance
    """
    return security_logger