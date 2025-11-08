"""
Configuration and Constants
Centralized configuration for the Chatterbox TTS application
"""

from pathlib import Path

# ============================================
# APPLICATION INFO
# ============================================
APP_NAME = "Chatterbox TTS - Voice Generator"
APP_VERSION = "1.0.0"
APP_AUTHOR = "JeroTan"

# ============================================
# DEFAULT PATHS
# ============================================
BASE_DIR = Path(__file__).parent.parent
OUTPUT_FOLDER = BASE_DIR / "outputs"
PROJECTS_FOLDER = BASE_DIR / "projects"
REFERENCE_FOLDER = BASE_DIR / "reference_audio"

# Create folders if they don't exist
OUTPUT_FOLDER.mkdir(exist_ok=True)
PROJECTS_FOLDER.mkdir(exist_ok=True)
REFERENCE_FOLDER.mkdir(exist_ok=True)

# ============================================
# UI CONFIGURATION
# ============================================
# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600

# Colors (for styling)
PRIMARY_COLOR = "#4A90E2"
SUCCESS_COLOR = "#4CAF50"
ERROR_COLOR = "#F44336"
WARNING_COLOR = "#FF9800"
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#333333"

# ============================================
# VOICE OPTIONS
# ============================================
# Languages supported by Chatterbox TTS
SUPPORTED_LANGUAGES = {
    "ar": "Arabic",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "fi": "Finnish",
    "fr": "French",
    "he": "Hebrew",
    "hi": "Hindi",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "ms": "Malay",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "sv": "Swedish",
    "sw": "Swahili",
    "tr": "Turkish",
    "zh": "Chinese",
}

# Default language
DEFAULT_LANGUAGE = "en"

# Voices organized by gender for filtering
PREDEFINED_VOICES = {
    "Female": [
        "Default (Female, Neutral)",
        "Energetic Female",
        "Professional Female",
        "Young Girl",
        "Mature Woman",
        "Narrator - Female (Calm)",
        "Character - High Pitched",
    ],
    "Male": [
        "Default (Male, Neutral)",
        "Professional Male",
        "Deep Male Voice",
        "Young Boy",
        "Old Man",
        "Narrator - Male (Epic)",
        "Character - Deep",
    ],
    "All": []  # Will be populated with all voices
}

# Populate "All" with all voices
PREDEFINED_VOICES["All"] = (
    PREDEFINED_VOICES["Female"] + PREDEFINED_VOICES["Male"]
)

# ============================================
# EXPRESSION OPTIONS
# ============================================
EMOTION_OPTIONS = [
    "Neutral",
    "Happy",
    "Sad",
    "Angry",
    "Excited",
    "Calm",
    "Fearful"
]

# Parameter ranges
ENERGY_RANGE = (0, 100)
SPEED_RANGE = (0.5, 2.0)
PITCH_RANGE = (-12, 12)
EMPHASIS_RANGE = (0, 100)

# ============================================
# FILE SETTINGS
# ============================================
AUDIO_FORMATS = [
    ("WAV Files", "*.wav"),
    ("MP3 Files", "*.mp3"),
    ("FLAC Files", "*.flac"),
    ("All Audio Files", "*.wav *.mp3 *.flac"),
]

PROJECT_FORMATS = [
    ("Chatterbox Projects", "*.cbx"),
    ("JSON Files", "*.json"),
    ("All Files", "*.*"),
]

# ============================================
# KEYBOARD SHORTCUTS
# ============================================
SHORTCUTS = {
    "generate": "<Return>",  # Enter key
    "new_line": "<Shift-Return>",  # Shift+Enter
    "save": "<Control-s>",  # Ctrl+S
    "open": "<Control-o>",  # Ctrl+O
    "new": "<Control-n>",  # Ctrl+N
}
