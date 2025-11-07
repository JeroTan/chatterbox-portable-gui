"""
Text Input Component
Reusable text input area with Enter/Shift+Enter support
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class TextInputComponent:
    """
    Multi-line text input with keyboard shortcuts
    - Enter: Generate
    - Shift+Enter: New line
    """
    
    def __init__(self, parent, on_generate: Optional[Callable] = None):
        """
        Args:
            parent: Parent tkinter widget
            on_generate: Callback when Enter is pressed
        """
        self.on_generate = on_generate
        
        # Container frame
        self.frame = ttk.LabelFrame(parent, text="Text Input", padding="10")
        
        # Text widget with scrollbar
        text_container = ttk.Frame(self.frame)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = tk.Text(
            text_container,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            height=6,
            relief=tk.SOLID,
            borderwidth=1
        )
        
        scrollbar = ttk.Scrollbar(text_container, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Keyboard bindings
        self.text_widget.bind("<Return>", self._on_enter_key)
        self.text_widget.bind("<Shift-Return>", self._on_shift_enter)
        
        # Placeholder
        self.placeholder = "Enter your text here...\nPress Enter to generate, Shift+Enter for new line"
        self._show_placeholder()
        
        self.text_widget.bind("<FocusIn>", self._on_focus_in)
        self.text_widget.bind("<FocusOut>", self._on_focus_out)
    
    def _show_placeholder(self):
        """Show placeholder text"""
        self.text_widget.insert("1.0", self.placeholder)
        self.text_widget.config(fg="gray")
    
    def _on_focus_in(self, event):
        """Remove placeholder on focus"""
        if self.text_widget.get("1.0", tk.END).strip() == self.placeholder:
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.config(fg="black")
    
    def _on_focus_out(self, event):
        """Show placeholder if empty"""
        if not self.text_widget.get("1.0", tk.END).strip():
            self._show_placeholder()
    
    def _on_enter_key(self, event):
        """Handle Enter key press"""
        if self.on_generate:
            self.on_generate()
        return "break"  # Prevent default newline
    
    def _on_shift_enter(self, event):
        """Handle Shift+Enter for new line"""
        self.text_widget.insert(tk.INSERT, "\n")
        return "break"
    
    def get_text(self) -> str:
        """Get current text value"""
        text = self.text_widget.get("1.0", tk.END).strip()
        return "" if text == self.placeholder else text
    
    def set_text(self, text: str):
        """Set text value"""
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", text)
        self.text_widget.config(fg="black")
    
    def clear(self):
        """Clear text"""
        self.text_widget.delete("1.0", tk.END)
        self._show_placeholder()
