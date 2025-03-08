"""
Instagram Manager App UI Module

This module contains the main application UI class for the Instagram Manager.
"""

import os
import tkinter as tk
import webbrowser
import logging
import threading
from tkinter import ttk, filedialog, messagebox

from instagram_manager.models.data_parser import InstagramDataParser
from instagram_manager.ui.views.requests_view import RequestsTabView
from instagram_manager.ui.views.pending_requests_view import PendingRequestsTabView
from instagram_manager.ui.views.non_followers_view import NonFollowersTabView

logger = logging.getLogger(__name__)

class InstagramManagerApp:
    """
    Main application class for the Instagram Account Manager.
    
    This class creates and manages the main UI window and tabs.
    """
    
    def __init__(self, root):
        """
        Initialize the application with the Tkinter root window.
        
        Args:
            root (tk.Tk): The root Tkinter window
        """
        self.root = root
        self.root.title("Instagram Account Manager")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Set app icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "instagram_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Setup styles
        self._setup_styles()
        
        # Initialize data parser
        self.data_parser = InstagramDataParser()
        
        # Variables
        self.zip_path = tk.StringVar()
        self.extract_dir = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0.0)
        
        # Create UI elements
        self._create_ui()
        
        logger.info("Application UI initialized")
    
    def _setup_styles(self):
        """Configure ttk styles for the application."""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", background="#4e4edd", foreground="white", font=("Arial", 10))
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("Subheader.TLabel", font=("Arial", 12))
    
    def _create_ui(self):
        """Create the application UI elements."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="Instagram Account Manager", style="Header.TLabel").pack(side=tk.LEFT)
        
        # File selection section
        self._create_file_section(main_frame)
        
        # Progress and status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        progress_bar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, 
                                      length=100, mode='determinate', 
                                      variable=self.progress_var)
        progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tab frames
        self.requests_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.requests_frame, text="Follow Requests")
        
        self.pending_requests_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.pending_requests_frame, text="Pending Requests")
        
        self.non_followers_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.non_followers_frame, text="Non-Followers")
        
        # Initialize tab views
        self.requests_view = RequestsTabView(self.requests_frame, self.data_parser, self.status_var)
        self.pending_requests_view = PendingRequestsTabView(self.pending_requests_frame, self.data_parser, self.status_var)
        self.non_followers_view = NonFollowersTabView(self.non_followers_frame, self.data_parser, self.status_var)
    
    def _create_file_section(self, parent):
        """
        Create the file selection and import section.
        
        Args:
            parent (ttk.Frame): Parent frame to add the section to
        """
        file_frame = ttk.LabelFrame(parent, text="Data Import", padding=10)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Select Instagram data export (.zip):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.zip_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(file_frame, text="Browse", command=self.browse_zip).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="Warning: Make sure to download HTML files, not JSON,\nfrom Instagram's Download Your Information page").grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        ttk.Button(file_frame, text="Import Data", command=self.import_data).grid(row=2, column=0, columnspan=3, pady=10)
    
    def browse_zip(self):
        """Browse for Instagram data zip file."""
        file_path = filedialog.askopenfilename(
            title="Select Instagram Data Export",
            filetypes=[("ZIP files", "*.zip")]
        )
        if file_path:
            self.zip_path.set(file_path)
            # Set default extract directory to same location as zip
            default_extract = os.path.join(os.path.dirname(file_path), "instagram_data_extracted")
            self.extract_dir.set(default_extract)
            logger.info(f"Selected zip file: {file_path}")
    
    def import_data(self):
        """Import and process Instagram data."""
        if not self.zip_path.get():
            messagebox.showerror("Error", "Please select an Instagram data export ZIP file")
            return
        
        # Create extract directory if it doesn't exist
        if not self.extract_dir.get():
            self.extract_dir.set(os.path.join(os.path.dirname(self.zip_path.get()), "instagram_data_extracted"))
        
        if not os.path.exists(self.extract_dir.get()):
            os.makedirs(self.extract_dir.get())
        
        # Extract and process in a separate thread
        threading.Thread(target=self._process_data, daemon=True).start()
    
    def _process_data(self):
        """Background process to extract and parse Instagram data."""
        try:
            self.status_var.set("Extracting zip file...")
            self.progress_var.set(10)
            
            # Extract zip
            success = self.data_parser.extract_zip(self.zip_path.get(), self.extract_dir.get())
            if not success:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to extract ZIP file"))
                self.status_var.set("Error extracting data")
                return
            
            self.progress_var.set(30)
            self.status_var.set("Processing follow requests received...")
            
            # Find and process HTML files
            connections_dir = os.path.join(self.extract_dir.get(), "connections", "followers_and_following")
            
            # Parse follow requests
            follow_requests_path = os.path.join(connections_dir, "follow_requests_you've_received.html")
            if os.path.exists(follow_requests_path):
                self.data_parser.parse_follow_requests(follow_requests_path)
            else:
                logger.warning(f"Follow requests file not found: {follow_requests_path}")
            
            self.progress_var.set(40)
            self.status_var.set("Processing pending follow requests sent...")
            
            # Parse pending follow requests sent
            pending_sent_path = os.path.join(connections_dir, "pending_follow_requests.html")
            if os.path.exists(pending_sent_path):
                self.data_parser.parse_pending_sent_requests(pending_sent_path)
            else:
                logger.warning(f"Pending requests file not found: {pending_sent_path}")
                # Try to find the file in a different location
                for root, dirs, files in os.walk(self.extract_dir.get()):
                    if "pending_follow_requests.html" in files:
                        pending_sent_path = os.path.join(root, "pending_follow_requests.html")
                        self.data_parser.parse_pending_sent_requests(pending_sent_path)
                        logger.info(f"Found pending requests file at: {pending_sent_path}")
                        break
            
            self.progress_var.set(50)
            self.status_var.set("Processing followers...")
            
            # Parse followers
            followers_path = os.path.join(connections_dir, "followers_1.html")
            if os.path.exists(followers_path):
                self.data_parser.parse_followers(followers_path)
            else:
                logger.warning(f"Followers file not found: {followers_path}")
            
            self.progress_var.set(70)
            self.status_var.set("Processing following...")
            
            # Parse following
            following_path = os.path.join(connections_dir, "following.html")
            if os.path.exists(following_path):
                self.data_parser.parse_following(following_path)
            else:
                logger.warning(f"Following file not found: {following_path}")
            
            self.progress_var.set(90)
            self.status_var.set("Finding non-followers...")
            
            # Find non-followers
            self.data_parser.find_non_followers()
            
            self.progress_var.set(100)
            self.status_var.set("Data processing complete")
            
            # Update UI
            self.root.after(0, self.update_ui)
            
        except Exception as e:
            logger.error(f"Error processing data: {e}", exc_info=True)
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process data: {str(e)}"))
            self.status_var.set("Error processing data")
    
    def update_ui(self):
        """Update all UI elements with the parsed data."""
        self.requests_view.update_view()
        self.pending_requests_view.update_view()
        self.non_followers_view.update_view()
        
        # Select the first tab
        self.notebook.select(0)