"""
File utilities for project save/load and file operations
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


def save_project_to_file(state_dict: Dict[str, Any], file_path: Path) -> bool:
    """
    Save project state to JSON file
    
    Args:
        state_dict: Dictionary with project state
        file_path: Path to save file
        
    Returns:
        bool: Success status
    """
    try:
        project_data = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            **state_dict
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving project: {e}")
        return False


def load_project_from_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load project state from JSON file
    
    Args:
        file_path: Path to project file
        
    Returns:
        Optional[Dict]: Project state or None if failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        return project_data
    except Exception as e:
        print(f"Error loading project: {e}")
        return None


def generate_audio_filename(text: str) -> str:
    """
    Generate filename from text and timestamp
    Format: YYYYMMDD_HHMMSS_first_5_words.wav
    
    Args:
        text: Input text
        
    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get first 5 words
    words = text.strip().split()[:5]
    words_part = "_".join(words).lower()
    
    # Remove special characters
    words_part = "".join(c if c.isalnum() or c == "_" else "" for c in words_part)
    
    # Limit length
    if len(words_part) > 50:
        words_part = words_part[:50]
    
    return f"{timestamp}_{words_part}.wav"


def ensure_folder_exists(folder_path: Path) -> bool:
    """
    Ensure folder exists, create if not
    
    Args:
        folder_path: Path to folder
        
    Returns:
        bool: Success status
    """
    try:
        folder_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating folder: {e}")
        return False
