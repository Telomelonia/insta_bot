"""
File Utility Module

This module provides utility functions for file operations.
"""

import os
import shutil
import logging

logger = logging.getLogger(__name__)

def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path (str): Path to the directory to check/create
        
    Returns:
        bool: True if the directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory_path}: {e}", exc_info=True)
        return False

def safe_delete_directory(directory_path):
    """
    Safely delete a directory and all its contents.
    
    Args:
        directory_path (str): Path to the directory to delete
        
    Returns:
        bool: True if the directory was deleted, False otherwise
    """
    try:
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
        return True
    except Exception as e:
        logger.error(f"Failed to delete directory {directory_path}: {e}", exc_info=True)
        return False

def get_file_size_mb(file_path):
    """
    Get the size of a file in megabytes.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        float: Size of the file in MB, or -1 if the file doesn't exist
    """
    try:
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)  # Convert to MB
        return -1
    except Exception as e:
        logger.error(f"Failed to get file size for {file_path}: {e}", exc_info=True)
        return -1

def list_files_with_extension(directory_path, extension):
    """
    List all files with a specific extension in a directory.
    
    Args:
        directory_path (str): Path to the directory to search
        extension (str): File extension to search for (e.g., '.html')
        
    Returns:
        list: List of file paths with the specified extension
    """
    try:
        if not os.path.exists(directory_path):
            return []
            
        file_list = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith(extension.lower()):
                    file_list.append(os.path.join(root, file))
        return file_list
    except Exception as e:
        logger.error(f"Failed to list files in {directory_path}: {e}", exc_info=True)
        return []