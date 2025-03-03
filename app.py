import sys
import os
import json
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import re
from datetime import datetime

class InstagramBot:
    def __init__(self):
        self.driver = None
        self.logged_in = False
    
    def initialize_browser(self):
        """Initialize the Chrome browser with required options"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # Use existing Chrome profile to maintain login state
        chrome_options.add_argument("--user-data-dir=C:\\ChromeProfile")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            return True
        except Exception as e:
            print(f"Error initializing browser: {e}")
            return False
    
    def check_login_status(self):
        """Check if user is logged in to Instagram"""
        try:
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            # Check if profile icon exists (indication of being logged in)
            if len(self.driver.find_elements(By.XPATH, "//a[contains(@href, '/direct/inbox/')]")) > 0:
                self.logged_in = True
                return True
            return False
        except Exception as e:
            print(f"Error checking login status: {e}")
            return False
    
    def remove_follow_request(self, username):
        """Remove a specific follow request"""
        try:
            self.driver.get(f"https://www.instagram.com/{username}")
            time.sleep(2)
            
            # Find and click the "..." button
            menu_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'More options')]"))
            )
            menu_button.click()
            time.sleep(1)
            
            # Find and click "Remove" option
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Remove')]"))
            )
            remove_button.click()
            time.sleep(1)
            
            return True
        except Exception as e:
            print(f"Error removing follow request for {username}: {e}")
            return False
    
    def unfollow_user(self, username):
        """Unfollow a specific user"""
        try:
            self.driver.get(f"https://www.instagram.com/{username}")
            time.sleep(2)
            
            # Find and click the "Following" button
            following_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Following')]"))
            )
            following_button.click()
            time.sleep(1)
            
            # Find and click "Unfollow" option in the confirmation dialog
            unfollow_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Unfollow')]"))
            )
            unfollow_button.click()
            time.sleep(1)
            
            return True
        except Exception as e:
            print(f"Error unfollowing {username}: {e}")
            return False
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


class InstagramDataParser:
    def __init__(self):
        self.follow_requests = []
        self.followers = []
        self.following = []
        self.non_followers = []  # People you follow who don't follow you back
    
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
        
        # Instagram bot and data parser
        self.bot = InstagramBot()
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
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: Follow Requests
        self.requests_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.requests_frame, text="Follow Requests")
        
        # Tab 2: Non-Followers (People you follow who don't follow you back)
        self.non_followers_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.non_followers_frame, text="Non-Followers")
        
        # Tab 3: Browser Control
        self.browser_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.browser_frame, text="Browser Control")
        
        # Browser control content
        ttk.Label(self.browser_frame, text="Browser Control", style="Subheader.TLabel").pack(anchor=tk.W, pady=(0, 10))
        ttk.Label(self.browser_frame, text="This will open a Chrome browser instance that uses your current Chrome profile.").pack(anchor=tk.W)
        ttk.Label(self.browser_frame, text="Make sure you're already logged into Instagram in Chrome.").pack(anchor=tk.W, pady=(0, 10))
        
        browser_btn_frame = ttk.Frame(self.browser_frame)
        browser_btn_frame.pack(anchor=tk.W, pady=10)
        
        ttk.Button(browser_btn_frame, text="Initialize Browser", command=self.init_browser).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(browser_btn_frame, text="Check Login Status", command=self.check_login).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(browser_btn_frame, text="Close Browser", command=self.close_browser).pack(side=tk.LEFT)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Progressbar(status_frame, variable=self.progress_var, length=200, mode="determinate").pack(side=tk.RIGHT)
    
    def update_requests_tab(self):
        """Update the follow requests tab with data"""
        # Clear existing content
        for widget in self.requests_frame.winfo_children():
            widget.destroy()
        
        # Header
        ttk.Label(self.requests_frame, text="Pending Follow Requests", style="Subheader.TLabel").grid(row=0, column=0, sticky=tk.W, pady=(0, 10), columnspan=3)
        
        # Create Treeview for follow requests
        columns = ("Username", "Date", "Actions")
        tree = ttk.Treeview(self.requests_frame, columns=columns, show="headings", height=15)
        
        tree.heading("Username", text="Username")
        tree.heading("Date", text="Date Requested")
        tree.heading("Actions", text="Actions")
        
        tree.column("Username", width=200)
        tree.column("Date", width=200)
        tree.column("Actions", width=150)
        
        tree.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.requests_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Add action buttons
        ttk.Button(self.requests_frame, text="Remove Selected", command=lambda: self.remove_selected_requests(tree)).grid(row=2, column=0, pady=10, padx=(0, 5))
        ttk.Button(self.requests_frame, text="Remove All", command=lambda: self.remove_all_requests(tree)).grid(row=2, column=1, pady=10, padx=5)
        
        # Make the treeview expandable
        self.requests_frame.grid_rowconfigure(1, weight=1)
        self.requests_frame.grid_columnconfigure(0, weight=1)
        self.requests_frame.grid_columnconfigure(1, weight=1)
        self.requests_frame.grid_columnconfigure(2, weight=1)
        
        # Populate treeview with follow requests
        for i, request in enumerate(self.data_parser.follow_requests):
            tree.insert("", "end", values=(request["username"], request["timestamp"], "Remove"))
    
    def update_non_followers_tab(self):
        """Update the non-followers tab with data"""
        # Clear existing content
        for widget in self.non_followers_frame.winfo_children():
            widget.destroy()
        
        # Header
        ttk.Label(self.non_followers_frame, text="Users You Follow Who Don't Follow You Back", style="Subheader.TLabel").grid(row=0, column=0, sticky=tk.W, pady=(0, 10), columnspan=3)
        
        # Create Treeview for non-followers
        columns = ("Username", "Actions")
        tree = ttk.Treeview(self.non_followers_frame, columns=columns, show="headings", height=15)
        
        tree.heading("Username", text="Username")
        tree.heading("Actions", text="Actions")
        
        tree.column("Username", width=300)
        tree.column("Actions", width=150)
        
        tree.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.non_followers_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Add action buttons
        ttk.Button(self.non_followers_frame, text="Unfollow Selected", command=lambda: self.unfollow_selected(tree)).grid(row=2, column=0, pady=10, padx=(0, 5))
        ttk.Button(self.non_followers_frame, text="Unfollow All", command=lambda: self.unfollow_all(tree)).grid(row=2, column=1, pady=10, padx=5)
        
        # Make the treeview expandable
        self.non_followers_frame.grid_rowconfigure(1, weight=1)
        self.non_followers_frame.grid_columnconfigure(0, weight=1)
        self.non_followers_frame.grid_columnconfigure(1, weight=1)
        self.non_followers_frame.grid_columnconfigure(2, weight=1)
        
        # Populate treeview with non-followers
        for i, user in enumerate(self.data_parser.non_followers):
            tree.insert("", "end", values=(user["username"], "Unfollow"))
    
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
            
            self.progress_var.set(30)
            self.status_var.set("Processing follow requests...")
            
            # Find and process HTML files
            connections_dir = os.path.join(self.extract_dir.get(), "connections", "followers_and_following")
            
            # Parse follow requests
            follow_requests_path = os.path.join(connections_dir, "follow_requests_you've_received.html")
            if os.path.exists(follow_requests_path):
                self.data_parser.parse_follow_requests(follow_requests_path)
            
            self.progress_var.set(50)
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
            
            self.progress_var.set(90)
            self.status_var.set("Finding non-followers...")
            
            # Find non-followers
            self.data_parser.find_non_followers()
            
            self.progress_var.set(100)
            self.status_var.set("Data processing complete")
            
            # Update UI
            self.root.after(0, self.update_requests_tab)
            self.root.after(0, self.update_non_followers_tab)
            
        except Exception as e:
            print(f"Error processing data: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process data: {str(e)}"))
            self.status_var.set("Error processing data")
    
    def init_browser(self):
        """Initialize browser"""
        self.status_var.set("Initializing browser...")
        
        def _init():
            success = self.bot.initialize_browser()
            if success:
                self.status_var.set("Browser initialized")
            else:
                self.status_var.set("Failed to initialize browser")
                messagebox.showerror("Error", "Failed to initialize browser. Make sure Chrome is installed.")
        
        threading.Thread(target=_init, daemon=True).start()
    
    def check_login(self):
        """Check if logged in to Instagram"""
        if not self.bot.driver:
            messagebox.showerror("Error", "Browser not initialized. Please initialize browser first.")
            return
        
        self.status_var.set("Checking login status...")
        
        def _check():
            logged_in = self.bot.check_login_status()
            if logged_in:
                self.status_var.set("Logged in to Instagram")
                messagebox.showinfo("Login Status", "You are logged in to Instagram")
            else:
                self.status_var.set("Not logged in to Instagram")
                messagebox.showwarning("Login Status", "You are not logged in to Instagram. Please log in using the browser.")
        
        threading.Thread(target=_check, daemon=True).start()
    
    def close_browser(self):
        """Close browser"""
        if self.bot.driver:
            self.bot.close_browser()
            self.status_var.set("Browser closed")
        else:
            self.status_var.set("No browser to close")
    
    def remove_selected_requests(self, tree):
        """Remove selected follow requests"""
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No items selected")
            return
        
        if not self.bot.driver or not self.bot.logged_in:
            messagebox.showerror("Error", "Please initialize browser and check login status first")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove the selected follow requests?"):
            for item in selected_items:
                username = tree.item(item, "values")[0]
                threading.Thread(target=self._remove_request, args=(username, item, tree), daemon=True).start()
    
    def _remove_request(self, username, item, tree):
        """Remove a specific follow request in a background thread"""
        self.status_var.set(f"Removing request from {username}...")
        success = self.bot.remove_follow_request(username)
        
        if success:
            self.root.after(0, lambda: tree.delete(item))
            self.status_var.set(f"Removed request from {username}")
        else:
            self.status_var.set(f"Failed to remove request from {username}")
    
    def remove_all_requests(self, tree):
        """Remove all follow requests"""
        if not tree.get_children():
            messagebox.showinfo("Info", "No follow requests to remove")
            return
        
        if not self.bot.driver or not self.bot.logged_in:
            messagebox.showerror("Error", "Please initialize browser and check login status first")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove ALL follow requests?"):
            items = tree.get_children()
            total = len(items)
            
            def _process_batch(items, index=0):
                if index >= len(items):
                    self.status_var.set("All follow requests removed")
                    return
                
                item = items[index]
                username = tree.item(item, "values")[0]
                
                self.status_var.set(f"Removing request {index+1}/{total}: {username}")
                self.progress_var.set((index/total) * 100)
                
                success = self.bot.remove_follow_request(username)
                if success:
                    tree.delete(item)
                
                # Process next item after a delay
                self.root.after(1000, lambda: _process_batch(items, index+1))
            
            threading.Thread(target=lambda: _process_batch(items), daemon=True).start()
    
    def unfollow_selected(self, tree):
        """Unfollow selected users"""
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No items selected")
            return
        
        if not self.bot.driver or not self.bot.logged_in:
            messagebox.showerror("Error", "Please initialize browser and check login status first")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to unfollow the selected users?"):
            for item in selected_items:
                username = tree.item(item, "values")[0]
                threading.Thread(target=self._unfollow_user, args=(username, item, tree), daemon=True).start()
    
    def _unfollow_user(self, username, item, tree):
        """Unfollow a specific user in a background thread"""
        self.status_var.set(f"Unfollowing {username}...")
        success = self.bot.unfollow_user(username)
        
        if success:
            self.root.after(0, lambda: tree.delete(item))
            self.status_var.set(f"Unfollowed {username}")
        else:
            self.status_var.set(f"Failed to unfollow {username}")
    
    def unfollow_all(self, tree):
        """Unfollow all users in the non-followers list"""
        if not tree.get_children():
            messagebox.showinfo("Info", "No users to unfollow")
            return
        
        if not self.bot.driver or not self.bot.logged_in:
            messagebox.showerror("Error", "Please initialize browser and check login status first")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to unfollow ALL these users?"):
            items = tree.get_children()
            total = len(items)
            
            def _process_batch(items, index=0):
                if index >= len(items):
                    self.status_var.set("All users unfollowed")
                    return
                
                item = items[index]
                username = tree.item(item, "values")[0]
                
                self.status_var.set(f"Unfollowing {index+1}/{total}: {username}")
                self.progress_var.set((index/total) * 100)
                
                success = self.bot.unfollow_user(username)
                if success:
                    tree.delete(item)
                
                # Process next item after a delay to avoid rate limiting
                self.root.after(2000, lambda: _process_batch(items, index+1))
            
            threading.Thread(target=lambda: _process_batch(items), daemon=True).start()


def main():
    root = tk.Tk()
    app = InstagramManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()