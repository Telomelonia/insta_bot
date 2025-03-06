"""
Non-Followers Tab View Module

This module handles the UI for the non-followers tab.
"""

import tkinter as tk
import webbrowser
import logging
from tkinter import ttk

logger = logging.getLogger(__name__)

class NonFollowersTabView:
    """
    View class for the non-followers tab.
    
    This class manages displaying and interacting with the list of
    users who don't follow you back.
    """
    
    def __init__(self, parent, data_parser, status_var):
        """
        Initialize the non-followers tab view.
        
        Args:
            parent (ttk.Frame): Parent frame for this view
            data_parser (InstagramDataParser): The data parser instance with user data
            status_var (tk.StringVar): Status bar variable for displaying messages
        """
        self.parent = parent
        self.data_parser = data_parser
        self.status_var = status_var
        
        logger.debug("Initializing NonFollowersTabView")
        
        # Initialize empty UI
        self.tree = None
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI elements for the non-followers tab."""
        # Header
        ttk.Label(self.parent, text="Users You Follow Who Don't Follow You Back", 
                 style="Subheader.TLabel").grid(row=0, column=0, 
                                              sticky=tk.W, pady=(0, 10), 
                                              columnspan=4)
        
        # Create Treeview for non-followers
        columns = ("Username", "URL", "Actions")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        
        self.tree.heading("Username", text="Username")
        self.tree.heading("URL", text="Profile URL")
        self.tree.heading("Actions", text="Actions")
        
        self.tree.column("Username", width=200)
        self.tree.column("URL", width=350)
        self.tree.column("Actions", width=150)
        
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Add action buttons (commented out for now as they're not implemented)
        # ttk.Button(self.parent, text="Unfollow Selected", 
        #            command=self._unfollow_selected).grid(row=2, column=0, pady=10, padx=(0, 5))
        # ttk.Button(self.parent, text="Unfollow All", 
        #            command=self._unfollow_all).grid(row=2, column=1, pady=10, padx=5)
        
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
            if column == "#2":  # URL column
                item = self.tree.identify_row(event.y)
                if not item:
                    return
                    
                values = self.tree.item(item, "values")
                if not values or len(values) < 2:
                    return
                    
                url = values[1]
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
        
        # Populate treeview with non-followers
        for user in self.data_parser.non_followers:
            self.tree.insert("", "end", values=(
                user["username"],
                user["url"],
                "View Profile"
            ))
        
        logger.info(f"Updated non-followers view with {len(self.data_parser.non_followers)} items")
    
    def _unfollow_selected(self):
        """Unfollow the selected users (not implemented)."""
        # This would be implemented if Instagram had an API to do this
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            username = item["values"][0]
            self.status_var.set(f"Would unfollow {username} (not implemented)")
            logger.info(f"Request to unfollow {username}")
    
    def _unfollow_all(self):
        """Unfollow all non-followers (not implemented)."""
        # This would be implemented if Instagram had an API to do this
        count = len(self.tree.get_children())
        self.status_var.set(f"Would unfollow all {count} non-followers (not implemented)")
        logger.info(f"Request to unfollow all {count} non-followers")