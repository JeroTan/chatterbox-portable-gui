"""
Main Application - Desktop Window for Chatterbox TTS
Built with Tkinter for a native desktop experience
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# Import components
from components.text_input import TextInputComponent
from components.voice_selector import VoiceSelectorComponent
from components.expression_controls import ExpressionControlsComponent

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
        
        self._setup_menu()
        self._setup_ui()
        self._setup_keyboard_shortcuts()
        
        app_state.subscribe(self._on_state_change)
        
        print("✅ Chatterbox TTS Desktop App Ready!")
    
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
        
        self.text_input = TextInputComponent(left, on_generate=self._generate_audio)
        self.text_input.frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.voice_selector = VoiceSelectorComponent(left, PREDEFINED_VOICES, on_voice_change=self._on_voice_change)
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
        ttk.Button(right, text="🎤 Generate (Enter)", command=self._generate_audio).pack(fill=tk.X, pady=(0, 10))
        
        # Audio status
        audio_frame = ttk.LabelFrame(right, text="Generated Audio", padding="10")
        audio_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.audio_status_var = tk.StringVar(value="No audio yet")
        ttk.Label(audio_frame, textvariable=self.audio_status_var, wraplength=260).pack(fill=tk.X)
        
        btn_frame = ttk.Frame(audio_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.preview_btn = ttk.Button(btn_frame, text="🔊 Preview", command=self._preview_audio, state=tk.DISABLED)
        self.preview_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.export_btn = ttk.Button(btn_frame, text="💾 Export", command=self._export_audio, state=tk.DISABLED)
        self.export_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
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
        title = APP_NAME
        if app_state.current_project_path:
            title += f" - {app_state.current_project_path.name}"
        if app_state.unsaved_changes:
            title += " *"
        self.root.title(title)
    
    # Event handlers
    def _generate_audio(self):
        text = self.text_input.get_text()
        if not text:
            messagebox.showwarning("No Text", "Enter text first")
            return
        
        self.status_label.config(text="Generating...")
        self.root.update()
        
        try:
            voice_config = self.voice_selector.get_voice_config()
            expression_config = self.expression_controls.get_expression_config()
            filename = generate_audio_filename(text)
            output_path = Path(self.output_folder_var.get()) / filename
            ensure_folder_exists(output_path.parent)
            
            result_path = tts_generator.generate_audio(text, voice_config, expression_config, output_path)
            
            if result_path:
                app_state.update(generated_audio_path=result_path)
                self.audio_status_var.set(f"✅ {result_path.name}")
                self.preview_btn.config(state=tk.NORMAL)
                self.export_btn.config(state=tk.NORMAL)
                self.status_label.config(text="Generated")
            else:
                self.status_label.config(text="Failed")
                messagebox.showinfo("Not Implemented", "TTS integration pending.\nThis UI shows the modular structure.")
        except Exception as e:
            self.status_label.config(text="Error")
            messagebox.showerror("Error", str(e))
    
    def _preview_audio(self):
        if app_state.generated_audio_path:
            preview_audio(app_state.generated_audio_path)
    
    def _export_audio(self):
        if not app_state.generated_audio_path:
            return
        file_path = filedialog.asksaveasfilename(
            title="Export Audio",
            defaultextension=".wav",
            filetypes=AUDIO_FORMATS,
            initialfile=app_state.generated_audio_path.name
        )
        if file_path:
            export_audio(app_state.generated_audio_path, Path(file_path))
    
    def _browse_output_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_folder_var.get())
        if folder:
            self.output_folder_var.set(folder)
            app_state.update(output_folder=Path(folder))
    
    def _on_voice_change(self):
        config = self.voice_selector.get_voice_config()
        app_state.update(voice_mode=config["mode"], selected_voice=config["voice"], custom_audio_path=config["custom_path"])
    
    def _on_expression_change(self):
        config = self.expression_controls.get_expression_config()
        if config["mode"] == "text":
            app_state.update(expression_mode="text", expression_text=config["text"])
        else:
            app_state.update(expression_mode="parameters", **{k: v for k, v in config.items() if k != "mode"})
    
    # Project management
    def _new_project(self):
        new_project()
    
    def _open_project(self):
        file_path = filedialog.askopenfilename(title="Open Project", filetypes=PROJECT_FORMATS, initialdir=PROJECTS_FOLDER)
        if file_path:
            load_project(Path(file_path))
    
    def _save_project(self):
        if app_state.current_project_path:
            save_project()
        else:
            self._save_project_as()
    
    def _save_project_as(self):
        file_path = filedialog.asksaveasfilename(title="Save As", defaultextension=".json", filetypes=PROJECT_FORMATS, initialdir=PROJECTS_FOLDER)
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
