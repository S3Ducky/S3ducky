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

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError
import os
import zipfile
import threading
from datetime import datetime
import webbrowser
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class S3DuckyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("S3Ducky")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set app icon
        self.set_app_icon()
        
        # AWS connection variables
        self.s3_client = None
        self.bucket_name = ""
        self.files_list = []
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show credentials page initially
        self.show_credentials_page()
        
    def set_app_icon(self):
        """Set the app icon from PNG file"""
        try:
            if not PIL_AVAILABLE:
                print("PIL not available, using default icon")
                return
                
            # Get the path to the PNG file
            icon_path = os.path.join(os.path.dirname(__file__), 'asset', 'logo.png')
            
            if os.path.exists(icon_path):
                # Load PNG image
                pil_image = Image.open(icon_path)
                
                # Resize if needed (tkinter works best with 32x32 or 16x16)
                pil_image = pil_image.resize((32, 32), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(pil_image)
                
                # Set as window icon
                self.root.iconphoto(True, photo)
                
                # Keep a reference to prevent garbage collection
                self.icon_photo = photo
                print("Successfully loaded PNG icon")
            else:
                print(f"Icon file not found: {icon_path}")
                
        except Exception as e:
            print(f"Failed to load icon: {e}")
            # Continue without icon if it fails
            pass

    def load_png_logo(self, width=48, height=48):
        """Load PNG logo for display in the UI"""
        try:
            if not PIL_AVAILABLE:
                return None
                
            # Get the path to the PNG file
            logo_path = os.path.join(os.path.dirname(__file__), 'asset', 'logo.png')
            
            if os.path.exists(logo_path):
                # Load PNG image
                pil_image = Image.open(logo_path)
                
                # Resize to specified dimensions
                pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(pil_image)
                
                return photo
            else:
                print(f"Logo file not found: {logo_path}")
                return None
                
        except Exception as e:
            print(f"Failed to load PNG logo: {e}")
            return None

    def show_credentials_page(self):
        """Display the credentials input page"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()          # Title with logo
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(pady=(0, 20))
        
        # Load and display logo
        logo_photo = self.load_png_logo(48, 48)
        if logo_photo:
            logo_label = ttk.Label(title_frame, image=logo_photo)
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
            # Keep a reference to prevent garbage collection
            self.logo_photo = logo_photo
        
        title_label = ttk.Label(title_frame, text="S3Ducky", 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Credentials frame
        cred_frame = ttk.LabelFrame(self.main_frame, text="AWS Credentials", padding=20)
        cred_frame.pack(fill=tk.X, pady=(0, 20))
        
        # AWS Access Key
        ttk.Label(cred_frame, text="AWS Access Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.access_key_var = tk.StringVar()
        self.access_key_entry = ttk.Entry(cred_frame, textvariable=self.access_key_var, width=50)
        self.access_key_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # AWS Secret Key
        ttk.Label(cred_frame, text="AWS Secret Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.secret_key_var = tk.StringVar()
        self.secret_key_entry = ttk.Entry(cred_frame, textvariable=self.secret_key_var, 
                                         width=50, show="*")
        self.secret_key_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # AWS Region
        ttk.Label(cred_frame, text="AWS Region:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.region_var = tk.StringVar(value="us-east-1")
        self.region_entry = ttk.Entry(cred_frame, textvariable=self.region_var, width=50)
        self.region_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # Bucket Name
        ttk.Label(cred_frame, text="Bucket Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.bucket_var = tk.StringVar()
        self.bucket_entry = ttk.Entry(cred_frame, textvariable=self.bucket_var, width=50)
        self.bucket_entry.grid(row=3, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
          # Resource (optional)
        ttk.Label(cred_frame, text="Prefix Filter (optional):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.resource_var = tk.StringVar()
        self.resource_entry = ttk.Entry(cred_frame, textvariable=self.resource_var, width=50)
        self.resource_entry.grid(row=4, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # Add help text for prefix filter
        help_label = ttk.Label(cred_frame, text="(Leave empty to see all files, or enter a prefix to filter files)", 
                              font=("Arial", 8), foreground="gray")
        help_label.grid(row=5, column=1, padx=(10, 0), pady=(0, 5), sticky=tk.W)
        
        # Configure grid weights
        cred_frame.columnconfigure(1, weight=1)
        
        # Connect button
        self.connect_button = ttk.Button(self.main_frame, text="Connect", 
                                        command=self.connect_to_s3)
        self.connect_button.pack(pady=10)
          # Status label
        self.status_label = ttk.Label(self.main_frame, text="Enter your AWS credentials to connect", 
                                     foreground="blue")
        self.status_label.pack(pady=5)
          # Bind Enter key to connect
        self.root.bind('<Return>', lambda event: self.connect_to_s3())
        
        # Add footer
        self.create_footer()
        
    def connect_to_s3(self):
        """Connect to S3 using provided credentials"""
        # Validate inputs
        if not all([self.access_key_var.get(), self.secret_key_var.get(), 
                   self.region_var.get(), self.bucket_var.get()]):
            messagebox.showerror("Error", "Please fill in all required fields (Access Key, Secret Key, Region, Bucket Name)")
            return
            
        # Disable connect button and show loading
        self.connect_button.config(state='disabled', text='Connecting...')
        self.status_label.config(text="Connecting to AWS S3...", foreground="orange")
        self.root.update()
        
        try:
            # Create S3 session and resource (more reliable than client for listing)
            from boto3.session import Session
            
            self.session = Session(
                aws_access_key_id=self.access_key_var.get(),
                aws_secret_access_key=self.secret_key_var.get(),
                region_name=self.region_var.get()
            )
            
            # Create both client and resource for different operations
            self.s3_client = self.session.client('s3')
            self.s3_resource = self.session.resource('s3')
              # Store connection details
            self.bucket_name = self.bucket_var.get()
            # Only use prefix if it's not empty and not just whitespace
            resource_input = self.resource_var.get().strip()
            self.resource_prefix = resource_input if resource_input else None
            
            # Load files list
            self.load_files_list()
            
            # Connection successful - show file browser
            self.show_file_browser()
            
        except NoCredentialsError:
            messagebox.showerror("Error", "Invalid AWS credentials")
            self.reset_connect_button()
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                messagebox.showerror("Error", f"Bucket '{self.bucket_name}' does not exist")
            elif error_code == 'AccessDenied':
                messagebox.showerror("Error", "Access denied. Check your credentials and permissions")
            else:
                messagebox.showerror("Error", f"AWS Error: {e.response['Error']['Message']}")
            self.reset_connect_button()
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
            self.reset_connect_button()
            
    def load_files_list(self):
        """Load files list from S3 bucket using pagination to get all files"""
        try:
            self.files_list = []
            
            print(f"Debug: Loading files from bucket: {self.bucket_name}")
            if self.resource_prefix:
                print(f"Debug: Using prefix filter: {self.resource_prefix}")
            
            # Use client method with pagination (most reliable)
            paginator = self.s3_client.get_paginator('list_objects_v2')
            
            # Set up pagination parameters
            page_params = {'Bucket': self.bucket_name}
            if self.resource_prefix:
                page_params['Prefix'] = self.resource_prefix
            
            page_iterator = paginator.paginate(**page_params)
            
            total_files = 0
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        total_files += 1
                        self.files_list.append({
                            'key': obj['Key'],
                            'size': obj['Size'],
                            'modified': obj['LastModified']
                        })
                        
                        # Log progress for large buckets
                        if total_files % 1000 == 0:
                            print(f"Debug: Loaded {total_files} files so far...")
            
            print(f"Debug: Successfully loaded {len(self.files_list)} files from S3")
            
            # Sort files by name
            self.files_list.sort(key=lambda x: x['key'])
            
        except Exception as e:
            print(f"Debug: Failed to load files: {str(e)}")
            raise Exception(f"Failed to load files: {str(e)}")
            
    def reset_connect_button(self):
        """Reset the connect button state"""
        self.connect_button.config(state='normal', text='Connect')
        self.status_label.config(text="Connection failed. Please check your credentials.", 
                                foreground="red")
        
    def refresh_files(self):
        """Refresh the files list from S3 bucket"""
        try:
            # Show loading status
            if hasattr(self, 'download_status'):
                self.download_status.config(text="Refreshing files...", foreground="orange")
            
            # Reload files from S3
            self.load_files_list()
            
            # Refresh the file browser display
            self.show_file_browser()
            
            # Show success message
            if hasattr(self, 'download_status'):
                self.download_status.config(text=f"Refreshed! Found {len(self.files_list)} files", 
                                          foreground="green")
            
        except Exception as e:
            error_msg = f"Refresh failed: {str(e)}"
            if hasattr(self, 'download_status'):
                self.download_status.config(text=error_msg, foreground="red")
            messagebox.showerror("Error", error_msg)
            
    def show_file_browser(self):
        """Display the file browser page"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()        # Title and info
        title_label = ttk.Label(self.main_frame, text=f"S3 Bucket: {self.bucket_name}", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        self.info_label = ttk.Label(self.main_frame, text=f"Found {len(self.files_list)} files")
        self.info_label.pack(pady=(0, 10))
        
        # Navigation buttons frame
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Back button
        back_button = ttk.Button(nav_frame, text="← Back to Credentials", 
                                command=self.show_credentials_page)
        back_button.pack(side=tk.LEFT)
        
        # Refresh button
        refresh_button = ttk.Button(nav_frame, text="🔄 Refresh Files", 
                                   command=self.refresh_files)
        refresh_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Files frame with scrollbar
        files_frame = ttk.Frame(self.main_frame)
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
          # Create Treeview for file list
        columns = ('Sl.No.', 'Select', 'File Name', 'Size', 'Last Modified')
        self.tree = ttk.Treeview(files_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('Sl.No.', text='Sl.No.')
        self.tree.heading('Select', text='Select')
        self.tree.heading('File Name', text='File Name')
        self.tree.heading('Size', text='Size')
        self.tree.heading('Last Modified', text='Last Modified')
        
        # Configure column widths
        self.tree.column('Sl.No.', width=60, anchor='center')
        self.tree.column('Select', width=60, anchor='center')
        self.tree.column('File Name', width=400, anchor='w')
        self.tree.column('Size', width=100, anchor='e')
        self.tree.column('Last Modified', width=150, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(files_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        files_frame.grid_rowconfigure(0, weight=1)
        files_frame.grid_columnconfigure(0, weight=1)
          # Populate the tree with files
        self.selected_files = set()
        for index, file_info in enumerate(self.files_list, 1):
            size_str = self.format_file_size(file_info['size'])
            modified_str = file_info['modified'].strftime('%Y-%m-%d %H:%M')
            
            item_id = self.tree.insert('', 'end', values=(index, '☐', file_info['key'], size_str, modified_str))
            
        # Bind click event for selection
        self.tree.bind('<Button-1>', self.on_tree_click)
        
        # Download buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Select All / Deselect All buttons
        select_frame = ttk.Frame(button_frame)
        select_frame.pack(side=tk.LEFT)
        
        ttk.Button(select_frame, text="Select All", command=self.select_all_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(select_frame, text="Deselect All", command=self.deselect_all_files).pack(side=tk.LEFT)
        
        # Download buttons
        download_frame = ttk.Frame(button_frame)
        download_frame.pack(side=tk.RIGHT)
        
        ttk.Button(download_frame, text="Download Selected", 
                  command=self.download_selected_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(download_frame, text="Download as Zip", 
                  command=self.download_as_zip).pack(side=tk.LEFT)          # Status label
        self.download_status = ttk.Label(self.main_frame, text="Select files to download")
        self.download_status.pack(pady=5)
        
        # Create footer
        self.create_footer()
        
    def create_footer(self):
        """Create a footer with clickable links"""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        # Add a separator line
        separator = ttk.Separator(footer_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(5, 10))
        
        # Create footer content frame
        footer_content = ttk.Frame(footer_frame)
        footer_content.pack(fill=tk.X)
        
        # Repository link
        repo_label = ttk.Label(footer_content, text="S3Ducky", 
                              foreground="blue", cursor="hand2", font=("Arial", 9, "underline"))
        repo_label.pack(side=tk.LEFT)
        repo_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/extinctsion/S3ducky"))
        
        # Separator text
        ttk.Label(footer_content, text=" | ", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # MIT License link
        mit_label = ttk.Label(footer_content, text="MIT License", 
                             foreground="blue", cursor="hand2", font=("Arial", 9, "underline"))
        mit_label.pack(side=tk.LEFT)
        mit_label.bind("<Button-1>", lambda e: webbrowser.open("https://opensource.org/licenses/MIT"))
          # Copyright text
        copyright_label = ttk.Label(footer_content, text=" © 2025 S3Ducky", 
                                   font=("Arial", 9), foreground="gray")
        copyright_label.pack(side=tk.RIGHT)
        
    def on_tree_click(self, event):
        """Handle tree item click for selection"""
        item = self.tree.identify('item', event.x, event.y)
        if item:
            column = self.tree.identify('column', event.x, event.y)
            if column == '#2':  # Select column (now the second column)
                if item in self.selected_files:
                    self.selected_files.remove(item)
                    self.tree.set(item, 'Select', '☐')
                else:
                    self.selected_files.add(item)
                    self.tree.set(item, 'Select', '☑')
                    
                self.update_selection_status()
                
    def select_all_files(self):
        """Select all files"""
        self.selected_files.clear()
        for child in self.tree.get_children():
            self.selected_files.add(child)
            self.tree.set(child, 'Select', '☑')
        self.update_selection_status()
        
    def deselect_all_files(self):
        """Deselect all files"""
        self.selected_files.clear()
        for child in self.tree.get_children():
            self.tree.set(child, 'Select', '☐')
        self.update_selection_status()
        
    def update_selection_status(self):
        """Update the selection status label"""
        count = len(self.selected_files)
        if count == 0:
            self.download_status.config(text="Select files to download")
        elif count == 1:
            self.download_status.config(text="1 file selected")
        else:
            self.download_status.config(text=f"{count} files selected")
            
    def get_selected_file_keys(self):
        """Get the S3 keys of selected files"""
        selected_keys = []
        for item in self.selected_files:
            file_name = self.tree.set(item, 'File Name')
            selected_keys.append(file_name)
        return selected_keys
        
    def download_selected_files(self):
        """Download selected files individually"""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one file to download")
            return
            
        # Choose destination folder
        dest_folder = filedialog.askdirectory(title="Choose Download Destination")
        if not dest_folder:
            return
            
        selected_keys = self.get_selected_file_keys()
        
        # Start download in separate thread
        thread = threading.Thread(target=self._download_files_thread, 
                                 args=(selected_keys, dest_folder, False))
        thread.daemon = True
        thread.start()
        
    def download_as_zip(self):
        """Download selected files as a zip archive"""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one file to download")
            return
            
        # Choose destination for zip file
        zip_file_path = filedialog.asksaveasfilename(
            title="Save Zip File As",
            defaultextension=".zip",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        if not zip_file_path:
            return
            
        selected_keys = self.get_selected_file_keys()
        
        # Start download in separate thread
        thread = threading.Thread(target=self._download_files_thread, 
                                 args=(selected_keys, zip_file_path, True))
        thread.daemon = True
        thread.start()
        
    def _download_files_thread(self, file_keys, destination, as_zip):
        """Download files in a separate thread"""
        try:
            self.root.after(0, lambda: self.download_status.config(text="Downloading...", foreground="orange"))
            
            if as_zip:
                self._download_as_zip(file_keys, destination)
            else:
                self._download_individual_files(file_keys, destination)
                
            self.root.after(0, lambda: self.download_status.config(
                text=f"Download completed successfully!", foreground="green"))
            self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
            
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            self.root.after(0, lambda: self.download_status.config(text=error_msg, foreground="red"))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
    def _download_individual_files(self, file_keys, dest_folder):
        """Download files individually to the destination folder"""
        for i, key in enumerate(file_keys, 1):
            # Update status
            status_text = f"Downloading {i}/{len(file_keys)}: {os.path.basename(key)}"
            self.root.after(0, lambda text=status_text: self.download_status.config(text=text))
            
            # Create local file path
            local_filename = os.path.basename(key) if os.path.basename(key) else key.replace('/', '_')
            local_path = os.path.join(dest_folder, local_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Download file
            self.s3_client.download_file(self.bucket_name, key, local_path)
            
    def _download_as_zip(self, file_keys, zip_file_path):
        """Download files and create a zip archive"""
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download files to temporary directory
            temp_files = []
            for i, key in enumerate(file_keys, 1):
                # Update status
                status_text = f"Downloading {i}/{len(file_keys)}: {os.path.basename(key)}"
                self.root.after(0, lambda text=status_text: self.download_status.config(text=text))
                
                # Create temporary file path
                local_filename = os.path.basename(key) if os.path.basename(key) else key.replace('/', '_')
                temp_file_path = os.path.join(temp_dir, local_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
                
                # Download file
                self.s3_client.download_file(self.bucket_name, key, temp_file_path)
                temp_files.append((temp_file_path, local_filename))
                
            # Create zip file
            self.root.after(0, lambda: self.download_status.config(text="Creating zip archive..."))
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for temp_file_path, archive_name in temp_files:
                    zipf.write(temp_file_path, archive_name)
                    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
        
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = S3DuckyApp()
    app.run()
