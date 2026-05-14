"""
Logging Configuration
Structured logging with rotating files and console output.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from app.config.settings import get_settings

# ANSI color codes
COLORS = {
    'DEBUG': '\033[36m',      # Cyan
    'INFO': '\033[32m',       # Green
    'WARNING': '\033[33m',    # Yellow
    'ERROR': '\033[31m',      # Red
    'CRITICAL': '\033[35m',   # Magenta
    'RESET': '\033[0m'
}


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support."""

    FORMAT_CONSOLE = (
        '%(asctime)s - '
        '%(name)s - '
        '%(levelname)s - '
        '%(message)s'
    )

    FORMAT_FILE = (
        '%(asctime)s - '
        '%(name)s - '
        '%(levelname)s - '
        '%(filename)s:%(lineno)d - '
        '%(funcName)s() - '
        '%(message)s'
    )

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors for console output."""
        if record.levelname in COLORS:
            record.levelname = f"{COLORS[record.levelname]}{record.levelname}{COLORS['RESET']}"
        
        if hasattr(self, '_style') and '_fmt' in dir(self._style):
            return super().format(record)
        return logging.Formatter.format(self, record)


def setup_logging() -> None:
    """
    Configure application-wide logging.
    Creates rotating file handlers and colored console output.
    """
    settings = get_settings()
    
    # Create logs directory if it doesn't exist
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console Handler (colored output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level)
    console_formatter = ColoredFormatter(ColoredFormatter.FORMAT_CONSOLE)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File Handler (rotating, with full details)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=settings.log_file,
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count
    )
    file_handler.setLevel(settings.log_level)
    file_formatter = logging.Formatter(ColoredFormatter.FORMAT_FILE)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Configure specific loggers
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    root_logger.info(
        f"Logging configured: level={settings.log_level}, "
        f"file={settings.log_file}, "
        f"environment={settings.environment}"
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)


class StructuredLogger:
    """
    Wrapper for structured logging with contextual information.
    Useful for adding context to log messages.
    """

    def __init__(self, name: str, **context):
        """
        Initialize structured logger.
        
        Args:
            name: Logger name
            **context: Context key-value pairs
        """
        self.logger = get_logger(name)
        self.context = context

    def _format_message(self, message: str) -> str:
        """Format message with context."""
        if self.context:
            context_str = " | ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{message} [{context_str}]"
        return message

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with context."""
        self.logger.debug(self._format_message(message), **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message with context."""
        self.logger.info(self._format_message(message), **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with context."""
        self.logger.warning(self._format_message(message), **kwargs)

    def error(self, message: str, exc_info: bool = False, **kwargs) -> None:
        """Log error message with context."""
        self.logger.error(self._format_message(message), exc_info=exc_info, **kwargs)

    def critical(self, message: str, exc_info: bool = False, **kwargs) -> None:
        """Log critical message with context."""
        self.logger.critical(self._format_message(message), exc_info=exc_info, **kwargs)

    def add_context(self, **context) -> None:
        """Add additional context."""
        self.context.update(context)


# Module-level logger
logger = get_logger(__name__)
