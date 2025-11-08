"""
Resource Path Helper for PyInstaller
Handles finding bundled assets in both development and frozen (PyInstaller) environments
"""

import sys
import os
from pathlib import Path


def get_resource_path(relative_path: str) -> Path:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    
    When running from source: uses src/assets/
    When running as .exe: uses bundled _MEIPASS/assets/
    
    Args:
        relative_path: Path relative to assets folder (e.g., "reference_voices/en/voice1.wav")
    
    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
        asset_path = base_path / "assets" / relative_path
    except AttributeError:
        # Running in normal Python environment
        base_path = Path(__file__).parent.parent
        asset_path = base_path / "assets" / relative_path
    
    return asset_path


def get_assets_dir() -> Path:
    """
    Get the assets directory path
    
    Returns:
        Path to assets folder
    """
    try:
        # PyInstaller environment
        base_path = Path(sys._MEIPASS)
        return base_path / "assets"
    except AttributeError:
        # Development environment
        return Path(__file__).parent.parent / "assets"


def get_reference_voices_dir() -> Path:
    """
    Get the reference voices directory
    
    Returns:
        Path to reference_voices folder
    """
    return get_assets_dir() / "reference_voices"


def resource_exists(relative_path: str) -> bool:
    """
    Check if a resource exists
    
    Args:
        relative_path: Path relative to assets folder
    
    Returns:
        True if resource exists
    """
    return get_resource_path(relative_path).exists()
