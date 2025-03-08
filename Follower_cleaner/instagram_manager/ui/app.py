"""
Instagram Manager App UI Module - Apple UI Style

This module contains the main application UI class for the Instagram Manager
with Apple UI design standards applied.
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
    Main application class for the Instagram Account Manager with Apple UI design.
    
    This class creates and manages the main UI window and tabs following
    macOS design guidelines.
    """
    
    def __init__(self, root):
        """
        Initialize the application with the Tkinter root window.
        
        Args:
            root (tk.Tk): The root Tkinter window
        """
        self.root = root
        self.root.title("Instagram Manager")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Set app icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "instagram_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Setup Apple-like styles
        self._setup_apple_styles()
        
        # Initialize data parser
        self.data_parser = InstagramDataParser()
        
        # Variables
        self.zip_path = tk.StringVar()
        self.extract_dir = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0.0)
        
        # Create UI elements
        self._create_apple_ui()
        
        logger.info("Application UI initialized with Apple design standards")
    
    def _setup_apple_styles(self):
        """Configure ttk styles for Apple-like appearance."""
        self.style = ttk.Style()
        
        # Use the closest theme to macOS
        if "aqua" in self.style.theme_names():
            # If running on macOS, use native aqua theme
            self.style.theme_use("aqua")
        else:
            # Otherwise use a light theme and customize
            self.style.theme_use("clam")
        
        # Define Apple-like colors
        apple_bg = "#FFFFFF"
        apple_accent = "#0066CC"  # Apple's blue accent color
        apple_light_gray = "#F5F5F7"
        apple_dark_gray = "#86868B"
        
        # Configure styles to match Apple's design language
        self.style.configure("TFrame", background=apple_bg)
        self.style.configure("TButton", 
                            background=apple_accent, 
                            foreground="white", 
                            font=("SF Pro", 10, "normal"),
                            borderwidth=0,
                            focusthickness=0,
                            padding=5)
        self.style.map("TButton",
                      background=[('active', '#0077E6')],
                      relief=[('pressed', 'flat')])
        
        # Secondary button style (outlined)
        self.style.configure("Secondary.TButton", 
                            background=apple_bg,
                            foreground=apple_accent,
                            font=("SF Pro", 10, "normal"),
                            borderwidth=1,
                            relief="solid",
                            focusthickness=0,
                            padding=5)
        self.style.map("Secondary.TButton",
                      background=[('active', '#F0F0F0')],
                      foreground=[('active', apple_accent)])
        
        # Label styles
        self.style.configure("TLabel", 
                            background=apple_bg, 
                            font=("SF Pro", 10, "normal"))
        
        self.style.configure("Header.TLabel", 
                            font=("SF Pro", 20, "normal"),
                            foreground="#000000",
                            background=apple_bg)
        
        self.style.configure("Subheader.TLabel", 
                            font=("SF Pro", 14, "normal"),
                            foreground="#000000",
                            background=apple_bg)
        
        # Notebook (tab) style
        self.style.configure("TNotebook", 
                            background=apple_bg,
                            borderwidth=0)
        self.style.configure("TNotebook.Tab", 
                            background=apple_light_gray,
                            foreground=apple_dark_gray,
                            padding=[12, 4],
                            font=("SF Pro", 10, "normal"))
        self.style.map("TNotebook.Tab",
                      background=[("selected", apple_bg)],
                      foreground=[("selected", apple_accent)],
                      expand=[("selected", [0, 0, 0, 0])])
        
        # Progress bar
        self.style.configure("TProgressbar", 
                            background=apple_accent,
                            troughcolor=apple_light_gray,
                            borderwidth=0,
                            thickness=6)
        
        # Entry fields
        self.style.configure("TEntry", 
                            font=("SF Pro", 10, "normal"),
                            borderwidth=1,
                            relief="solid",
                            fieldbackground=apple_bg)
        
        # Labelframe
        self.style.configure("TLabelframe", 
                            background=apple_bg,
                            borderwidth=1,
                            relief="solid")
        self.style.configure("TLabelframe.Label", 
                            background=apple_bg,
                            font=("SF Pro", 12, "normal"),
                            foreground="#000000")
    
    def _create_apple_ui(self):
        """Create the application UI elements with Apple design standards."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with SF font and proper spacing
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Instagram Manager", style="Header.TLabel").pack(side=tk.LEFT)
        
        # File selection section
        self._create_file_section(main_frame)
        
        # Notebook (tabs) with Apple-like styling
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Create tab frames with proper padding
        self.requests_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.requests_frame, text="Follow Requests")
        
        self.pending_requests_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.pending_requests_frame, text="Pending Requests")
        
        self.non_followers_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.non_followers_frame, text="Non-Followers")
        
        # Initialize tab views
        self.requests_view = RequestsTabView(self.requests_frame, self.data_parser, self.status_var)
        self.pending_requests_view = PendingRequestsTabView(self.pending_requests_frame, self.data_parser, self.status_var)
        self.non_followers_view = NonFollowersTabView(self.non_followers_frame, self.data_parser, self.status_var)
        
        # Progress and status bar in Apple style
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        progress_bar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, 
                                      length=100, mode='determinate', 
                                      variable=self.progress_var,
                                      style="TProgressbar")
        progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT)
    
    def _create_file_section(self, parent):
        """
        Create the file selection and import section with Apple design.
        
        Args:
            parent (ttk.Frame): Parent frame to add the section to
        """
        file_frame = ttk.LabelFrame(parent, text="Data Import", padding=15)
        file_frame.pack(fill=tk.X, pady=10)
        
        # Grid configuration for proper spacing
        file_frame.columnconfigure(1, weight=1)
        
        # File selection row
        ttk.Label(file_frame, text="Instagram data export (.zip):").grid(row=0, column=0, sticky=tk.W, pady=10)
        ttk.Entry(file_frame, textvariable=self.zip_path, width=50).grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="Choose File...", style="Secondary.TButton", command=self.browse_zip).grid(row=0, column=2, padx=10, pady=10)
        
        # Warning message with SF font
        warning_label = ttk.Label(file_frame, 
                                text="Please download HTML files (not JSON) from Instagram's 'Download Your Information' page",
                                foreground="#FF3B30")  # Apple's red warning color
        warning_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=10)
        
        # Button row with Apple-styled button
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=15)
        
        ttk.Button(button_frame, text="Import Data", command=self.import_data).pack()
    
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