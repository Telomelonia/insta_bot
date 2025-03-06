#!/usr/bin/env python3
"""
Simple script to build Instagram Account Manager from a local directory.
This script avoids network drive issues by working with local files.
"""

import os
import shutil
import sys
import subprocess
import tempfile

def main():
    print("Instagram Account Manager - Local Build Helper")
    print("=" * 50)
    
    # Create a temporary directory on C: drive
    temp_dir = tempfile.mkdtemp(prefix="instagram_build_")
    print(f"Created temporary directory: {temp_dir}")
    
    # Get source directory from command line or current directory
    source_dir = os.getcwd()
    print(f"Source directory: {source_dir}")
    
    # Copy project files to the temp directory
    print("Copying project files to local drive...")
    for item in os.listdir(source_dir):
        if item not in ['build', 'dist', '__pycache__', '.git']:
            src_path = os.path.join(source_dir, item)
            dst_path = os.path.join(temp_dir, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
    
    # Run PyInstaller from the temp directory
    print("Running PyInstaller from local drive...")
    os.chdir(temp_dir)
    
    # Run PyInstaller command
    pyinstaller_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name=InstagramAccountManager",
        "instagram_manager/main.py"
    ]
    
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("PyInstaller completed successfully!")
        
        # Copy the build results back to the original directory
        print("Copying build results back to original location...")
        dist_src = os.path.join(temp_dir, "dist")
        dist_dst = os.path.join(source_dir, "dist")
        
        if os.path.exists(dist_dst):
            shutil.rmtree(dist_dst)
        
        shutil.copytree(dist_src, dist_dst)
        print(f"Build successful! Executable is in: {dist_dst}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running PyInstaller: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Clean up
    print("Cleaning up temporary files...")
    try:
        shutil.rmtree(temp_dir)
    except:
        print(f"Note: Could not remove temp directory: {temp_dir}")
        print("You may want to delete it manually later.")

if __name__ == "__main__":
    main()
