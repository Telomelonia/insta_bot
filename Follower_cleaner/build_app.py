#!/usr/bin/env python3
"""
Build Script for Instagram Account Manager

This script creates an executable (.exe) file from the Instagram Account Manager
application using PyInstaller.

Usage:
    python build_app.py

Requirements:
    - PyInstaller package: pip install pyinstaller
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

def ensure_pyinstaller_installed():
    """Check if PyInstaller is installed and install it if necessary."""
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully.")

def clean_build_directories():
    """Clean up previous build directories if they exist."""
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        print(f"Cleaning up {build_dir}...")
        shutil.rmtree(build_dir)
    
    if dist_dir.exists():
        print(f"Cleaning up {dist_dir}...")
        shutil.rmtree(dist_dir)

def create_executable(one_file=True, console=False, icon_path="Follower_cleaner/resources/instagram_icon.ico"):
    """
    Build the executable using PyInstaller.
    
    Args:
        one_file (bool): If True, create a single executable file. If False, create a directory.
        console (bool): If True, show console window when running the app. If False, hide console.
        icon_path (str): Path to the icon file for the executable.
    """
    print("Building executable with PyInstaller...")
    
    # Base command
    cmd = [
        "pyinstaller",
        "--name=InstagramAccountManager",
        "--clean",
        "--noconfirm",
    ]
    
    # Add one-file or one-directory mode
    if one_file:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    
    # Add console mode
    if not console:
        cmd.append("--noconsole")
    # Add icon if provided
    if icon_path and os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
    
    # Add additional data files (if any)
    resources_dir = Path("resources")
    if resources_dir.exists():
        cmd.append(f"--add-data={resources_dir};resources")
    
    # Main script
    cmd.append("Follower_cleaner/instagram_manager/main.py")
    
    # Execute PyInstaller
    print(f"Running command: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    print("\nExecutable created successfully!")
    if one_file:
        print(f"You can find the executable at: {os.path.abspath('dist/InstagramAccountManager.exe')}")
    else:
        print(f"You can find the executable at: {os.path.abspath('dist/InstagramAccountManager/InstagramAccountManager.exe')}")

def main():
    """Main function to handle the build process."""
    default_icon = "Follower_cleaner/resources/instagram_icon.ico"
    parser = argparse.ArgumentParser(description="Build Instagram Account Manager executable")
    parser.add_argument("--dir", action="store_true", help="Create a directory instead of a single file")
    parser.add_argument("--console", action="store_true", help="Show console window when app is running")
    parser.add_argument("--icon", type=str, help="Path to icon file for the executable", default=default_icon)
    parser.add_argument("--skip-cleanup", action="store_true", help="Skip cleaning up previous build files")
    
    args = parser.parse_args()
    
    # Make sure PyInstaller is installed
    ensure_pyinstaller_installed()
    
    # Clean up previous build files unless --skip-cleanup is specified
    if not args.skip_cleanup:
        clean_build_directories()
    
    # Create the executable
    create_executable(
        one_file=not args.dir,
        console=args.console,
        icon_path=args.icon
    )
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
