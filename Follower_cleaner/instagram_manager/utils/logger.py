"""
Logger Module

This module sets up logging for the application.
"""

import os
import logging
from datetime import datetime

def setup_logger(log_level=logging.INFO):
    """
    Set up and configure the application logger.
    
    Args:
        log_level (int): The logging level to use (default: logging.INFO)
        
    Returns:
        logging.Logger: The configured logger
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.expanduser("~"), ".instagram_manager", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"instagram_manager_{timestamp}.log")
    
    # Configure logging
    logger = logging.getLogger("instagram_manager")
    logger.setLevel(log_level)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging started. Log file: {log_file}")
    return logger