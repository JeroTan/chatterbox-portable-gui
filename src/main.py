"""
Chatterbox TTS GUI - Main Application
Copyright (C) 2025 JeroTan
Licensed under GNU GPL v3 - see LICENSE file

Desktop Window for Chatterbox TTS
Built with Tkinter for a native desktop experience
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import tempfile
import threading

# Import components
from components.text_input import TextInputComponent
from components.language_selector import LanguageSelectorComponent
from components.voice_selector import VoiceSelectorComponent
from components.expression_controls import ExpressionControlsComponent
from components.device_selector import DeviceSelector
from components.loading_screen import LoadingScreen
from components.audio_player import AudioPlayerComponent

# Import features
from features.generate import tts_generator
from features.project import save_project, load_project, new_project
from features.export import export_audio, preview_audio

# Import utilities
from utils.config import *
from utils.file_utils import generate_audio_filename, ensure_folder_exists
from store.state import app_state


class ChatterboxApp:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Hide main window initially
        self.root.withdraw()
        
        # Flag to prevent duplicate generation
        self.is_generating = False
        
        # Flag to prevent infinite loops when syncing UI
        self.is_syncing = False
        
        self._setup_menu()
        self._setup_ui()
        self._setup_keyboard_shortcuts()
        
        app_state.subscribe(self._on_state_change)
        
        print("✅ Chatterbox TTS Desktop App Ready!")
        
        # Show device selector immediately after window is ready
        self.root.after(100, self._show_device_selector)
    
    def _setup_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self._new_project, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self._open_project, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self._save_project, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self._save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        
        audio_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Audio", menu=audio_menu)
        audio_menu.add_command(label="Generate", command=self._generate_audio)
        audio_menu.add_command(label="Preview", command=self._preview_audio)
        audio_menu.add_command(label="Export...", command=self._export_audio)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _setup_ui(self):
        """Create UI layout"""
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left: inputs
        left = ttk.Frame(main_container)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.text_input = TextInputComponent(left, on_generate=self._generate_audio, on_text_change=self._on_text_change)
        self.text_input.frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.language_selector = LanguageSelectorComponent(
            left, 
            SUPPORTED_LANGUAGES, 
            DEFAULT_LANGUAGE, 
            on_language_change=self._on_language_change
        )
        self.language_selector.frame.pack(fill=tk.X, pady=(0, 10))
        
        self.voice_selector = VoiceSelectorComponent(left, current_language=DEFAULT_LANGUAGE, on_voice_change=self._on_voice_change)
        self.voice_selector.frame.pack(fill=tk.X, pady=(0, 10))
        
        self.expression_controls = ExpressionControlsComponent(left, EMOTION_OPTIONS, on_expression_change=self._on_expression_change)
        self.expression_controls.frame.pack(fill=tk.X)  # Changed: Don't expand vertically - keep text input size stable
        
        # Right: actions
        right = ttk.Frame(main_container, width=300)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right.pack_propagate(False)
        
        # Output folder
        output_frame = ttk.LabelFrame(right, text="Output", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_folder_var = tk.StringVar(value=str(OUTPUT_FOLDER))
        ttk.Entry(output_frame, textvariable=self.output_folder_var, state="readonly").pack(fill=tk.X, pady=(0, 5))
        ttk.Button(output_frame, text="Browse...", command=self._browse_output_folder).pack(fill=tk.X)
        
        # Generate button
        self.generate_btn = ttk.Button(right, text="🎤 Generate (Enter)", command=self._generate_audio)
        self.generate_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Audio player (built-in preview)
        self.audio_player = AudioPlayerComponent(right)
        self.audio_player.frame.pack(fill=tk.X, pady=(0, 10))
        
        # Export button
        self.export_btn = ttk.Button(right, text="💾 Export Audio", command=self._export_audio, state=tk.DISABLED)
        self.export_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Status bar
        status_bar = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = ttk.Label(status_bar, text="Ready", padding="2")
        self.status_label.pack(side=tk.LEFT)
    
    def _setup_keyboard_shortcuts(self):
        """Setup shortcuts"""
        self.root.bind(SHORTCUTS["save"], lambda e: self._save_project())
        self.root.bind(SHORTCUTS["open"], lambda e: self._open_project())
        self.root.bind(SHORTCUTS["new"], lambda e: self._new_project())
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _on_state_change(self):
        """Update UI on state change"""
        # Skip if we're currently syncing to prevent infinite loops
        if self.is_syncing:
            return
            
        title = APP_NAME
        if app_state.current_project_path:
            title += f" - {app_state.current_project_path.name}"
        if app_state.unsaved_changes:
            title += " *"
        self.root.title(title)
    
    def _show_device_selector(self):
        """Show device selector and then initialize models"""
        # Show device selector
        device_selector = DeviceSelector(self.root)
        selected_device = device_selector.show()
        
        # If user closed the dialog without selecting, exit the app
        if selected_device is None:
            print("⚠️ Device selection cancelled. Exiting app...")
            self.root.quit()
            return
        
        # Store the selected device
        self.selected_device = selected_device
        print(f"🎯 Selected device: {selected_device.upper()}")
        
        # Give a brief moment before showing loading screen
        self.root.after(100, self._initialize_tts_models)
    
    def _sync_ui_with_state(self):
        """Sync UI components with current app state"""
        # Set syncing flag to prevent infinite loops
        if self.is_syncing:
            return
        
        self.is_syncing = True
        
        try:
            # Update language selector FIRST (before text input)
            if hasattr(self, 'language_selector'):
                # Language selector will update voice selector automatically
                self.language_selector.set_language(app_state.language_code)
            
            # Update voice selector
            if hasattr(self, 'voice_selector'):
                self.voice_selector.set_voice_config(
                    mode=app_state.voice_mode,
                    voice=app_state.selected_voice,
                    custom_path=app_state.custom_audio_path
                )
            
            # Update expression controls
            if hasattr(self, 'expression_controls'):
                config = {
                    "mode": app_state.expression_mode,
                    "text": app_state.expression_text,
                    "energy": app_state.energy,
                    "speed": app_state.speed,
                    "pitch": app_state.pitch,
                    "emphasis": app_state.emphasis
                }
                
                # Add preset if in preset mode
                if app_state.expression_mode == "preset":
                    config["preset"] = app_state.selected_preset
                
                self.expression_controls.set_expression_config(config)
            
            # Update output folder
            if hasattr(self, 'output_folder_var'):
                self.output_folder_var.set(str(app_state.output_folder))
            
            # Update text input LAST to avoid it being cleared by other component callbacks
            if hasattr(self, 'text_input'):
                # Always set text, even if empty (don't use "if app_state.text_input" as it's False for empty strings)
                text = app_state.text_input if app_state.text_input else ""
                if text:
                    self.text_input.set_text(text)
                else:
                    self.text_input.clear()
                
        except Exception as e:
            print(f"⚠️ Error syncing UI with state: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Always clear the syncing flag
            self.is_syncing = False
    
    # Initialization
    def _initialize_tts_models(self):
        """Initialize TTS models with loading screen"""
        # Create and show loading screen
        loading_screen = LoadingScreen(self.root)
        loading_screen.show()
        
        # Initialize models with the selected device
        success = tts_generator.initialize(loading_screen, force_device=self.selected_device)
        
        # Close loading screen
        if loading_screen.window and loading_screen.window.winfo_exists():
            loading_screen.close()
        
        # Show main window after loading is complete
        self.root.deiconify()
        
        if not success:
            if not loading_screen.is_stopped():
                messagebox.showerror(
                    "Initialization Error",
                    "Failed to load TTS models. Some features may not work."
                )
    
    # Event handlers
    def _generate_audio(self):
        # Prevent duplicate generation if already generating
        if self.is_generating:
            print("⚠️ Generation already in progress, ignoring duplicate request")
            return
        
        text = self.text_input.get_text()
        if not text:
            messagebox.showwarning("No Text", "Enter text first")
            return
        
        # Set generating flag
        self.is_generating = True
        
        # Disable all buttons during generation
        self._set_ui_enabled(False)
        self.status_label.config(text="Generating... 0%")
        self.root.update()
        
        # Use temporary file for preview
        temp_file = Path(tempfile.gettempdir()) / f"chatterbox_preview_{generate_audio_filename(text)}"
        
        def progress_callback(percentage, status):
            """Update UI with progress - safe for threads"""
            self.root.after(0, lambda p=percentage, s=status: self.status_label.config(text=f"{s} {int(p)}%"))
        
        def generate_in_thread():
            """Generate audio in background thread"""
            try:
                voice_config = self.voice_selector.get_voice_config()
                expression_config = self.expression_controls.get_expression_config()
                
                result_path = tts_generator.generate_audio(
                    text, 
                    voice_config, 
                    expression_config, 
                    temp_file,
                    app_state.language_code,
                    progress_callback
                )
                
                # Update UI on main thread
                self.root.after(0, lambda: self._on_generation_complete(result_path, temp_file))
                
            except Exception as e:
                self.root.after(0, lambda: self._on_generation_error(e))
        
        # Start generation in background thread
        thread = threading.Thread(target=generate_in_thread, daemon=True)
        thread.start()
    
    def _on_generation_complete(self, result_path, temp_file):
        """Handle successful audio generation"""
        if result_path:
            app_state.update(generated_audio_path=result_path)
            self.audio_player.load_audio(result_path)
            self.export_btn.config(state=tk.NORMAL)
            self.status_label.config(text="✅ Generation complete!")
        else:
            self.status_label.config(text="❌ Generation failed")
            messagebox.showerror("Generation Failed", "Failed to generate audio. Check console for details.")
        
        # Clear generating flag
        self.is_generating = False
        
        # Re-enable UI
        self._set_ui_enabled(True)
    
    def _on_generation_error(self, error):
        """Handle generation error"""
        self.status_label.config(text="❌ Error")
        messagebox.showerror("Error", f"Error generating audio:\n{str(error)}")
        
        # Clear generating flag
        self.is_generating = False
        
        self._set_ui_enabled(True)
    
    def _set_ui_enabled(self, enabled: bool):
        """Enable or disable UI controls"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.generate_btn.config(state=state)
        self.text_input.text_widget.config(state=state)
        # Note: Components don't expose enable/disable yet, but generate button is the main one
    
    def _preview_audio(self):
        if app_state.generated_audio_path:
            preview_audio(app_state.generated_audio_path)
    
    def _export_audio(self):
        if not app_state.generated_audio_path:
            return
        
        # Disable buttons during export
        self.export_btn.config(state=tk.DISABLED)
        self.generate_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Exporting audio...")
        self.root.update()
        
        try:
            # Generate filename from text or use default
            default_filename = app_state.generated_audio_path.name
            
            # Use the output folder directly
            output_folder = Path(self.output_folder_var.get())
            export_path = output_folder / default_filename
            
            # If file exists, add number suffix
            counter = 1
            while export_path.exists():
                stem = default_filename.rsplit('.', 1)[0]
                ext = default_filename.rsplit('.', 1)[1] if '.' in default_filename else 'wav'
                export_path = output_folder / f"{stem}_{counter}.{ext}"
                counter += 1
            
            # Copy temp file to output folder
            export_audio(app_state.generated_audio_path, export_path)
            
            self.status_label.config(text=f"✅ Exported: {export_path.name}")
            
        except Exception as e:
            self.status_label.config(text="❌ Export failed")
            messagebox.showerror("Export Error", f"Failed to export audio:\n{str(e)}")
        finally:
            # Re-enable buttons
            self.export_btn.config(state=tk.NORMAL)
            self.generate_btn.config(state=tk.NORMAL)
    
    def _browse_output_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_folder_var.get())
        if folder:
            self.output_folder_var.set(folder)
            app_state.update(output_folder=Path(folder))
    
    def _on_language_change(self, language_code: str, language_name: str):
        """Handle language selection change"""
        app_state.update(language_code=language_code, language_name=language_name)
        # Update voice selector to show voices for new language
        self.voice_selector.update_language(language_code)
    
    def _on_text_change(self, text: str):
        """Handle text input change"""
        # Skip if syncing OR if state is loading to prevent infinite loops and overwrites
        if self.is_syncing or app_state._loading:
            print(f"⏭️ Skipping text change (syncing={self.is_syncing}, loading={app_state._loading})")
            return
            
        print(f"💬 Text changed: {len(text)} characters")
        app_state.update(text_input=text)
    
    def _on_voice_change(self):
        config = self.voice_selector.get_voice_config()
        # Use voice_file (actual path) instead of voice name
        voice_path = config.get("voice_file") or config.get("custom_path")
        app_state.update(voice_mode=config["mode"], selected_voice=config["voice"], custom_audio_path=voice_path)
    
    def _on_expression_change(self):
        config = self.expression_controls.get_expression_config()
        if config["mode"] == "text":
            app_state.update(expression_mode="text", expression_text=config["text"])
        elif config["mode"] == "preset":
            # Save preset selection and its parameter values
            app_state.update(
                expression_mode="preset",
                selected_preset=config.get("preset", "🎭 Default (Neutral)"),
                energy=config.get("energy", 0.70),
                speed=config.get("speed", 0.40),
                emphasis=config.get("emphasis", 0.90),
                pitch=config.get("pitch", 0)
            )
        else:  # parameters
            app_state.update(expression_mode="parameters", **{k: v for k, v in config.items() if k != "mode"})
    
    # Project management
    def _new_project(self):
        new_project()
        # Sync UI after creating new project
        self._sync_ui_with_state()
    
    def _open_project(self):
        # Show "Loading..." in text input before opening file dialog
        if hasattr(self, 'text_input'):
            self.text_input.set_text("Loading save file...")
            self.root.update()  # Force UI update
        
        file_path = filedialog.askopenfilename(
            title="Open Project", 
            filetypes=PROJECT_FORMATS, 
            defaultextension=".cbx",
            initialdir=PROJECTS_FOLDER
        )
        
        if file_path:
            success = load_project(Path(file_path))
            if success:
                # Sync UI after loading project
                self._sync_ui_with_state()
        else:
            # User cancelled - restore previous state or clear loading message
            if hasattr(self, 'text_input'):
                if app_state.text_input:
                    self.text_input.set_text(app_state.text_input)
                else:
                    self.text_input.clear()
    
    def _save_project(self):
        if app_state.current_project_path:
            save_project()
        else:
            self._save_project_as()
    
    def _save_project_as(self):
        file_path = filedialog.asksaveasfilename(title="Save As", defaultextension=".cbx", filetypes=PROJECT_FORMATS, initialdir=PROJECTS_FOLDER)
        if file_path:
            save_project(Path(file_path))
    
    def _on_close(self):
        if app_state.unsaved_changes:
            response = messagebox.askyesnocancel("Unsaved Changes", "Save before closing?")
            if response is None:
                return
            elif response:
                self._save_project()
        tts_generator.cleanup()
        self.root.destroy()
    
    def _show_about(self):
        messagebox.showinfo("About", f"{APP_NAME}\nVersion {APP_VERSION}\n\nModular desktop TTS app\nby {APP_AUTHOR}")
    
    def run(self):
        self.root.mainloop()


def main():
    app = ChatterboxApp()
    app.run()


if __name__ == "__main__":
    main()
