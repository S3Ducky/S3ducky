# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
File download and management operations for S3Ducky.
"""

import os
import zipfile
import tempfile
import threading
from .s3_client import S3Client


class FileManager:
    """
    Handles file download operations and management.
    """
    
    def __init__(self, s3_client: S3Client):
        self.s3_client = s3_client
        
    def download_files_individually(self, file_keys, dest_folder, progress_callback=None):
        """
        Download files individually to the destination folder.
        
        Args:
            file_keys (list): List of S3 object keys to download
            dest_folder (str): Destination folder path
            progress_callback (callable, optional): Callback for progress updates
        
        Raises:
            Exception: If download fails
        """
        if not self.s3_client.is_connected():
            raise RuntimeError("S3 client is not connected")
        
        for i, key in enumerate(file_keys, 1):
            # Update progress
            if progress_callback:
                progress_callback(f"Downloading {i}/{len(file_keys)}: {os.path.basename(key)}")
            
            # Create local file path
            local_filename = os.path.basename(key) if os.path.basename(key) else key.replace('/', '_')
            local_path = os.path.join(dest_folder, local_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Download file
            self.s3_client.download_file(key, local_path)
    
    def download_files_as_zip(self, file_keys, zip_file_path, progress_callback=None):
        """
        Download files and create a zip archive.
        
        Args:
            file_keys (list): List of S3 object keys to download
            zip_file_path (str): Path for the output zip file
            progress_callback (callable, optional): Callback for progress updates
        
        Raises:
            Exception: If download or zip creation fails
        """
        if not self.s3_client.is_connected():
            raise RuntimeError("S3 client is not connected")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download files to temporary directory
            temp_files = []
            for i, key in enumerate(file_keys, 1):
                # Update progress
                if progress_callback:
                    progress_callback(f"Downloading {i}/{len(file_keys)}: {os.path.basename(key)}")
                
                # Create temporary file path
                local_filename = os.path.basename(key) if os.path.basename(key) else key.replace('/', '_')
                temp_file_path = os.path.join(temp_dir, local_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
                
                # Download file
                self.s3_client.download_file(key, temp_file_path)
                temp_files.append((temp_file_path, local_filename))
                
            # Create zip file
            if progress_callback:
                progress_callback("Creating zip archive...")
            
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for temp_file_path, archive_name in temp_files:
                    zipf.write(temp_file_path, archive_name)
    
    def download_files_async(self, file_keys, destination, as_zip=False, 
                           progress_callback=None, completion_callback=None, error_callback=None):
        """
        Download files asynchronously in a separate thread.
        
        Args:
            file_keys (list): List of S3 object keys to download
            destination (str): Destination folder path or zip file path
            as_zip (bool): Whether to create a zip archive
            progress_callback (callable, optional): Callback for progress updates
            completion_callback (callable, optional): Callback when download completes
            error_callback (callable, optional): Callback when download fails
        """
        def download_thread():
            try:
                if as_zip:
                    self.download_files_as_zip(file_keys, destination, progress_callback)
                else:
                    self.download_files_individually(file_keys, destination, progress_callback)
                
                if completion_callback:
                    completion_callback()
                    
            except Exception as e:
                if error_callback:
                    error_callback(str(e))
        
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
        return thread
