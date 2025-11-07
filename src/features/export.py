"""
Audio Export Feature
Handle audio export in various formats
"""

from pathlib import Path
from typing import Optional
from tkinter import messagebox
import shutil


def export_audio(
    source_audio: Path,
    destination: Path,
    format: str = "wav"
) -> bool:
    """
    Export generated audio to specified location and format
    
    Args:
        source_audio: Path to source audio file
        destination: Destination path
        format: Audio format (wav, mp3, flac)
        
    Returns:
        bool: Success status
    """
    try:
        if not source_audio.exists():
            messagebox.showerror("Error", "Source audio file not found")
            return False
        
        # Ensure destination has correct extension
        dest_path = Path(destination)
        if dest_path.suffix.lower() != f".{format}":
            dest_path = dest_path.with_suffix(f".{format}")
        
        # TODO: If format conversion is needed, use pydub or similar
        # For now, just copy if same format
        if source_audio.suffix.lower() == dest_path.suffix.lower():
            shutil.copy2(source_audio, dest_path)
            print(f"✅ Audio exported: {dest_path}")
            messagebox.showinfo("Success", f"Audio exported successfully!\n{dest_path.name}")
            return True
        else:
            # TODO: Format conversion
            print("⚠️  Format conversion not yet implemented")
            messagebox.showwarning(
                "Not Implemented",
                "Format conversion is not yet implemented.\nOnly WAV export is currently supported."
            )
            return False
            
    except Exception as e:
        print(f"❌ Error exporting audio: {e}")
        messagebox.showerror("Error", f"Failed to export audio:\n{str(e)}")
        return False


def preview_audio(audio_path: Path) -> bool:
    """
    Preview audio using system default player
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        bool: Success status
    """
    try:
        if not audio_path.exists():
            messagebox.showerror("Error", "Audio file not found")
            return False
        
        # Open with system default
        import os
        import platform
        
        system = platform.system()
        
        if system == "Windows":
            os.startfile(audio_path)
        elif system == "Darwin":  # macOS
            os.system(f"open '{audio_path}'")
        else:  # Linux
            os.system(f"xdg-open '{audio_path}'")
        
        print(f"🔊 Opening audio: {audio_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error previewing audio: {e}")
        messagebox.showerror("Error", f"Failed to preview audio:\n{str(e)}")
        return False
