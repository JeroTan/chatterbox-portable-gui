import tkinter as tk
from tkinter import ttk
import torch

class DeviceSelector:
    def __init__(self, parent):
        self.parent = parent
        self.selected_device = None
        self.dialog = None
        
    def show(self):
        """Show the device selection dialog and return the selected device"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Select Processing Device")
        self.dialog.resizable(False, False)
        
        # Apply dark theme colors
        dark_bg = "#2d2d30"
        dark_fg = "#d4d4d4"
        
        self.dialog.config(bg=dark_bg)
        
        # Handle window close button (X) - return None to exit app
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: self._close_dialog())
        
        # Make it always on top and focused
        self.dialog.attributes('-topmost', True)
        self.dialog.focus_force()
        
        # Main container with dark background
        main_frame = tk.Frame(self.dialog, bg=dark_bg, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Choose Processing Device",
            font=("Segoe UI", 16, "bold"),
            bg=dark_bg,
            fg=dark_fg
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = tk.Label(
            main_frame,
            text="Select which device to use for audio generation:",
            font=("Segoe UI", 10),
            bg=dark_bg,
            fg=dark_fg
        )
        desc_label.pack(pady=(0, 20))
        
        # Check GPU availability
        gpu_available = torch.cuda.is_available()
        gpu_name = torch.cuda.get_device_name(0) if gpu_available else "No GPU detected"
        
        # CPU Option (First choice - Recommended)
        cpu_frame = tk.LabelFrame(
            main_frame, 
            text="CPU (Recommended)", 
            bg=dark_bg,
            fg=dark_fg,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=15
        )
        cpu_frame.pack(fill=tk.X, pady=(0, 10))
        
        cpu_info = tk.Label(
            cpu_frame,
            text="🐌 Slower generation (10-60 seconds)\n✓ More stable and reliable",
            font=("Segoe UI", 9),
            bg=dark_bg,
            fg=dark_fg,
            justify=tk.LEFT
        )
        cpu_info.pack(anchor=tk.W, pady=(0, 10))
        
        cpu_button = tk.Button(
            cpu_frame,
            text="Use CPU",
            command=lambda: self._select_device("cpu"),
            width=20,
            bg="#0e639c",
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#1177bb",
            activeforeground="white"
        )
        cpu_button.pack()
        
        # GPU Option (Second choice)
        gpu_frame = tk.LabelFrame(
            main_frame, 
            text="GPU", 
            bg=dark_bg,
            fg=dark_fg,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=15
        )
        gpu_frame.pack(fill=tk.X, pady=(0, 10))
        
        gpu_info = tk.Label(
            gpu_frame,
            text=f"🚀 {gpu_name}\n{'✓ Fast generation (2-10 seconds)' if gpu_available else '✗ Not available on this system'}",
            font=("Segoe UI", 9),
            fg="#4ec9b0" if gpu_available else "#858585",
            bg=dark_bg,
            justify=tk.LEFT
        )
        gpu_info.pack(anchor=tk.W, pady=(0, 10))
        
        gpu_button = tk.Button(
            gpu_frame,
            text="Use GPU" if gpu_available else "GPU Not Available",
            command=lambda: self._select_device("cuda"),
            state=tk.NORMAL if gpu_available else tk.DISABLED,
            width=20,
            bg="#0e639c" if gpu_available else "#3c3c3c",
            fg="white" if gpu_available else "#858585",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            cursor="hand2" if gpu_available else "arrow",
            activebackground="#1177bb" if gpu_available else "#3c3c3c",
            activeforeground="white" if gpu_available else "#858585"
        )
        gpu_button.pack()
        
        # Auto-select GPU if available (for convenience)
        if gpu_available:
            note_label = tk.Label(
                main_frame,
                text="💡 Tip: CPU is more stable, but GPU is faster if you need quick results",
                font=("Segoe UI", 8),
                fg="#858585",
                bg=dark_bg
            )
            note_label.pack(pady=(10, 0))
        
        # Update window to calculate required size
        self.dialog.update_idletasks()
        
        # Set width and let height auto-adjust
        required_width = 500
        required_height = self.dialog.winfo_reqheight()
        
        # Center the dialog with calculated dimensions
        x = (self.dialog.winfo_screenwidth() // 2) - (required_width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (required_height // 2)
        self.dialog.geometry(f"{required_width}x{required_height}+{x}+{y}")
        
        # Wait for the dialog to close
        self.parent.wait_window(self.dialog)
        
        return self.selected_device
    
    def _select_device(self, device):
        """Handle device selection"""
        self.selected_device = device
        self.dialog.destroy()
    
    def _close_dialog(self):
        """Handle dialog close button (X) - exit without selecting"""
        self.selected_device = None
        self.dialog.destroy()
