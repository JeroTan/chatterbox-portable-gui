"""
Naming Scheme Component
Allows user to specify an optional prefix for generated audio filenames
"""

import tkinter as tk
from tkinter import ttk
from store.state import app_state


class NamingSchemeComponent:
    """Component for configuring output filename prefix"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Create UI
        self._create_widgets()
        
        # Load initial value from state
        self.prefix_entry.insert(0, app_state.naming_prefix)
        
        print("✅ Naming Scheme Component initialized")
    
    def _create_widgets(self):
        """Create the naming scheme UI elements"""
        # Label
        label = ttk.Label(
            self.frame, 
            text="Filename Prefix (optional):",
            font=("Segoe UI", 9)
        )
        label.pack(fill=tk.X, pady=(5, 2))
        
        # Input frame
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill=tk.X)
        
        # Prefix entry
        self.prefix_entry = ttk.Entry(input_frame)
        self.prefix_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.prefix_entry.bind('<KeyRelease>', self._on_prefix_changed)
        
        # Clear button
        clear_btn = ttk.Button(
            input_frame, 
            text="Clear", 
            command=self._clear_prefix,
            width=8
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Example label
        self.example_label = ttk.Label(
            self.frame,
            text=self._get_example_text(),
            font=("Segoe UI", 8),
            foreground="gray"
        )
        self.example_label.pack(fill=tk.X, pady=(2, 0))
    
    def _on_prefix_changed(self, event=None):
        """Handle prefix input change"""
        prefix = self.prefix_entry.get().strip()
        app_state.update(naming_prefix=prefix)
        
        # Update example
        self.example_label.config(text=self._get_example_text())
    
    def _clear_prefix(self):
        """Clear the prefix entry"""
        self.prefix_entry.delete(0, tk.END)
        app_state.update(naming_prefix="")
        self.example_label.config(text=self._get_example_text())
    
    def _get_example_text(self) -> str:
        """Get example filename text"""
        prefix = self.prefix_entry.get().strip()
        if prefix:
            # Clean prefix for display
            clean_prefix = "".join(c if c.isalnum() or c == "_" else "" for c in prefix)
            return f"e.g., {clean_prefix}_20251114_123456_hello.wav"
        return "e.g., 20251114_123456_hello_world.wav"
    
    def get_prefix(self) -> str:
        """Get the current prefix value"""
        return self.prefix_entry.get().strip()
    
    def set_prefix(self, prefix: str):
        """Set the prefix value (for loading projects)"""
        self.prefix_entry.delete(0, tk.END)
        if prefix:
            self.prefix_entry.insert(0, prefix)
        self.example_label.config(text=self._get_example_text())
