# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
Main window for S3Ducky application.
"""

import tkinter as tk
from tkinter import ttk
import os
from ..utils.image_utils import set_app_icon


class MainWindow:
    """
    Main application window that manages the overall UI.
    """
    
    def __init__(self, title="S3Ducky", geometry="800x600"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(True, True)
        
        # Set app icon
        self.icon_photo = self._set_app_icon()
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Current page reference
        self.current_page = None
        
    def _set_app_icon(self):
        """Set the application icon from PNG file."""
        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'asset', 'logo.png')
        icon_path = os.path.abspath(icon_path)
        return set_app_icon(self.root, icon_path)
    
    def clear_main_frame(self):
        """Clear all widgets from the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_page(self, page_class, *args, **kwargs):
        """
        Show a specific page in the main frame.
        
        Args:
            page_class: The page class to instantiate and show
            *args, **kwargs: Arguments to pass to the page constructor
        """
        self.clear_main_frame()
        self.current_page = page_class(self.main_frame, *args, **kwargs)
        return self.current_page
    
    def get_main_frame(self):
        """Get the main frame for direct widget placement."""
        return self.main_frame
    
    def get_root(self):
        """Get the root tkinter window."""
        return self.root
    
    def bind_key(self, key, callback):
        """Bind a key event to the root window."""
        self.root.bind(key, callback)
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
    
    def destroy(self):
        """Destroy the window."""
        self.root.destroy()
