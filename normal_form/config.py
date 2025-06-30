"""
Configuration and logging setup for Nash Equilibrium Finder
"""

import logging
import os

# Default configuration
DEFAULT_CONFIG = {
    "precision": 6,
    "tolerance": 1e-6,
    "max_iterations": 1000,
    "random_seed": None,
    "output_format": "text",
    "log_level": "INFO",
}


def setup_logging(level: str = "INFO", log_file: str = None):
    """Setup logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(level=getattr(logging, level.upper()), format=log_format, handlers=handlers)


def get_config():
    """Get configuration from environment variables or defaults."""
    config = DEFAULT_CONFIG.copy()

    # Override with environment variables if present
    if "NASH_PRECISION" in os.environ:
        config["precision"] = int(os.environ["NASH_PRECISION"])

    if "NASH_TOLERANCE" in os.environ:
        config["tolerance"] = float(os.environ["NASH_TOLERANCE"])

    if "NASH_LOG_LEVEL" in os.environ:
        config["log_level"] = os.environ["NASH_LOG_LEVEL"]

    return config


def get_logger(name: str):
    """Get a logger instance."""
    return logging.getLogger(name)
