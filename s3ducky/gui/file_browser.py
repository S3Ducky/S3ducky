# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
File browser page for S3Ducky.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from ..utils.formatters import format_file_size
from .footer import Footer


class FileBrowser:
    """
    Page for browsing and managing S3 bucket files.
    """
    
    def __init__(self, parent_frame, bucket_name, files_list, 
                 back_callback=None, refresh_callback=None, download_callback=None):
        self.parent_frame = parent_frame
        self.bucket_name = bucket_name
        self.files_list = files_list or []
        self.back_callback = back_callback
        self.refresh_callback = refresh_callback
        self.download_callback = download_callback
        
        # UI components
        self.tree = None
        self.download_status = None
        self.info_label = None
        
        # Selection tracking
        self.selected_files = set()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and layout all widgets for the file browser page."""
        # Title and info
        title_label = ttk.Label(self.parent_frame, text=f"S3 Bucket: {self.bucket_name}", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        self.info_label = ttk.Label(self.parent_frame, text=f"Found {len(self.files_list)} files")
        self.info_label.pack(pady=(0, 10))
        
        # Navigation buttons frame
        nav_frame = ttk.Frame(self.parent_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Back button
        if self.back_callback:
            back_button = ttk.Button(nav_frame, text="← Back to Credentials", 
                                    command=self.back_callback)
            back_button.pack(side=tk.LEFT)
        
        # Refresh button
        if self.refresh_callback:
            refresh_button = ttk.Button(nav_frame, text="🔄 Refresh Files", 
                                       command=self._on_refresh)
            refresh_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Files frame with scrollbar
        files_frame = ttk.Frame(self.parent_frame)
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self._create_file_tree(files_frame)
        
        # Download buttons frame
        button_frame = ttk.Frame(self.parent_frame)
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
                  command=self._download_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(download_frame, text="Download as Zip", 
                  command=self._download_as_zip).pack(side=tk.LEFT)
        
        # Status label
        self.download_status = ttk.Label(self.parent_frame, text="Select files to download")
        self.download_status.pack(pady=5)
        
        # Create footer
        Footer(self.parent_frame)
        
    def _create_file_tree(self, parent):
        """Create the file tree view."""
        # Create Treeview for file list
        columns = ('Sl.No.', 'Select', 'File Name', 'Size', 'Last Modified')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
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
        v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Populate the tree with files
        self._populate_tree()
        
        # Bind click event for selection
        self.tree.bind('<Button-1>', self._on_tree_click)
        
    def _populate_tree(self):
        """Populate the tree with file data."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.selected_files.clear()
        
        for index, file_info in enumerate(self.files_list, 1):
            size_str = format_file_size(file_info['size'])
            modified_str = file_info['modified'].strftime('%Y-%m-%d %H:%M')
            
            item_id = self.tree.insert('', 'end', values=(
                index, '☐', file_info['key'], size_str, modified_str))
    
    def _on_tree_click(self, event):
        """Handle tree item click for selection."""
        item = self.tree.identify('item', event.x, event.y)
        if item:
            column = self.tree.identify('column', event.x, event.y)
            if column == '#2':  # Select column (second column)
                if item in self.selected_files:
                    self.selected_files.remove(item)
                    self.tree.set(item, 'Select', '☐')
                else:
                    self.selected_files.add(item)
                    self.tree.set(item, 'Select', '☑')
                    
                self._update_selection_status()
    
    def _on_refresh(self):
        """Handle refresh button click."""
        if self.refresh_callback:
            self.refresh_callback()
    
    def select_all_files(self):
        """Select all files."""
        self.selected_files.clear()
        for child in self.tree.get_children():
            self.selected_files.add(child)
            self.tree.set(child, 'Select', '☑')
        self._update_selection_status()
        
    def deselect_all_files(self):
        """Deselect all files."""
        self.selected_files.clear()
        for child in self.tree.get_children():
            self.tree.set(child, 'Select', '☐')
        self._update_selection_status()
        
    def _update_selection_status(self):
        """Update the selection status label."""
        count = len(self.selected_files)
        if count == 0:
            self.download_status.config(text="Select files to download")
        elif count == 1:
            self.download_status.config(text="1 file selected")
        else:
            self.download_status.config(text=f"{count} files selected")
    
    def _get_selected_file_keys(self):
        """Get the S3 keys of selected files."""
        selected_keys = []
        for item in self.selected_files:
            file_name = self.tree.set(item, 'File Name')
            selected_keys.append(file_name)
        return selected_keys
    
    def _download_selected(self):
        """Handle download selected files."""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one file to download")
            return
            
        # Choose destination folder
        dest_folder = filedialog.askdirectory(title="Choose Download Destination")
        if not dest_folder:
            return
            
        selected_keys = self._get_selected_file_keys()
        
        if self.download_callback:
            self.download_callback(selected_keys, dest_folder, as_zip=False)
    
    def _download_as_zip(self):
        """Handle download as zip."""
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
            
        selected_keys = self._get_selected_file_keys()
        
        if self.download_callback:
            self.download_callback(selected_keys, zip_file_path, as_zip=True)
    
    def update_files_list(self, files_list):
        """
        Update the files list and refresh the display.
        
        Args:
            files_list (list): New list of files
        """
        self.files_list = files_list or []
        if self.info_label:
            self.info_label.config(text=f"Found {len(self.files_list)} files")
        self._populate_tree()
    
    def set_status(self, message, color="blue"):
        """
        Update the status label.
        
        Args:
            message (str): Status message to display
            color (str): Text color for the message
        """
        if self.download_status:
            self.download_status.config(text=message, foreground=color)
