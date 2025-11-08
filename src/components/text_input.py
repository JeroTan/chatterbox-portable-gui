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
    
    def __init__(self, parent, on_generate: Optional[Callable] = None, on_text_change: Optional[Callable] = None):
        """
        Args:
            parent: Parent tkinter widget
            on_generate: Callback when Enter is pressed
            on_text_change: Callback when text changes
        """
        self.on_generate = on_generate
        self.on_text_change = on_text_change
        
        # Track whether placeholder is showing
        self.is_placeholder_showing = False
        
        # Track if we're programmatically setting text
        self.is_programmatic_change = False
        
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
        
        # Bind text change event (fires after any modification)
        self.text_widget.bind("<<Modified>>", self._on_text_modified)
        
        # Placeholder
        self.placeholder = "Enter your text here...\nPress Enter to generate, Shift+Enter for new line"
        self._show_placeholder()
        
        self.text_widget.bind("<FocusIn>", self._on_focus_in)
        self.text_widget.bind("<FocusOut>", self._on_focus_out)
    
    def _show_placeholder(self):
        """Show placeholder text"""
        self.text_widget.insert("1.0", self.placeholder)
        self.text_widget.config(fg="gray")
        self.is_placeholder_showing = True
    
    def _on_focus_in(self, event):
        """Remove placeholder on focus"""
        if self.is_placeholder_showing:
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.config(fg="black")
            self.is_placeholder_showing = False
    
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
    
    def _on_text_modified(self, event):
        """Handle text modification"""
        # Clear the modified flag to allow future events
        self.text_widget.edit_modified(False)
        
        # Skip if this is a programmatic change
        if self.is_programmatic_change:
            return
        
        # Call the callback if provided
        if self.on_text_change:
            text = self.get_text()
            self.on_text_change(text)
    
    def get_text(self) -> str:
        """Get current text value"""
        if self.is_placeholder_showing:
            return ""
        text = self.text_widget.get("1.0", tk.END).strip()
        return text
    
    def set_text(self, text: str):
        """Set text value"""
        # Mark as programmatic change to prevent callbacks
        self.is_programmatic_change = True
        
        try:
            # Force remove focus from text widget to prevent focus events from interfering
            # This ensures placeholder logic doesn't conflict with setting text
            self.text_widget.master.focus_set()  # Move focus to parent
            
            # If placeholder is showing, clear it first
            if self.is_placeholder_showing:
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.config(fg="black")
                self.is_placeholder_showing = False
            
            # Clear existing content (whether it's placeholder or real text)
            self.text_widget.delete("1.0", tk.END)
            
            if text:
                # Insert the new text
                self.text_widget.insert("1.0", text)
                self.text_widget.config(fg="black")
                self.is_placeholder_showing = False
            else:
                # Show placeholder if empty
                self._show_placeholder()
                
            # Reset the modified flag after programmatic text change
            self.text_widget.edit_modified(False)
        finally:
            # Always clear the programmatic flag
            self.is_programmatic_change = False
    
    def clear(self):
        """Clear text"""
        # Mark as programmatic change to prevent callbacks
        self.is_programmatic_change = True
        
        try:
            self.text_widget.delete("1.0", tk.END)
            self._show_placeholder()
        finally:
            self.is_programmatic_change = False
