import logging
from datetime import datetime
import json
from typing import Dict, Any


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


# Initialize security logger
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

    # Setup security logging
    security_logger = SecurityLogger()

    return security_logger


def get_security_logger():
    """
    Get the security logger instance
    """
    return security_logger