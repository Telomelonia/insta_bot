import sys
import os
import json
import zipfile
import tkinter as tk, webbrowser
from tkinter import ttk, filedialog, messagebox
from bs4 import BeautifulSoup
import threading
import time 
import re
from datetime import datetime
                                                                                                                      
class InstagramDataParser:
    def __init__(self):
        self.follow_requests = []
        self.followers = []
        self.following = []
        self.non_followers = []  # People you follow who don't follow you back
        self.pending_sent_requests = []  # People you've requested to follow
    
    def extract_zip(self, zip_path, extract_dir):
        """Extract Instagram data zip file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            return True
        except Exception as e:
            print(f"Error extracting zip: {e}")
            return False
    
    def parse_html_file(self, file_path):
        """Parse HTML files and extract username data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # This pattern works for the sample file you provided
            username_elements = soup.select("div._a6-p div div a")
            date_elements = soup.select("div._a6-p div div:nth-of-type(2)")
            
            results = []
            for i in range(len(username_elements)):
                username = username_elements[i].text.strip()
                
                # Extract date if available
                date_str = ""
                if i < len(date_elements):
                    date_str = date_elements[i].text.strip()
                
                # Extract username from URL as fallback
                if not username and "instagram.com/" in username_elements[i]['href']:
                    username = username_elements[i]['href'].split("instagram.com/")[1].strip()
                    if username.endswith("/"):
                        username = username[:-1]
                
                if username:
                    results.append({
                        "username": username,
                        "url": username_elements[i]['href'] if 'href' in username_elements[i].attrs
                                else f"https://www.instagram.com/{username}/",
                        "timestamp": date_str
                    })
            return results
        except Exception as e:
            print(f"Error parsing HTML file {file_path}: {e}")
            return []
    
    def parse_follow_requests(self, file_path):
        """Parse follow requests HTML file"""
        self.follow_requests = self.parse_html_file(file_path)
        return self.follow_requests
    
    def parse_pending_sent_requests(self, file_path):
        """Parse pending follow requests you've sent HTML file"""
        self.pending_sent_requests = self.parse_html_file(file_path)
        return self.pending_sent_requests
    
    def parse_followers(self, file_path):
        """Parse followers HTML file"""
        self.followers = self.parse_html_file(file_path)
        return self.followers
    
    def parse_following(self, file_path):
        """Parse following HTML file"""
        self.following = self.parse_html_file(file_path)
        return self.following
    
    def find_non_followers(self):
        """Find people you follow who don't follow you back"""
        follower_usernames = [follower["username"] for follower in self.followers]
        self.non_followers = [user for user in self.following if user["username"] not in follower_usernames]
        return self.non_followers


class InstagramManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Account Manager")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Set app icon
        # self.root.iconbitmap("instagram_icon.ico")  # You need to create/download this icon
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", background="#4e4edd", foreground="white", font=("Arial", 10))
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("Subheader.TLabel", font=("Arial", 12))
    
        # parse the data
        self.data_parser = InstagramDataParser()
        
        # Variables
        self.zip_path = tk.StringVar()
        self.extract_dir = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0.0)
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the application UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="Instagram Account Manager", style="Header.TLabel").pack(side=tk.LEFT)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Data Import", padding=10)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Select Instagram data export (.zip):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.zip_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(file_frame, text="Browse", command=self.browse_zip).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="Warning: Make sure to download HTML files, not JSON,\nfrom Instagram's Download Your Information page").grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        ttk.Button(file_frame, text="Import Data", command=self.import_data).grid(row=2, column=0, columnspan=3, pady=10)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)
        ttk.Progressbar(status_frame, variable=self.progress_var, length=200, mode="determinate").pack(side=tk.RIGHT)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: Follow Requests Received
        self.requests_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.requests_frame, text="Follow Requests Received")
        
        # Tab 2: Pending Follow Requests Sent
        self.pending_sent_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.pending_sent_frame, text="Pending Requests Sent")
        
        # Tab 3: Non-Followers (People you follow who don't follow you back)
        self.non_followers_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.non_followers_frame, text="Non-Followers")

        # Add option to load individual files for testing
        ttk.Button(main_frame, text="Load Pending Sent Requests File", 
                  command=self.load_pending_sent_requests_file).pack(side=tk.LEFT, pady=5)

    def load_pending_sent_requests_file(self):
        """Load pending sent requests file directly (for testing)"""
        file_path = filedialog.askopenfilename(
            title="Select Pending Follow Requests HTML File",
            filetypes=[("HTML files", "*.html")]
        )
        if file_path:
            try:
                self.data_parser.parse_pending_sent_requests(file_path)
                self.update_pending_sent_tab()
                self.notebook.select(1)  # Switch to the pending sent tab
                self.status_var.set("Loaded pending sent requests file")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
        
    def update_requests_tab(self):
        """Update the follow requests received tab with data"""
        # Clear existing content
        for widget in self.requests_frame.winfo_children():
            widget.destroy()
        
        # Header
        ttk.Label(self.requests_frame, text="Follow Requests Received", style="Subheader.TLabel").grid(row=0, column=0, sticky=tk.W, pady=(0, 10), columnspan=3)
        
        # Create Treeview for follow requests
        columns = ("Username", "Date", "URL", "Actions")
        tree = ttk.Treeview(self.requests_frame, columns=columns, show="headings", height=15)
        
        tree.heading("Username", text="Username")
        tree.heading("Date", text="Date Requested")
        tree.heading("URL", text="Profile URL")
        tree.heading("Actions", text="Actions")
        
        tree.column("Username", width=200)
        tree.column("Date", width=200)
        tree.column("URL", width=250)
        tree.column("Actions", width=150)
        
        tree.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        tree.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.requests_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Add action buttons
        # ttk.Button(self.requests_frame, text="Remove Selected", command=lambda: self.remove_selected_requests(tree)).grid(row=2, column=0, pady=10, padx=(0, 5))
        # ttk.Button(self.requests_frame, text="Remove All", command=lambda: self.remove_all_requests(tree)).grid(row=2, column=1, pady=10, padx=5)
        
        # Make the treeview expandable
        self.requests_frame.grid_rowconfigure(1, weight=1)
        self.requests_frame.grid_columnconfigure(0, weight=1)
        self.requests_frame.grid_columnconfigure(1, weight=1)
        self.requests_frame.grid_columnconfigure(2, weight=1)
        
        #Add binding for clickable URL
        def on_treeview_click(event):
            region = tree.identify_region(event.x, event.y)
            if region == "cell":
                column = tree.identify_column(event.x)
                if column == "#3":
                    item = tree.identify_row(event.y)
                    url = tree.item(item, "values")[2]
                    if url:
                        webbrowser.open(url)
                        self.status_var.set(f"Opening {url}")
                    else:
                        self.status_var.set("No URL available")
        tree.bind("<ButtonRelease-1>", on_treeview_click)

        # Populate treeview with follow requests
        for i, request in enumerate(self.data_parser.follow_requests):
            tree.insert("", "end", values=(request["username"], request["timestamp"], request["url"], "Remove"))
    
    def update_pending_sent_tab(self):
        """Update the pending follow requests sent tab with data"""
        # Clear existing content
        for widget in self.pending_sent_frame.winfo_children():
            widget.destroy()
        
        # Header
        ttk.Label(self.pending_sent_frame, text="Pending Follow Requests You've Sent", style="Subheader.TLabel").grid(row=0, column=0, sticky=tk.W, pady=(0, 10), columnspan=3)
        
        # Create Treeview for pending sent requests
        columns = ("Username", "Date", "URL", "Actions")
        tree = ttk.Treeview(self.pending_sent_frame, columns=columns, show="headings", height=15)
        
        tree.heading("Username", text="Username")
        tree.heading("Date", text="Date Sent")
        tree.heading("URL", text="Profile URL")
        tree.heading("Actions", text="Actions")
        
        tree.column("Username", width=200)
        tree.column("Date", width=200)
        tree.column("URL", width=250)
        tree.column("Actions", width=150)
        
        tree.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.pending_sent_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Add action buttons
        # ttk.Button(self.pending_sent_frame, text="Cancel Selected", command=lambda: self.cancel_selected_requests(tree)).grid(row=2, column=0, pady=10, padx=(0, 5))
        # ttk.Button(self.pending_sent_frame, text="Cancel All", command=lambda: self.cancel_all_requests(tree)).grid(row=2, column=1, pady=10, padx=5)
        
        # Make the treeview expandable
        self.pending_sent_frame.grid_rowconfigure(1, weight=1)
        self.pending_sent_frame.grid_columnconfigure(0, weight=1)
        self.pending_sent_frame.grid_columnconfigure(1, weight=1)
        self.pending_sent_frame.grid_columnconfigure(2, weight=1)
        
        # Add binding for clickable URL
        def on_treeview_click(event):
            region = tree.identify_region(event.x, event.y)
            if region == "cell":
                column = tree.identify_column(event.x)
                if column == "#3":
                    item = tree.identify_row(event.y)
                    url = tree.item(item, "values")[2]
                    if url:
                        webbrowser.open(url)
                        self.status_var.set(f"Opening {url}")
                    else:
                        self.status_var.set("No URL available")
        tree.bind("<ButtonRelease-1>", on_treeview_click)

        # Populate treeview with pending sent requests
        for i, request in enumerate(self.data_parser.pending_sent_requests):
            tree.insert("", "end", values=(request["username"], request["timestamp"], request["url"], "Cancel"))
    
    def update_non_followers_tab(self):
        """Update the non-followers tab with data"""
        # Clear existing content
        for widget in self.non_followers_frame.winfo_children():
            widget.destroy()
        
        # Header
        ttk.Label(self.non_followers_frame, text="Users You Follow Who Don't Follow You Back", style="Subheader.TLabel").grid(row=0, column=0, sticky=tk.W, pady=(0, 10), columnspan=3)
        
        # Create Treeview for non-followers
        columns = ("Username", "URL", "Actions")
        tree = ttk.Treeview(self.non_followers_frame, columns=columns, show="headings", height=15)
        
        tree.heading("Username", text="Username")
        tree.heading("URL", text="Profile URL")
        tree.heading("Actions", text="Actions")
        
        tree.column("Username", width=200)
        tree.column("URL", width=250)
        tree.column("Actions", width=150)
        
        tree.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.non_followers_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Add action buttons
        # ttk.Button(self.non_followers_frame, text="Unfollow Selected", command=lambda: self.unfollow_selected(tree)).grid(row=2, column=0, pady=10, padx=(0, 5))
        # ttk.Button(self.non_followers_frame, text="Unfollow All", command=lambda: self.unfollow_all(tree)).grid(row=2, column=1, pady=10, padx=5)
        
        # Make the treeview expandable
        self.non_followers_frame.grid_rowconfigure(1, weight=1)
        self.non_followers_frame.grid_columnconfigure(0, weight=1)
        self.non_followers_frame.grid_columnconfigure(1, weight=1)
        self.non_followers_frame.grid_columnconfigure(2, weight=1)
        # Add binding for clickable URL in non-followers tab
        def on_nonfollowers_treeview_click(event):
            region = tree.identify_region(event.x, event.y)
            if region == "cell":
                column = tree.identify_column(event.x)
                if column == "#2":  # URL column is the 2nd column
                    item = tree.identify_row(event.y)
                    url = tree.item(item, "values")[1]
                    if url:
                        webbrowser.open(url)
                        self.status_var.set(f"Opening {url}")
                    else:
                        self.status_var.set("No URL available")
        
        tree.bind("<ButtonRelease-1>", on_nonfollowers_treeview_click)
        
        # Populate treeview with non-followers
        for i, user in enumerate(self.data_parser.non_followers):
            tree.insert("", "end", values=(user["username"], user["url"], "Unfollow"))
    
    def browse_zip(self):
        """Browse for Instagram data zip file"""
        file_path = filedialog.askopenfilename(
            title="Select Instagram Data Export",
            filetypes=[("ZIP files", "*.zip")]
        )
        if file_path:
            self.zip_path.set(file_path)
            # Set default extract directory to same location as zip
            default_extract = os.path.join(os.path.dirname(file_path), "instagram_data_extracted")
            self.extract_dir.set(default_extract)
    
    def import_data(self):
        """Import and process Instagram data"""
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
        """Background process to extract and parse Instagram data"""
        try:
            self.status_var.set("Extracting zip file...")
            self.progress_var.set(10)
            
            # Extract zip
            success = self.data_parser.extract_zip(self.zip_path.get(), self.extract_dir.get())
            if not success:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to extract ZIP file"))
                self.status_var.set("Error extracting data")
                return
            
            self.progress_var.set(25)
            self.status_var.set("Processing follow requests received...")
            
            # Find and process HTML files
            connections_dir = os.path.join(self.extract_dir.get(), "connections", "followers_and_following")
            
            # Parse follow requests received
            follow_requests_path = os.path.join(connections_dir, "follow_requests_you've_received.html")
            if os.path.exists(follow_requests_path):
                self.data_parser.parse_follow_requests(follow_requests_path)
            
            self.progress_var.set(40)
            self.status_var.set("Processing pending follow requests sent...")
            
            # Parse pending follow requests sent
            pending_sent_path = os.path.join(connections_dir, "pending_follow_requests.html")
            if os.path.exists(pending_sent_path):
                self.data_parser.parse_pending_sent_requests(pending_sent_path)
            else:
                print(f"Warning: Could not find {pending_sent_path}")
                # If the file is in a different location than expected, try to find it
                for root, dirs, files in os.walk(self.extract_dir.get()):
                    if "pending_follow_requests.html" in files:
                        pending_sent_path = os.path.join(root, "pending_follow_requests.html")
                        self.data_parser.parse_pending_sent_requests(pending_sent_path)
                        break
            
            self.progress_var.set(55)
            self.status_var.set("Processing followers...")
            
            # Parse followers
            followers_path = os.path.join(connections_dir, "followers_1.html")
            if os.path.exists(followers_path):
                self.data_parser.parse_followers(followers_path)
            
            self.progress_var.set(70)
            self.status_var.set("Processing following...")
            
            # Parse following
            following_path = os.path.join(connections_dir, "following.html")
            if os.path.exists(following_path):
                self.data_parser.parse_following(following_path)
            
            self.progress_var.set(85)
            self.status_var.set("Finding non-followers...")
            
            # Find non-followers
            self.data_parser.find_non_followers()
            
            self.progress_var.set(100)
            self.status_var.set("Data processing complete")
            
            # Update UI
            self.root.after(0, self.update_requests_tab)
            self.root.after(0, self.update_pending_sent_tab)
            self.root.after(0, self.update_non_followers_tab)
            
        except Exception as e:
            print(f"Error processing data: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process data: {str(e)}"))
            self.status_var.set("Error processing data")   

def main():
    root = tk.Tk()
    app = InstagramManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()