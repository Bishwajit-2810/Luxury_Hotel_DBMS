# themes/luxury_theme.py

import tkinter as tk
from tkinter import ttk

def apply_luxury_theme(root):
    """Apply Material Grey theme with classic luxurious gold button style."""
    style = ttk.Style()
    
    # Configure root window background to dark grey (Material Grey)
    root.configure(bg="#212121")  # Dark Grey background (Material Design Grey)

    # Configure ttk widgets
    style.theme_use("default")
    
    # Label Style
    style.configure(
        "TLabel",
        background="#212121",  # Dark background for labels
        foreground="#E0E0E0",   # Light Grey text (for readability)
        font=("Arial", 12),      # Use Arial font for modern look
    )
    
    # Button Style (Updated to Classic Luxury Gold)
    style.configure(
        "TButton",
        background="#D4AF37",  # Classic gold button background
        foreground="black",    # Black text for high contrast
        font=("Arial", 11, "bold"),
        padding=8,
    )
    style.map(
        "TButton",
        background=[("active", "#C28F00"), ("disabled", "#BDBDBD")],  # Darker gold on hover and grey for disabled state
    )
    
    # Entry Field Style
    style.configure(
        "TEntry",
        background="#424242",  # Dark grey input fields
        foreground="#E0E0E0",   # Light grey text in input fields
        font=("Arial", 12),
        insertcolor="#03A9F4",  # Blue caret color (primary accent)
    )
    
    # Frame Style
    style.configure(
        "TFrame",
        background="#212121",  # Dark grey background for frames
    )
    
    # Scrollbar Style
    style.configure(
        "TScrollbar",
        troughcolor="#333333",  # Darker grey for scrollbar trough
        background="#757575",   # Grey scrollbar background
        arrowcolor="#03A9F4",   # Blue arrow for scrollbars (accent color)
        bordercolor="#212121",  # Border color matching the background
    )
    
    # Default Font for the entire application
    root.option_add("*Font", "Arial 11")  # Modern, clean font
    root.option_add("*Foreground", "#E0E0E0")  # Default text color
    root.option_add("*Background", "#212121")  # Default dark background color for widgets
