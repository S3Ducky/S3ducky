# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
Image utilities for S3Ducky.
"""

import os
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def load_png_image(image_path, width=48, height=48):
    """
    Load a PNG image and resize it.
    
    Args:
        image_path (str): Path to the PNG image file
        width (int): Target width in pixels
        height (int): Target height in pixels
        
    Returns:
        ImageTk.PhotoImage or None: Loaded image or None if failed
    """
    try:
        if not PIL_AVAILABLE:
            print("PIL not available for loading PNG images")
            return None
            
        if os.path.exists(image_path):
            # Load PNG image
            pil_image = Image.open(image_path)
            
            # Resize to specified dimensions
            pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            return photo
        else:
            print(f"Image file not found: {image_path}")
            return None
            
    except Exception as e:
        print(f"Failed to load PNG image: {e}")
        return None


def set_app_icon(root, icon_path):
    """
    Set the application icon from a PNG file.
    
    Args:
        root (tk.Tk): The root window
        icon_path (str): Path to the icon PNG file
        
    Returns:
        ImageTk.PhotoImage or None: Icon photo object (keep reference to prevent GC)
    """
    try:
        if not PIL_AVAILABLE:
            print("PIL not available, using default icon")
            return None
            
        if os.path.exists(icon_path):
            # Load PNG image
            pil_image = Image.open(icon_path)
            
            # Resize for icon (tkinter works best with 32x32 or 16x16)
            pil_image = pil_image.resize((32, 32), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            # Set as window icon
            root.iconphoto(True, photo)
            
            print("Successfully loaded PNG icon")
            return photo
        else:
            print(f"Icon file not found: {icon_path}")
            return None
            
    except Exception as e:
        print(f"Failed to load icon: {e}")
        return None
