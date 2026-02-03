import structlog
import logging
import os
from datetime import datetime


def configure_logger():
    """Configure structured logging for the audit service."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Set up basic logging configuration
    logging.basicConfig(
        format="%(message)s",
        level=os.environ.get("LOG_LEVEL", "INFO"),
    )


def get_logger():
    """Get a configured logger instance."""
    return structlog.get_logger()


# Initialize logger configuration
configure_logger()