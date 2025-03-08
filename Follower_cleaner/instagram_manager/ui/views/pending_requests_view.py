"""
Pending Requests Tab View Module

This module handles the UI for the pending follow requests tab.
"""

import tkinter as tk
import webbrowser
import logging
from tkinter import ttk

logger = logging.getLogger(__name__)

class PendingRequestsTabView:
    """
    View class for the pending follow requests tab.
    
    This class manages displaying and interacting with the list of
    follow requests that you've sent to other users.
    """
    
    def __init__(self, parent, data_parser, status_var):
        """
        Initialize the pending requests tab view.
        
        Args:
            parent (ttk.Frame): Parent frame for this view
            data_parser (InstagramDataParser): The data parser instance with request data
            status_var (tk.StringVar): Status bar variable for displaying messages
        """
        self.parent = parent
        self.data_parser = data_parser
        self.status_var = status_var
        
        logger.debug("Initializing PendingRequestsTabView")
        
        # Initialize empty UI
        self.tree = None
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI elements for the pending requests tab."""
        # Header
        ttk.Label(self.parent, text="Pending Follow Requests You've Sent", 
                 style="Subheader.TLabel").grid(row=0, column=0, 
                                              sticky=tk.W, pady=(0, 10), 
                                              columnspan=4)
        
        # Create Treeview for pending requests
        columns = ("Username", "Date", "URL")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        
        self.tree.heading("Username", text="Username")
        self.tree.heading("Date", text="Date Sent")
        self.tree.heading("URL", text="Profile URL")
        
        self.tree.column("Username", width=200)
        self.tree.column("Date", width=200)
        self.tree.column("URL", width=300)
        
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Make the treeview expandable
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_columnconfigure(2, weight=1)
        self.parent.grid_columnconfigure(3, weight=1)
        
        # Add binding for clickable URL
        self.tree.bind("<ButtonRelease-1>", self._on_treeview_click)
    
    def _on_treeview_click(self, event):
        """
        Handle clicks on the treeview to open URLs.
        
        Args:
            event (tk.Event): The click event
        """
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#3":  # URL column
                item = self.tree.identify_row(event.y)
                if not item:
                    return
                    
                values = self.tree.item(item, "values")
                if not values or len(values) < 3:
                    return
                    
                url = values[2]
                if url:
                    logger.info(f"Opening URL: {url}")
                    webbrowser.open(url)
                    self.status_var.set(f"Opening {url}")
                else:
                    self.status_var.set("No URL available")
    
    def update_view(self):
        """Update the view with the latest data from the data parser."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Populate treeview with pending requests
        for request in self.data_parser.pending_sent_requests:
            self.tree.insert("", "end", values=(
                request["username"],
                request["timestamp"],
                request["url"]
            ))
        
        logger.info(f"Updated pending requests view with {len(self.data_parser.pending_sent_requests)} items")