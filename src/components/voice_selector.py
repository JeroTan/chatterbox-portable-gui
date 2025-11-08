"""
Voice Selector Component
Dynamically loads voices from reference_voices/[language]/ folder
Keeps the fancy dropdown UI with grid layout
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional, Dict, List
from pathlib import Path
from .dropdown import DropdownComponent


class VoiceSelectorComponent:
    """
    Voice selector that loads voices from assets/reference_voices/[lang]/
    Uses fancy dropdown with Male/Female filtering
    """
    
    def __init__(
        self,
        parent,
        current_language: str = "en",
        on_voice_change: Optional[Callable] = None
    ):
        """
        Args:
            parent: Parent tkinter widget
            current_language: Current selected language code
            on_voice_change: Callback when voice changes
        """
        self.current_language = current_language
        self.on_voice_change = on_voice_change
        self.reference_voices_path = Path("src/assets/reference_voices")
        self.current_filter = "All"
        
        # Load voices for current language
        self._load_voices_for_language(current_language)
        
        # Container frame
        self.frame = ttk.LabelFrame(parent, text="Voice Selection", padding="10")
        
        # Voice mode selection
        mode_frame = ttk.Frame(self.frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.voice_mode = tk.StringVar(value="predefined")
        
        ttk.Radiobutton(
            mode_frame,
            text="Predefined Voice",
            variable=self.voice_mode,
            value="predefined",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            mode_frame,
            text="Custom Voice (Upload Audio to Clone Voice)",
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
        
        # Create filter buttons
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
        
        # Default to first male voice if available
        default_voice = ""
        if self.predefined_voices.get("Male"):
            default_voice = self.predefined_voices["Male"][0]
        elif self.predefined_voices.get("All"):
            default_voice = self.predefined_voices["All"][0]
        
        # Use fancy Dropdown component
        self.voice_dropdown = DropdownComponent(
            parent=self.predefined_frame,
            items=self.predefined_voices["All"],
            label="Selected Voice:",
            default_value=default_voice,
            on_select=self._handle_voice_selection,
            button_width=35,
            popup_width=500,
            popup_height=350,
            columns=3
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
    
    def _load_voices_for_language(self, lang_code: str):
        """Load voices from reference_voices/[lang]/ folder"""
        lang_folder = self.reference_voices_path / lang_code
        
        all_voices = []
        male_voices = []
        female_voices = []
        self.voice_files = {}
        
        if lang_folder.exists():
            # Get all audio files
            audio_files = sorted(lang_folder.glob("*.wav")) + sorted(lang_folder.glob("*.flac"))
            
            for audio_file in audio_files:
                # Just use the filename (without extension) as the voice name
                voice_name = audio_file.stem
                all_voices.append(voice_name)
                self.voice_files[voice_name] = audio_file
                
                # Filter by male/female based on filename
                if "male" in voice_name.lower() and "female" not in voice_name.lower():
                    male_voices.append(voice_name)
                elif "female" in voice_name.lower():
                    female_voices.append(voice_name)
        
        # If no voices found, add placeholder
        if not all_voices:
            all_voices = ["No voices available"]
        
        self.predefined_voices = {
            "All": all_voices,
            "Male": male_voices if male_voices else all_voices,
            "Female": female_voices if female_voices else all_voices
        }
    
    def update_language(self, lang_code: str):
        """Update voices when language changes"""
        self.current_language = lang_code
        self._load_voices_for_language(lang_code)
        
        # Update dropdown items
        current_filter = self.current_filter
        self.voice_dropdown.items = self.predefined_voices[current_filter]
        
        # Select first voice in new language
        if self.predefined_voices[current_filter]:
            self.voice_dropdown.set_value(self.predefined_voices[current_filter][0])
        
        self._trigger_callback()
    
    def _handle_voice_selection(self, voice: str):
        """Handle voice selection from dropdown"""
        self._trigger_callback()
    
    def _set_filter(self, filter_name: str):
        """Set the gender filter and update voice list"""
        self.current_filter = filter_name
        
        # Get filtered voices
        filtered_voices = self.predefined_voices[filter_name]
        current_voice = self.voice_dropdown.get_value()
        
        # Update dropdown items
        self.voice_dropdown.items = filtered_voices
        
        # If current voice not in filter, select first one
        if current_voice not in filtered_voices and filtered_voices:
            self.voice_dropdown.set_value(filtered_voices[0])
        
        # Update button styles
        self._update_filter_buttons()
        
        self._trigger_callback()
    
    def _update_filter_buttons(self):
        """Update filter button styles"""
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
            selected_voice = self.voice_dropdown.get_value()
            voice_file = self.voice_files.get(selected_voice)
            
            return {
                "mode": "predefined",
                "voice": selected_voice,
                "voice_file": voice_file,
                "custom_path": None
            }
        else:
            path = self.custom_path_var.get()
            return {
                "mode": "custom",
                "voice": None,
                "voice_file": None,
                "custom_path": Path(path) if path != "No file selected" else None
            }
    
    def set_voice_config(self, mode: str, voice: Optional[str] = None, 
                        custom_path: Optional[Path] = None):
        """Set voice configuration"""
        self.voice_mode.set(mode)
        self._on_mode_change()
        
        if mode == "predefined" and voice:
            if voice in self.predefined_voices["All"]:
                self.voice_dropdown.set_value(voice)
        elif mode == "custom" and custom_path:
            self.custom_path_var.set(str(custom_path))
    
    def apply_theme(self, theme: dict):
        """Apply theme colors to this component"""
        # Stub - components will be themed via ttk styles
        pass
