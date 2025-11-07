"""
Loading Screen Component
Shows progress while loading TTS models
"""

import tkinter as tk
from tkinter import ttk


class LoadingScreen:
    """
    Loading screen with progress bar and force stop button
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        self.should_stop = False
        
    def show(self):
        """Show the loading screen"""
        self.should_stop = False
        
        # Create toplevel window
        self.window = tk.Toplevel(self.parent)
        self.window.title("Loading Chatterbox TTS")
        self.window.geometry("500x280")
        self.window.resizable(False, False)
        
        # Make it always on top
        self.window.attributes('-topmost', True)
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (280 // 2)
        self.window.geometry(f"500x280+{x}+{y}")
        
        # Configure background
        self.window.configure(bg="#2b2b2b")
        
        # Main container
        container = tk.Frame(self.window, bg="#2b2b2b")
        container.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Title
        title_label = tk.Label(
            container,
            text="🚀 Loading Chatterbox TTS",
            font=("Segoe UI", 16, "bold"),
            bg="#2b2b2b",
            fg="white"
        )
        title_label.pack(pady=(0, 20))
        
        # Status label
        self.status_label = tk.Label(
            container,
            text="Initializing models...",
            font=("Segoe UI", 10),
            bg="#2b2b2b",
            fg="#cccccc"
        )
        self.status_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            container,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(0, 10))
        
        # Progress percentage label
        self.percentage_label = tk.Label(
            container,
            text="0%",
            font=("Segoe UI", 9),
            bg="#2b2b2b",
            fg="#888888"
        )
        self.percentage_label.pack(pady=(0, 20))
        
        # Force stop button
        self.stop_button = tk.Button(
            container,
            text="Force Stop and Close",
            command=self._on_force_stop,
            font=("Segoe UI", 10, "bold"),
            bg="#dc3545",
            fg="white",
            activebackground="#c82333",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            padx=30,
            pady=10
        )
        self.stop_button.pack(pady=(5, 0))
        
        # Update the window
        self.window.update()
        
    def update_progress(self, percentage: float, status: str = None):
        """
        Update the progress bar
        
        Args:
            percentage: Progress percentage (0-100)
            status: Optional status message
        """
        if self.window and self.window.winfo_exists():
            self.progress_var.set(percentage)
            self.percentage_label.config(text=f"{int(percentage)}%")
            
            if status:
                self.status_label.config(text=status)
            
            self.window.update()
    
    def _on_force_stop(self):
        """Handle force stop button click - stops loading and closes the app"""
        self.should_stop = True
        self.status_label.config(text="Stopping and closing app...", fg="#ff6b6b")
        self.stop_button.config(state=tk.DISABLED, bg="#666666")
        self.window.update()
        
        # Close the loading screen
        self.close()
        
        # Close the main app
        if self.parent:
            self.parent.quit()
            self.parent.destroy()
    
    def is_stopped(self) -> bool:
        """Check if user requested to stop"""
        return self.should_stop
    
    def close(self):
        """Close the loading screen"""
        if self.window and self.window.winfo_exists():
            self.window.grab_release()
            self.window.destroy()
            self.window = None
