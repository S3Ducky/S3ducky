# MIT License
# 
# Copyright (c) 2025 S3 Bucket Viewer
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
Test script for S3 Bucket Viewer
Verifies that all dependencies are available and the application can start
"""

import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog
        print("✓ tkinter modules imported successfully")
    except ImportError as e:
        print(f"✗ tkinter import failed: {e}")
        return False
    
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError
        print("✓ boto3 modules imported successfully")
    except ImportError as e:
        print(f"✗ boto3 import failed: {e}")
        print("Please install boto3: pip install boto3")
        return False
    
    try:
        import os
        import zipfile
        import threading
        from datetime import datetime
        print("✓ Standard library modules imported successfully")
    except ImportError as e:
        print(f"✗ Standard library import failed: {e}")
        return False
    
    return True

def test_gui_creation():
    """Test that the GUI can be created"""
    print("\nTesting GUI creation...")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        print("✓ Tkinter root window created successfully")
        root.destroy()
        return True
    except Exception as e:
        print(f"✗ GUI creation failed: {e}")
        return False

def test_boto3_functionality():
    """Test basic boto3 functionality (without actual AWS connection)"""
    print("\nTesting boto3 functionality...")
    
    try:
        import boto3
        # Just test that we can create a client (won't actually connect)
        client = boto3.client('s3', 
                             aws_access_key_id='test',
                             aws_secret_access_key='test',
                             region_name='us-east-1')
        print("✓ boto3 S3 client created successfully")
        return True
    except Exception as e:
        print(f"✗ boto3 client creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("S3 Bucket Viewer - Test Suite")
    print("="*40)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_gui_creation():
        tests_passed += 1
    
    if test_boto3_functionality():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("python s3_bucket_viewer.py")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
