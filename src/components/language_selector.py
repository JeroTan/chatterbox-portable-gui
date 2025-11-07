"""
Language Selector Component
Select target language for TTS generation
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict
from .dropdown import DropdownComponent


class LanguageSelectorComponent:
    """
    Language selection component using reusable Dropdown
    Like React - import component, pass props!
    """
    
    def __init__(
        self,
        parent,
        languages: Dict[str, str],  # {"en": "English", ...}
        default_language: str = "en",
        on_language_change: Optional[Callable[[str, str], None]] = None
    ):
        """
        Args:
            parent: Parent tkinter widget
            languages: Dict of language codes to names
            default_language: Default language code
            on_language_change: Callback when language changes (code, name)
        """
        self.languages = languages
        self.on_language_change = on_language_change
        
        # Create reverse mapping (name -> code)
        self.name_to_code = {name: code for code, name in languages.items()}
        
        # Container frame
        self.frame = ttk.LabelFrame(parent, text="Language Preference", padding="10")
        
        # Create sorted list of language names
        language_names = sorted(languages.values())
        default_name = languages.get(default_language, language_names[0])
        
        # Use reusable Dropdown component (like importing in React!)
        self.dropdown = DropdownComponent(
            parent=self.frame,
            items=language_names,
            label="Select Language:",
            default_value=default_name,
            on_select=self._handle_selection,  # Event handler
            button_width=35,
            popup_width=500,
            popup_height=400,
            columns=3  # Grid layout
        )
        self.dropdown.frame.pack(fill=tk.X)
    
    def _handle_selection(self, language_name: str):
        """Handle dropdown selection (like onChange handler)"""
        language_code = self.name_to_code.get(language_name)
        
        if self.on_language_change and language_code:
            self.on_language_change(language_code, language_name)
    
    def get_language_code(self) -> str:
        """Get current selected language code"""
        language_name = self.dropdown.get_value()
        return self.name_to_code.get(language_name, "en")
    
    def get_language_name(self) -> str:
        """Get current selected language name"""
        return self.dropdown.get_value()
    
    def set_language(self, language_code: str):
        """Set the selected language by code"""
        language_name = self.languages.get(language_code)
        if language_name:
            self.dropdown.set_value(language_name)


