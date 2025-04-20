"""Utility functions for aish."""

import logging
from pathlib import Path


def setup_logging() -> logging.Logger:
    """Set up logging configuration.
    
    Returns:
        A configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path.home() / ".aish" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "aish.log"),
            logging.StreamHandler(),
        ],
    )
    
    return logging.getLogger("aish") 