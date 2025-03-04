#!/usr/bin/env python3
import os
import sys
import subprocess
import tempfile
import shutil
from urllib.request import urlretrieve
import zipfile

def print_step(message):
    """Print a step with formatting"""
    print("\n" + "=" * 60)
    print(f"  {message}")
    print("=" * 60)

def check_python():
    """Check if Python 3.6+ is installed"""
    print_step("Checking Python version")
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Using Python {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print_step("Installing required packages")
    requirements = ["requests", "pillow", "beautifulsoup4", "pyinstaller"]
    
    for package in requirements:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("✓ All required packages installed")
    return True

def download_project():
    """Download the project from GitHub"""
    print_step("Downloading Instagram Account Manager")
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "master.zip")
    
    try:
        print("Downloading project files...")
        urlretrieve("https://github.com/YourUsername/InstagramAccountManager/archive/refs/heads/main.zip", zip_path)
        
        print("Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extracted directory (it might be named differently based on repo)
        extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d)) and d != "__MACOSX"]
        if not extracted_dirs:
            print("Error: Could not find extracted directory")
            return None
        
        extracted_dir = os.path.join(temp_dir, extracted_dirs[0])
        print(f"✓ Project downloaded to {extracted_dir}")
        return extracted_dir
    except Exception as e:
        print(f"Error downloading project: {e}")
        return None

def build_app(project_dir):
    """Build the application"""
    print_step("Building the application")
    try:
        # Change to the project directory
        os.chdir(project_dir)
        
        # Run the build script
        print("Running build script...")
        subprocess.check_call([sys.executable, "build_app.py"])
        
        # Check if the build was successful
        if os.path.exists(os.path.join("dist", "InstagramAccountManager.exe")):
            print("✓ Application built successfully!")
            
            # Copy to desktop for easy access
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            dest_path = os.path.join(desktop, "InstagramAccountManager.exe")
            
            shutil.copy2(os.path.join("dist", "InstagramAccountManager.exe"), dest_path)
            print(f"✓ Application copied to desktop: {dest_path}")
            return True
        else:
            print("Error: Build failed, executable not found")
            return False
    except Exception as e:
        print(f"Error building application: {e}")
        return False

def main():
    """Main installation function"""
    print("\n" + "*" * 70)
    print("*  Instagram Account Manager - Easy Installer  *")
    print("*" * 70 + "\n")
    
    print("This script will download and install the Instagram Account Manager application.")
    print("Please wait while the installation proceeds...\n")
    
    if not check_python():
        input("Press Enter to exit...")
        return
    
    if not install_requirements():
        input("Press Enter to exit...")
        return
    
    project_dir = download_project()
    if not project_dir:
        input("Press Enter to exit...")
        return
    
    if build_app(project_dir):
        print("\n" + "*" * 70)
        print("*  Installation Complete!  *")
        print("*" * 70)
        print("\nYou can now run InstagramAccountManager.exe from your desktop.")
    else:
        print("\nInstallation failed. Please try again or contact support.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()