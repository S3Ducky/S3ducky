# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
Footer component for S3Ducky.
"""

import tkinter as tk
from tkinter import ttk
import webbrowser


class Footer:
    """
    Footer component with clickable links and copyright information.
    """
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self._create_footer()
    
    def _create_footer(self):
        """Create the footer with links and copyright."""
        footer_frame = ttk.Frame(self.parent_frame)
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
