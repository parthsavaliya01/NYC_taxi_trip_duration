"""
Logging configuration for NYC Taxi application.

Sets up structured logging with file and console handlers.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from app.core.config import settings


def setup_logging(
    logger_name: str,
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logger with file and console handlers.
    
    Args:
        logger_name: Name of the logger.
        level: Logging level (uses settings default if not provided).
        log_file: Path to log file (uses settings default if not provided).
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(logger_name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    level = level or settings.logging.level
    log_file = log_file or settings.logging.log_file
    
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(settings.logging.format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if path provided)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(settings.logging.format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger
