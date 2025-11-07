"""
Project Management Feature
Save and load project files
"""

from pathlib import Path
from typing import Optional
from tkinter import messagebox

from utils.file_utils import save_project_to_file, load_project_from_file
from store.state import app_state


def save_project(file_path: Optional[Path] = None) -> bool:
    """
    Save current project state
    
    Args:
        file_path: Path to save to, or None to use current project path
        
    Returns:
        bool: Success status
    """
    # Use provided path or current project path
    save_path = file_path or app_state.current_project_path
    
    if not save_path:
        print("❌ No save path provided")
        return False
    
    try:
        # Get current state
        state_dict = app_state.get_state_dict()
        
        # Save to file
        success = save_project_to_file(state_dict, save_path)
        
        if success:
            app_state.current_project_path = save_path
            app_state.mark_saved()
            print(f"✅ Project saved: {save_path}")
            messagebox.showinfo("Success", f"Project saved successfully!\n{save_path.name}")
            return True
        else:
            messagebox.showerror("Error", "Failed to save project")
            return False
            
    except Exception as e:
        print(f"❌ Error saving project: {e}")
        messagebox.showerror("Error", f"Failed to save project:\n{str(e)}")
        return False


def load_project(file_path: Path) -> bool:
    """
    Load project from file
    
    Args:
        file_path: Path to project file
        
    Returns:
        bool: Success status
    """
    try:
        # Check for unsaved changes
        if app_state.unsaved_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before loading?"
            )
            
            if response is None:  # Cancel
                return False
            elif response:  # Yes, save
                if not save_project():
                    return False
        
        # Load from file
        project_data = load_project_from_file(file_path)
        
        if project_data:
            app_state.load_state_dict(project_data)
            app_state.current_project_path = file_path
            print(f"✅ Project loaded: {file_path}")
            messagebox.showinfo("Success", f"Project loaded successfully!\n{file_path.name}")
            return True
        else:
            messagebox.showerror("Error", "Failed to load project")
            return False
            
    except Exception as e:
        print(f"❌ Error loading project: {e}")
        messagebox.showerror("Error", f"Failed to load project:\n{str(e)}")
        return False


def new_project() -> bool:
    """
    Create new project (reset state)
    
    Returns:
        bool: Success status
    """
    try:
        # Check for unsaved changes
        if app_state.unsaved_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before creating a new project?"
            )
            
            if response is None:  # Cancel
                return False
            elif response:  # Yes, save
                if not save_project():
                    return False
        
        # Reset state
        app_state.__init__()
        print("✅ New project created")
        return True
        
    except Exception as e:
        print(f"❌ Error creating new project: {e}")
        messagebox.showerror("Error", f"Failed to create new project:\n{str(e)}")
        return False
