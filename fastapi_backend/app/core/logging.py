"""Structured logging configuration using structlog."""

import logging
import sys
import uuid

import structlog
from structlog.types import EventDict, Processor

from app.config import settings


def add_request_id(logger, method_name: str, event_dict: EventDict) -> EventDict:
    """Add or generate request_id for tracing."""
    request_id = event_dict.get("request_id")
    if not request_id:
        request_id = str(uuid.uuid4())
    event_dict["request_id"] = request_id
    return event_dict


def rename_level(logger, method_name: str, event_dict: EventDict) -> EventDict:
    """Rename 'level' to 'severity' for better compatibility."""
    event_dict["severity"] = event_dict.pop("level", "info")
    return event_dict


def configure_logging() -> None:
    """Configure structlog for JSON output to stdout."""
    log_level = getattr(settings, "LOG_LEVEL", "INFO").upper()

    # Configure standard logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level, logging.INFO),
    )

    # Mute uvicorn's standard handlers to prevent double logging
    # and ensure they go through structlog if we want them to
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = True

    # Configure structlog with JSON processor
    processors: list[Processor] = [
        # Add log level
        structlog.stdlib.add_log_level,
        # Add timestamp
        structlog.processors.TimeStamper(fmt="iso"),
        # Add logger name
        structlog.stdlib.add_logger_name,
        # Process position info
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            ]
        ),
        # Format as JSON
        structlog.processors.JSONRenderer(),
    ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)
