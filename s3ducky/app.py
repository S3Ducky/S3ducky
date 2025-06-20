# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
Main application controller for S3Ducky.
"""

from tkinter import messagebox
from botocore.exceptions import ClientError, NoCredentialsError

from .gui.main_window import MainWindow
from .gui.credentials_page import CredentialsPage
from .gui.file_browser import FileBrowser
from .core.s3_client import S3Client
from .core.file_manager import FileManager


class S3DuckyApp:
    """
    Main application controller that manages the overall application flow.
    """
    
    def __init__(self):
        # Initialize main window
        self.main_window = MainWindow("S3Ducky", "800x600")
        
        # Initialize core components
        self.s3_client = S3Client()
        self.file_manager = FileManager(self.s3_client)
        
        # Current state
        self.files_list = []
        self.current_page = None
        
        # Bind Enter key to connect action
        self.main_window.bind_key('<Return>', self._on_enter_key)
        
        # Show credentials page initially
        self.show_credentials_page()
    
    def _on_enter_key(self, event):
        """Handle Enter key press."""
        # If on credentials page and credentials page has focus, attempt to connect
        if isinstance(self.current_page, CredentialsPage):
            self._connect_to_s3(self.current_page.get_credentials())
    
    def show_credentials_page(self):
        """Display the credentials input page."""
        self.current_page = self.main_window.show_page(
            CredentialsPage, 
            connect_callback=self._connect_to_s3
        )
    
    def show_file_browser_page(self):
        """Display the file browser page."""
        if not self.s3_client.is_connected():
            messagebox.showerror("Error", "Not connected to S3")
            self.show_credentials_page()
            return
        
        self.current_page = self.main_window.show_page(
            FileBrowser,
            bucket_name=self.s3_client.bucket_name,
            files_list=self.files_list,
            back_callback=self.show_credentials_page,
            refresh_callback=self._refresh_files,
            download_callback=self._download_files
        )
    
    def _connect_to_s3(self, credentials):
        """
        Connect to S3 using provided credentials.
        
        Args:
            credentials (dict): Dictionary containing AWS credentials and connection details
        """
        # Validate inputs
        required_fields = ['access_key', 'secret_key', 'region', 'bucket_name']
        if not all([credentials.get(field) for field in required_fields]):
            messagebox.showerror("Error", "Please fill in all required fields (Access Key, Secret Key, Region, Bucket Name)")
            return
        
        # Update UI to show connecting state
        if isinstance(self.current_page, CredentialsPage):
            self.current_page.set_connect_button_state(False, 'Connecting...')
            self.current_page.set_status("Connecting to AWS S3...", "orange")
        
        # Force UI update
        self.main_window.get_root().update()
        
        try:
            # Attempt connection
            self.s3_client.connect(
                access_key=credentials['access_key'],
                secret_key=credentials['secret_key'],
                region=credentials['region'],
                bucket_name=credentials['bucket_name'],
                resource_prefix=credentials.get('resource_prefix')
            )
            
            # Load files list
            self._load_files_list()
            
            # Connection successful - show file browser
            self.show_file_browser_page()
            
        except NoCredentialsError:
            messagebox.showerror("Error", "Invalid AWS credentials")
            self._reset_credentials_page()
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                messagebox.showerror("Error", f"Bucket '{credentials['bucket_name']}' does not exist")
            elif error_code == 'AccessDenied':
                messagebox.showerror("Error", "Access denied. Check your credentials and permissions")
            else:
                messagebox.showerror("Error", f"AWS Error: {e.response['Error']['Message']}")
            self._reset_credentials_page()
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
            self._reset_credentials_page()
    
    def _reset_credentials_page(self):
        """Reset the credentials page to normal state after connection failure."""
        if isinstance(self.current_page, CredentialsPage):
            self.current_page.set_connect_button_state(True, 'Connect')
            self.current_page.set_status("Connection failed. Please check your credentials.", "red")
    
    def _load_files_list(self):
        """Load files list from S3 bucket."""
        try:
            self.files_list = self.s3_client.list_objects()
        except Exception as e:
            raise Exception(f"Failed to load files: {str(e)}")
    
    def _refresh_files(self):
        """Refresh the files list from S3 bucket."""
        try:
            # Show loading status
            if isinstance(self.current_page, FileBrowser):
                self.current_page.set_status("Refreshing files...", "orange")
            
            # Reload files from S3
            self._load_files_list()
            
            # Update the file browser display
            if isinstance(self.current_page, FileBrowser):
                self.current_page.update_files_list(self.files_list)
                self.current_page.set_status(f"Refreshed! Found {len(self.files_list)} files", "green")
            
        except Exception as e:
            error_msg = f"Refresh failed: {str(e)}"
            if isinstance(self.current_page, FileBrowser):
                self.current_page.set_status(error_msg, "red")
            messagebox.showerror("Error", error_msg)
    
    def _download_files(self, file_keys, destination, as_zip=False):
        """
        Download files asynchronously.
        
        Args:
            file_keys (list): List of S3 object keys to download
            destination (str): Destination folder path or zip file path
            as_zip (bool): Whether to create a zip archive
        """
        def progress_callback(message):
            """Update progress in the main thread."""
            self.main_window.get_root().after(0, lambda: self._update_download_status(message, "orange"))
        
        def completion_callback():
            """Handle download completion in the main thread."""
            self.main_window.get_root().after(0, lambda: self._update_download_status("Download completed successfully!", "green"))
            self.main_window.get_root().after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
        
        def error_callback(error_message):
            """Handle download error in the main thread."""
            error_msg = f"Download failed: {error_message}"
            self.main_window.get_root().after(0, lambda: self._update_download_status(error_msg, "red"))
            self.main_window.get_root().after(0, lambda: messagebox.showerror("Error", error_msg))
        
        # Start async download
        self.file_manager.download_files_async(
            file_keys=file_keys,
            destination=destination,
            as_zip=as_zip,
            progress_callback=progress_callback,
            completion_callback=completion_callback,
            error_callback=error_callback
        )
    
    def _update_download_status(self, message, color):
        """Update download status on the current page."""
        if isinstance(self.current_page, FileBrowser):
            self.current_page.set_status(message, color)
    
    def run(self):
        """Start the application."""
        self.main_window.run()


if __name__ == "__main__":
    app = S3DuckyApp()
    app.run()
