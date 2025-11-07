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
        
        # Handle window close button (X) - return None to exit app
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: self._close_dialog())
        
        # Make it always on top and focused
        self.dialog.attributes('-topmost', True)
        self.dialog.focus_force()
        
        # Main container
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Choose Processing Device",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Select which device to use for audio generation:",
            font=("Segoe UI", 10)
        )
        desc_label.pack(pady=(0, 20))
        
        # Check GPU availability
        gpu_available = torch.cuda.is_available()
        gpu_name = torch.cuda.get_device_name(0) if gpu_available else "No GPU detected"
        
        # CPU Option (First choice - Recommended)
        cpu_frame = ttk.LabelFrame(main_frame, text="CPU (Recommended)", padding="15")
        cpu_frame.pack(fill=tk.X, pady=(0, 10))
        
        cpu_info = ttk.Label(
            cpu_frame,
            text="🐌 Slower generation (10-60 seconds)\n✓ More stable and reliable",
            font=("Segoe UI", 9)
        )
        cpu_info.pack(anchor=tk.W, pady=(0, 10))
        
        cpu_button = ttk.Button(
            cpu_frame,
            text="Use CPU",
            command=lambda: self._select_device("cpu"),
            width=20
        )
        cpu_button.pack()
        
        # GPU Option (Second choice)
        gpu_frame = ttk.LabelFrame(main_frame, text="GPU", padding="15")
        gpu_frame.pack(fill=tk.X, pady=(0, 10))
        
        gpu_info = ttk.Label(
            gpu_frame,
            text=f"🚀 {gpu_name}\n{'✓ Fast generation (2-10 seconds)' if gpu_available else '✗ Not available on this system'}",
            font=("Segoe UI", 9),
            foreground="green" if gpu_available else "gray"
        )
        gpu_info.pack(anchor=tk.W, pady=(0, 10))
        
        gpu_button = ttk.Button(
            gpu_frame,
            text="Use GPU" if gpu_available else "GPU Not Available",
            command=lambda: self._select_device("cuda"),
            state=tk.NORMAL if gpu_available else tk.DISABLED,
            width=20
        )
        gpu_button.pack()
        
        # Auto-select GPU if available (for convenience)
        if gpu_available:
            note_label = ttk.Label(
                main_frame,
                text="💡 Tip: CPU is more stable, but GPU is faster if you need quick results",
                font=("Segoe UI", 8),
                foreground="gray"
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
