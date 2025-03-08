"""
Instagram Data Parser Module

This module handles parsing and processing of Instagram data exports.
"""

import os
import zipfile
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class InstagramDataParser:
    """
    Parser for Instagram data exports.
    
    This class handles extracting and parsing HTML files from Instagram's
    data exports to collect information about followers, following,
    and follow requests.
    """
    
    def __init__(self):
        """Initialize the parser with empty data structures."""
        self.follow_requests = []
        self.followers = []
        self.following = []
        self.non_followers = []  # People you follow who don't follow you back
        self.pending_sent_requests = []  # People you've requested to follow
    
    def extract_zip(self, zip_path, extract_dir):
        """
        Extract Instagram data zip file.
        
        Args:
            zip_path (str): Path to the Instagram data zip file
            extract_dir (str): Directory to extract files to
            
        Returns:
            bool: True if extraction succeeded, False otherwise
        """
        try:
            logger.info(f"Extracting {zip_path} to {extract_dir}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            return True
        except Exception as e:
            logger.error(f"Error extracting zip: {e}", exc_info=True)
            return False
    
    def parse_html_file(self, file_path):
        """
        Parse HTML files and extract username data.
        
        Args:
            file_path (str): Path to the HTML file to parse
            
        Returns:
            list: List of dictionaries containing user data
        """
        try:
            logger.info(f"Parsing HTML file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract user data from HTML elements
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
            
            logger.info(f"Found {len(results)} users in {file_path}")
            return results
        except Exception as e:
            logger.error(f"Error parsing HTML file {file_path}: {e}", exc_info=True)
            return []
    
    def parse_follow_requests(self, file_path):
        """
        Parse follow requests HTML file.
        
        Args:
            file_path (str): Path to the follow requests HTML file
            
        Returns:
            list: List of follow requests
        """
        self.follow_requests = self.parse_html_file(file_path)
        return self.follow_requests
    
    def parse_pending_sent_requests(self, file_path):
        """
        Parse pending follow requests you've sent HTML file.
        
        Args:
            file_path (str): Path to the pending follow requests HTML file
            
        Returns:
            list: List of pending follow requests you've sent
        """
        self.pending_sent_requests = self.parse_html_file(file_path)
        return self.pending_sent_requests
        
    def parse_followers(self, file_path):
        """
        Parse followers HTML file.
        
        Args:
            file_path (str): Path to the followers HTML file
            
        Returns:
            list: List of followers
        """
        self.followers = self.parse_html_file(file_path)
        return self.followers
    
    def parse_following(self, file_path):
        """
        Parse following HTML file.
        
        Args:
            file_path (str): Path to the following HTML file
            
        Returns:
            list: List of users you follow
        """
        self.following = self.parse_html_file(file_path)
        return self.following
    
    def find_non_followers(self):
        """
        Find people you follow who don't follow you back.
        
        Returns:
            list: List of non-followers
        """
        follower_usernames = {follower["username"].lower() for follower in self.followers}
        
        # Find users you follow who aren't in your followers list
        self.non_followers = [
            user for user in self.following 
            if user["username"].lower() not in follower_usernames
        ]
        
        logger.info(f"Found {len(self.non_followers)} non-followers")
        return self.non_followers