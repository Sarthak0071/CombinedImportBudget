"""Unified logging configuration."""

import logging
import sys


def setup_logging(level: int = logging.INFO, format_type: str = 'standard'):
    """
    Setup unified logging configuration.
    
    Args:
        level: Logging level (logging.INFO, logging.DEBUG, etc.)
        format_type: 'standard' or 'detailed'
    """
    if format_type == 'detailed':
        log_format = '%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s'
    else:
        log_format = '%(levelname)s: %(message)s'
    
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout
    )
    
    # Suppress verbose libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
