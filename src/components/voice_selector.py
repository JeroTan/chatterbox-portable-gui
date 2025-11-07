"""
Voice Selector Component
Predefined or custom voice selection with Male/Female filtering
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional, Dict, List
from pathlib import Path
from .dropdown import DropdownComponent


class VoiceSelectorComponent:
    """
    Voice selection component with predefined/custom modes
    Predefined voices can be filtered by Male/Female/All
    Uses reusable DropdownComponent (React-style!)
    """
    
    def __init__(
        self,
        parent,
        predefined_voices: Dict[str, List[str]],
        on_voice_change: Optional[Callable] = None
    ):
        """
        Args:
            parent: Parent tkinter widget
            predefined_voices: Dict with keys "Male", "Female", "All" and lists of voice names
            on_voice_change: Callback when voice changes
        """
        self.predefined_voices = predefined_voices
        self.on_voice_change = on_voice_change
        self.current_filter = "All"  # Default filter
        
        # Container frame
        self.frame = ttk.LabelFrame(parent, text="Voice Selection", padding="10")
        
        # Voice mode selection
        mode_frame = ttk.Frame(self.frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.voice_mode = tk.StringVar(value="predefined")
        
        ttk.Radiobutton(
            mode_frame,
            text="Predefined Voices",
            variable=self.voice_mode,
            value="predefined",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            mode_frame,
            text="Custom Voice (Reference Audio)",
            variable=self.voice_mode,
            value="custom",
            command=self._on_mode_change
        ).pack(side=tk.LEFT)
        
        # Predefined voice section
        self.predefined_frame = ttk.Frame(self.frame)
        self.predefined_frame.pack(fill=tk.X)
        
        # Gender filter tabs
        filter_frame = ttk.Frame(self.predefined_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=(0, 10))
        
        # Create filter buttons (like tabs)
        self.filter_buttons = {}
        for filter_name in ["All", "Male", "Female"]:
            btn = ttk.Button(
                filter_frame,
                text=filter_name,
                command=lambda f=filter_name: self._set_filter(f),
                width=8
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.filter_buttons[filter_name] = btn
        
        # Highlight current filter
        self._update_filter_buttons()
        
        # Use reusable Dropdown component (React-style!)
        default_voice = predefined_voices["All"][0] if predefined_voices["All"] else ""
        
        self.voice_dropdown = DropdownComponent(
            parent=self.predefined_frame,
            items=predefined_voices["All"],
            label="Selected Voice:",
            default_value=default_voice,
            on_select=self._handle_voice_selection,
            button_width=35,
            popup_width=500,
            popup_height=350,
            columns=3  # Grid layout
        )
        self.voice_dropdown.frame.pack(fill=tk.X, pady=(5, 0))
        
        # Custom voice file selector
        self.custom_frame = ttk.Frame(self.frame)
        
        self.custom_path_var = tk.StringVar(value="No file selected")
        
        ttk.Label(self.custom_frame, text="Audio File:").pack(side=tk.LEFT, padx=(0, 10))
        
        path_entry = ttk.Entry(
            self.custom_frame,
            textvariable=self.custom_path_var,
            state="readonly",
            width=30
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(
            self.custom_frame,
            text="Browse...",
            command=self._browse_audio_file
        ).pack(side=tk.LEFT)
    
    def _handle_voice_selection(self, voice: str):
        """Handle voice selection from dropdown (event handler)"""
        self._trigger_callback()
    
    def _set_filter(self, filter_name: str):
        """Set the gender filter and update voice list"""
        self.current_filter = filter_name
        
        # Get filtered voices
        filtered_voices = self.predefined_voices[filter_name]
        current_voice = self.voice_dropdown.get_value()
        
        # Update dropdown items (React-style: update props!)
        self.voice_dropdown.items = filtered_voices
        
        # If current voice not in new filter, select first one
        if current_voice not in filtered_voices and filtered_voices:
            self.voice_dropdown.set_value(filtered_voices[0])
        
        # Update button styles
        self._update_filter_buttons()
        
        # Trigger callback
        self._trigger_callback()
    
    def _update_filter_buttons(self):
        """Update filter button styles to highlight active filter"""
        for filter_name, button in self.filter_buttons.items():
            if filter_name == self.current_filter:
                button.state(['pressed', '!disabled'])
            else:
                button.state(['!pressed', '!disabled'])
    
    def _on_mode_change(self):
        """Handle voice mode change"""
        mode = self.voice_mode.get()
        
        if mode == "predefined":
            self.predefined_frame.pack(fill=tk.X)
            self.custom_frame.pack_forget()
        else:
            self.predefined_frame.pack_forget()
            self.custom_frame.pack(fill=tk.X)
        
        self._trigger_callback()
    
    def _browse_audio_file(self):
        """Open file dialog for custom audio"""
        file_path = filedialog.askopenfilename(
            title="Select Reference Audio",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.flac"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.custom_path_var.set(file_path)
            self._trigger_callback()
    
    def _trigger_callback(self):
        """Trigger voice change callback"""
        if self.on_voice_change:
            self.on_voice_change()
    
    def get_voice_config(self) -> dict:
        """Get current voice configuration"""
        mode = self.voice_mode.get()
        
        if mode == "predefined":
            return {
                "mode": "predefined",
                "voice": self.voice_dropdown.get_value(),
                "gender_filter": self.current_filter,
                "custom_path": None
            }
        else:
            path = self.custom_path_var.get()
            return {
                "mode": "custom",
                "voice": None,
                "gender_filter": None,
                "custom_path": Path(path) if path != "No file selected" else None
            }
    
    def set_voice_config(self, mode: str, voice: Optional[str] = None, 
                        gender_filter: Optional[str] = None, 
                        custom_path: Optional[Path] = None):
        """Set voice configuration"""
        self.voice_mode.set(mode)
        self._on_mode_change()
        
        if mode == "predefined":
            # Set filter if provided
            if gender_filter and gender_filter in ["All", "Male", "Female"]:
                self._set_filter(gender_filter)
            
            # Set voice if provided
            if voice:
                self.selected_voice_var.set(voice)
        elif mode == "custom" and custom_path:
            self.custom_path_var.set(str(custom_path))
