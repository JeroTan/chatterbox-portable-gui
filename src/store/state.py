"""
Application State Management
Similar to Redux/Zustand in JavaScript
"""

from typing import Optional, Dict, Any
from pathlib import Path


class AppState:
    """
    Global application state manager
    Similar to React state or Vuex store
    """
    
    def __init__(self):
        # Text input
        self.text_input: str = ""
        
        # Language settings
        self.language_code: str = "en"
        self.language_name: str = "English"
        
        # Voice settings
        self.voice_mode: str = "predefined"  # or "custom"
        self.selected_voice: str = "Default Voice (Female, Neutral)"
        self.custom_audio_path: Optional[Path] = None
        
        # Expression settings
        self.expression_mode: str = "text"  # or "parameters"
        self.expression_text: str = ""
        self.emotion: str = "Neutral"
        self.energy: int = 50
        self.speed: float = 1.0
        self.pitch: int = 0
        self.emphasis: int = 30
        
        # Output settings
        self.output_folder: Path = Path("./outputs")
        
        # Generated audio
        self.generated_audio_path: Optional[Path] = None
        
        # Project management
        self.current_project_path: Optional[Path] = None
        self.unsaved_changes: bool = False
        
        # Observers (for UI updates)
        self._observers = []
    
    def update(self, **kwargs):
        """
        Update state and notify observers
        Usage: state.update(text_input="new text", energy=75)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.unsaved_changes = True
        self._notify_observers()
    
    def get_state_dict(self) -> Dict[str, Any]:
        """Get state as dictionary for saving"""
        return {
            "text_input": self.text_input,
            "language_code": self.language_code,
            "language_name": self.language_name,
            "voice_mode": self.voice_mode,
            "selected_voice": self.selected_voice,
            "custom_audio_path": str(self.custom_audio_path) if self.custom_audio_path else None,
            "expression_mode": self.expression_mode,
            "expression_text": self.expression_text,
            "emotion": self.emotion,
            "energy": self.energy,
            "speed": self.speed,
            "pitch": self.pitch,
            "emphasis": self.emphasis,
            "output_folder": str(self.output_folder),
        }
    
    def load_state_dict(self, state_dict: Dict[str, Any]):
        """Load state from dictionary"""
        for key, value in state_dict.items():
            if hasattr(self, key):
                if key in ["custom_audio_path", "output_folder"] and value:
                    setattr(self, key, Path(value))
                else:
                    setattr(self, key, value)
        
        self.unsaved_changes = False
        self._notify_observers()
    
    def subscribe(self, observer):
        """Add observer for state changes"""
        self._observers.append(observer)
    
    def _notify_observers(self):
        """Notify all observers of state change"""
        for observer in self._observers:
            observer()
    
    def mark_saved(self):
        """Mark current state as saved"""
        self.unsaved_changes = False
        self._notify_observers()


# Global state instance
app_state = AppState()
