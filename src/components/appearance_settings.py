"""
Appearance Settings Component
Allows users to choose between light and dark themes
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable


class AppearanceSettings:
    def __init__(self, parent: tk.Widget, on_theme_change: Callable = None):
        self.parent = parent
        self.on_theme_change = on_theme_change
        
        # Main frame
        self.frame = tk.Frame(parent)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create appearance settings UI"""
        # Title
        title_label = tk.Label(
            self.frame,
            text="Appearance Settings",
            font=("Segoe UI", 12, "bold")
        )
        title_label.pack(pady=(10, 20), anchor="w")
        
        # Theme selection frame
        theme_frame = tk.LabelFrame(
            self.frame,
            text="Theme",
            font=("Segoe UI", 10),
            padx=20,
            pady=15
        )
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        # Radio buttons for theme selection
        self.theme_var = tk.StringVar(value="dark")
        
        dark_radio = tk.Radiobutton(
            theme_frame,
            text="🌙 Dark Mode",
            variable=self.theme_var,
            value="dark",
            command=self._on_theme_selected,
            font=("Segoe UI", 10)
        )
        dark_radio.pack(anchor="w", pady=5)
        
        light_radio = tk.Radiobutton(
            theme_frame,
            text="☀️ Light Mode",
            variable=self.theme_var,
            value="light",
            command=self._on_theme_selected,
            font=("Segoe UI", 10)
        )
        light_radio.pack(anchor="w", pady=5)
        
        # Description
        desc_label = tk.Label(
            theme_frame,
            text="Choose your preferred color theme for the application.",
            font=("Segoe UI", 9),
            justify="left",
            wraplength=400
        )
        desc_label.pack(anchor="w", pady=(10, 0))
    
    def _on_theme_selected(self):
        """Handle theme selection"""
        if self.on_theme_change:
            theme = self.theme_var.get()
            self.on_theme_change(theme)
    
    def set_theme(self, theme: str):
        """Set the current theme"""
        self.theme_var.set(theme)
    
    def get_theme(self) -> str:
        """Get the current theme"""
        return self.theme_var.get()
    
    def apply_theme(self, theme: dict):
        """Apply theme colors to this component"""
        self.frame.config(bg=theme["bg"])
        
        # Update all child widgets
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.LabelFrame):
                widget.config(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    highlightbackground=theme["border"],
                    highlightcolor=theme["border"]
                )
                # Update radio buttons inside label frame
                for child in widget.winfo_children():
                    if isinstance(child, tk.Radiobutton):
                        child.config(
                            bg=theme["bg"],
                            fg=theme["fg"],
                            selectcolor=theme["bg_secondary"],
                            activebackground=theme["bg"],
                            activeforeground=theme["fg"]
                        )
                    elif isinstance(child, tk.Label):
                        child.config(bg=theme["bg"], fg=theme["label_fg"])
