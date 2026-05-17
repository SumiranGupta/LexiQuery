"""
LexiQuery Logging Configuration
Structured logging with consistent formatting across all modules.
"""

import logging
import sys

LOG_FORMAT = "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a namespaced logger with stdout handler."""
    logger = logging.getLogger(f"lexiquery.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger
