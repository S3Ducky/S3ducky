# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
Credentials input page for S3Ducky.
"""

import tkinter as tk
from tkinter import ttk
import os
from ..utils.image_utils import load_png_image
from .footer import Footer


class CredentialsPage:
    """
    Page for entering AWS credentials and connection details.
    """
    
    def __init__(self, parent_frame, connect_callback=None):
        self.parent_frame = parent_frame
        self.connect_callback = connect_callback
        
        # Variables for form inputs
        self.access_key_var = tk.StringVar()
        self.secret_key_var = tk.StringVar()
        self.region_var = tk.StringVar(value="us-east-1")
        self.bucket_var = tk.StringVar()
        self.resource_var = tk.StringVar()
        
        # UI components
        self.connect_button = None
        self.status_label = None
        self.logo_photo = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and layout all widgets for the credentials page."""
        # Title with logo
        title_frame = ttk.Frame(self.parent_frame)
        title_frame.pack(pady=(0, 20))
        
        # Load and display logo
        logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'asset', 'logo.png')
        logo_path = os.path.abspath(logo_path)
        self.logo_photo = load_png_image(logo_path, 48, 48)
        
        if self.logo_photo:
            logo_label = ttk.Label(title_frame, image=self.logo_photo)
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="S3Ducky", 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Credentials frame
        cred_frame = ttk.LabelFrame(self.parent_frame, text="AWS Credentials", padding=20)
        cred_frame.pack(fill=tk.X, pady=(0, 20))
        
        # AWS Access Key
        ttk.Label(cred_frame, text="AWS Access Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.access_key_entry = ttk.Entry(cred_frame, textvariable=self.access_key_var, width=50)
        self.access_key_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # AWS Secret Key
        ttk.Label(cred_frame, text="AWS Secret Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.secret_key_entry = ttk.Entry(cred_frame, textvariable=self.secret_key_var, 
                                         width=50, show="*")
        self.secret_key_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # AWS Region
        ttk.Label(cred_frame, text="AWS Region:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.region_entry = ttk.Entry(cred_frame, textvariable=self.region_var, width=50)
        self.region_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # Bucket Name
        ttk.Label(cred_frame, text="Bucket Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.bucket_entry = ttk.Entry(cred_frame, textvariable=self.bucket_var, width=50)
        self.bucket_entry.grid(row=3, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # Resource (optional)
        ttk.Label(cred_frame, text="Prefix Filter (optional):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.resource_entry = ttk.Entry(cred_frame, textvariable=self.resource_var, width=50)
        self.resource_entry.grid(row=4, column=1, padx=(10, 0), pady=5, sticky=tk.EW)
        
        # Add help text for prefix filter
        help_label = ttk.Label(cred_frame, text="(Leave empty to see all files, or enter a prefix to filter files)", 
                              font=("Arial", 8), foreground="gray")
        help_label.grid(row=5, column=1, padx=(10, 0), pady=(0, 5), sticky=tk.W)
        
        # Configure grid weights
        cred_frame.columnconfigure(1, weight=1)
        
        # Connect button
        self.connect_button = ttk.Button(self.parent_frame, text="Connect", 
                                        command=self._on_connect)
        self.connect_button.pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(self.parent_frame, text="Enter your AWS credentials to connect", 
                                     foreground="blue")
        self.status_label.pack(pady=5)
        
        # Add footer
        Footer(self.parent_frame)
        
    def _on_connect(self):
        """Handle connect button click."""
        if self.connect_callback:
            credentials = {
                'access_key': self.access_key_var.get(),
                'secret_key': self.secret_key_var.get(),
                'region': self.region_var.get(),
                'bucket_name': self.bucket_var.get(),
                'resource_prefix': self.resource_var.get()
            }
            self.connect_callback(credentials)
    
    def set_status(self, message, color="blue"):
        """
        Update the status label.
        
        Args:
            message (str): Status message to display
            color (str): Text color for the message
        """
        if self.status_label:
            self.status_label.config(text=message, foreground=color)
    
    def set_connect_button_state(self, enabled=True, text="Connect"):
        """
        Update the connect button state and text.
        
        Args:
            enabled (bool): Whether the button should be enabled
            text (str): Button text
        """
        if self.connect_button:
            state = 'normal' if enabled else 'disabled'
            self.connect_button.config(state=state, text=text)
    
    def get_credentials(self):
        """
        Get the current credential values.
        
        Returns:
            dict: Dictionary containing all credential fields
        """
        return {
            'access_key': self.access_key_var.get(),
            'secret_key': self.secret_key_var.get(),
            'region': self.region_var.get(),
            'bucket_name': self.bucket_var.get(),
            'resource_prefix': self.resource_var.get()
        }
