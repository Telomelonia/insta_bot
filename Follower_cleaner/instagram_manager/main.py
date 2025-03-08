#!/usr/bin/env python3
"""
Instagram Account Manager
=========================
A tool for managing your Instagram account data.

This application allows you to:
- Analyze your Instagram data export
- View pending follow requests
- Identify users you follow who don't follow you back

Author: Your Name
License: MIT
"""

import sys
import tkinter as tk
from instagram_manager.ui.app import InstagramManagerApp
from instagram_manager.utils.logger import setup_logger

def main():
    """Main entry point for the application."""
    # Setup logging
    logger = setup_logger()
    logger.info("Starting Instagram Account Manager")
    
    try:
        # Initialize the Tkinter application
        root = tk.Tk()
        app = InstagramManagerApp(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)
    
    logger.info("Application closed successfully")

if __name__ == "__main__":
    main()