# MIT License
# 
# Copyright (c) 2025 S3Ducky
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Build script for S3Ducky
Automates the process of creating a standalone executable
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("Dependencies installed successfully!")

def build_executable():
    """Build the standalone executable"""
    print("Building standalone executable...")
      # PyInstaller command with options
    cmd = [
        "pyinstaller",
        "--onefile",              # Create a single executable file
        "--windowed",             # Hide console window (for GUI apps)
        "--name=S3Ducky",         # Set executable name
        "--icon=asset/logo.png",  # Use logo as icon
        "--add-data=asset:asset", # Include asset folder
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*50)
        print("BUILD SUCCESSFUL!")
        print("="*50)
        print("Executable created: dist/S3Ducky.exe")
        print("You can now distribute this standalone executable.")
        print("\nTo test the executable:")
        print("1. Navigate to the 'dist' folder")
        print("2. Run S3Ducky.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return False
    
    return True

def main():
    """Main build process"""
    print("S3 Bucket Viewer - Build Script")
    print("="*40)
      # Check if we're in the correct directory
    if not os.path.exists("main.py"):
        print("Error: main.py not found!")
        print("Please run this script from the project directory.")
        return
    
    try:
        # Install dependencies
        install_dependencies()
        
        # Build executable
        if build_executable():
            print("\nBuild process completed successfully!")
        else:
            print("\nBuild process failed!")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
