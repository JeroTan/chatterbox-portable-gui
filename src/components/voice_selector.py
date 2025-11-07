"""
Voice Selector Component
Predefined or custom voice selection with Male/Female filtering
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional, Dict, List
from pathlib import Path


class VoiceSelectorComponent:
    """
    Voice selection component with predefined/custom modes
    Predefined voices can be filtered by Male/Female/All
    """
    
    def __init__(
        self,
        parent,
        predefined_voices: Dict[str, List[str]],  # Changed to dict
        on_voice_change: Optional[Callable] = None
    ):
        """
        Args:
            parent: Parent tkinter widget
            predefined_voices: Dict with keys "Male", "Female", "All" and lists of voice names
            on_voice_change: Callback when voice changes
        """
        self.predefined_voices = predefined_voices
        self.on_voice_change = on_voice_change
        self.current_filter = "All"  # Default filter
        
        # Container frame
        self.frame = ttk.LabelFrame(parent, text="Voice Selection", padding="10")
        
        # Voice mode selection
        mode_frame = ttk.Frame(self.frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.voice_mode = tk.StringVar(value="predefined")
        
        ttk.Radiobutton(
            mode_frame,
            text="Predefined Voices",
            variable=self.voice_mode,
            value="predefined",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            mode_frame,
            text="Custom Voice (Reference Audio)",
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
        
        # Create filter buttons (like tabs)
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
        
        # Voice selector button (shows popup on click)
        voice_frame = ttk.Frame(self.predefined_frame)
        voice_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(voice_frame, text="Selected Voice:").pack(side=tk.LEFT, padx=(0, 10))
        
        # Button showing current selection
        self.selected_voice_var = tk.StringVar(
            value=predefined_voices["All"][0] if predefined_voices["All"] else ""
        )
        
        self.voice_button = ttk.Button(
            voice_frame,
            textvariable=self.selected_voice_var,
            command=self._show_voice_picker,
            width=35
        )
        self.voice_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Popup window reference
        self.picker_window = None
        
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
    
    def _show_voice_picker(self):
        """Show dropdown overlay with search and scrollable voice list"""
        if self.picker_window:
            self._close_picker()  # Toggle if already open
            return
        
        # Create toplevel window without decorations (overlay style)
        self.picker_window = tk.Toplevel(self.frame)
        self.picker_window.overrideredirect(True)  # No window decorations
        
        # Position below the button with wider width
        button_x = self.voice_button.winfo_rootx()
        button_y = self.voice_button.winfo_rooty()
        button_height = self.voice_button.winfo_height()
        
        # Make dropdown wider than button
        dropdown_width = 500  # Fixed wider width
        dropdown_height = 350
        
        self.picker_window.geometry(f"{dropdown_width}x{dropdown_height}+{button_x}+{button_y + button_height}")
        
        # Add border
        main_frame = ttk.Frame(self.picker_window, relief=tk.SOLID, borderwidth=1)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search box at top
        search_frame = ttk.Frame(main_frame, padding="5")
        search_frame.pack(fill=tk.X)
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(fill=tk.X)
        search_entry.insert(0, "🔍 Type to search...")
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END) if search_entry.get().startswith("🔍") else None)
        search_entry.focus()
        
        # Scrollable list frame
        list_container = ttk.Frame(main_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas with scrollbar for list
        canvas = tk.Canvas(list_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Get voices for current filter
        voices = self.predefined_voices[self.current_filter]
        
        # Create buttons in grid layout (like flex-wrap)
        voice_buttons = []
        row_frame = None
        buttons_in_row = 0
        max_buttons_per_row = 3  # More buttons per row since dropdown is wider
        
        for i, voice in enumerate(voices):
            # Create new row frame if needed
            if buttons_in_row == 0:
                row_frame = ttk.Frame(scrollable_frame)
                row_frame.pack(fill=tk.X, pady=2, padx=2)
                row_frame.grid_columnconfigure(0, weight=1, uniform="button")
                row_frame.grid_columnconfigure(1, weight=1, uniform="button")
                row_frame.grid_columnconfigure(2, weight=1, uniform="button")
            
            btn = tk.Button(
                row_frame,
                text=voice,
                command=lambda v=voice: self._select_voice(v),
                wraplength=130,  # Wrap text at 130 pixels
                justify=tk.CENTER,
                relief=tk.RAISED,
                borderwidth=1,
                padx=8,
                pady=5,
                width=15,  # Fixed character width
                anchor=tk.CENTER
            )
            btn.grid(row=0, column=buttons_in_row, padx=3, pady=2, sticky="nsew")  # Changed to nsew
            voice_buttons.append((voice, btn, row_frame))
            
            buttons_in_row += 1
            
            # Start new row after max_buttons_per_row
            if buttons_in_row >= max_buttons_per_row:
                buttons_in_row = 0
        
        # Search functionality
        def filter_voices(*args):
            search_text = search_var.get().lower()
            if search_text.startswith("🔍"):
                search_text = ""
            
            # Clear all existing rows
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Recreate filtered buttons
            new_row_frame = None
            new_buttons_in_row = 0
            found_count = 0
            
            for voice, btn, old_row_frame in voice_buttons:
                if search_text in voice.lower():
                    found_count += 1
                    # Create new row if needed
                    if new_buttons_in_row == 0:
                        new_row_frame = ttk.Frame(scrollable_frame)
                        new_row_frame.pack(fill=tk.X, pady=2, padx=2)
                        new_row_frame.grid_columnconfigure(0, weight=1, uniform="button")
                        new_row_frame.grid_columnconfigure(1, weight=1, uniform="button")
                        new_row_frame.grid_columnconfigure(2, weight=1, uniform="button")
                    
                    # Create button in new row
                    new_btn = tk.Button(
                        new_row_frame,
                        text=voice,
                        command=lambda v=voice: self._select_voice(v),
                        wraplength=130,
                        justify=tk.CENTER,
                        relief=tk.RAISED,
                        borderwidth=1,
                        padx=8,
                        pady=5,
                        width=15,
                        anchor=tk.CENTER
                    )
                    new_btn.grid(row=0, column=new_buttons_in_row, padx=3, pady=2, sticky="nsew")  # Changed to nsew
                    
                    new_buttons_in_row += 1
                    if new_buttons_in_row >= max_buttons_per_row:
                        new_buttons_in_row = 0
            
            # Show "No voices found" message if no results
            if found_count == 0 and search_text:
                no_result_label = ttk.Label(
                    scrollable_frame,
                    text="🔍 No voices found",
                    font=("Segoe UI", 10),
                    foreground="gray"
                )
                no_result_label.pack(pady=20)
        
        search_var.trace_add("write", filter_voices)
        
        # Close on click outside
        def check_close(event):
            widget = event.widget
            # Check if click is outside the picker window
            if widget not in [self.picker_window, main_frame, search_entry, canvas, scrollbar, scrollable_frame]:
                # Check if it's not one of the voice buttons
                is_voice_button = False
                for _, btn, _ in voice_buttons:
                    if widget == btn:
                        is_voice_button = True
                        break
                
                if not is_voice_button and widget != self.voice_button:
                    self._close_picker()
        
        # Bind to root window to catch clicks outside
        self.picker_window.bind("<FocusOut>", lambda e: self._close_picker())
        
        # Keep focus
        self.picker_window.focus_set()
    
    def _select_voice(self, voice: str):
        """Select a voice and close picker"""
        self.selected_voice_var.set(voice)
        self._close_picker()
        self._trigger_callback()
    
    def _close_picker(self):
        """Close the voice picker window"""
        if self.picker_window:
            self.picker_window.destroy()
            self.picker_window = None
    
    def _on_combobox_search(self):
        """Filter voices as user types in combobox"""
        typed_text = self.voice_combobox.get().lower()
        
        # Get base list from current filter
        base_voices = self.predefined_voices[self.current_filter]
        
        # Filter by typed text
        if typed_text:
            filtered_voices = [v for v in base_voices if typed_text in v.lower()]
        else:
            filtered_voices = base_voices
        
        # Update dropdown list
        self.voice_combobox.config(values=filtered_voices)
        
        # Show dropdown if there are matches
        if filtered_voices:
            self.voice_combobox.event_generate('<Down>')
    
    def _on_voice_selected(self):
        """Handle voice selection from dropdown"""
        # Make sure selected value is valid
        selected = self.voice_combobox.get()
        base_voices = self.predefined_voices[self.current_filter]
        
        if selected in base_voices:
            self._trigger_callback()
    
    def _set_filter(self, filter_name: str):
        """Set the gender filter and update voice list"""
        self.current_filter = filter_name
        
        # Update selected voice to first in new filter if needed
        filtered_voices = self.predefined_voices[filter_name]
        current_voice = self.selected_voice_var.get()
        
        if current_voice not in filtered_voices and filtered_voices:
            self.selected_voice_var.set(filtered_voices[0])
        
        # Update button styles
        self._update_filter_buttons()
        
        # Trigger callback
        self._trigger_callback()
    
    def _update_filter_buttons(self):
        """Update filter button styles to highlight active filter"""
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
            return {
                "mode": "predefined",
                "voice": self.selected_voice_var.get(),
                "gender_filter": self.current_filter,
                "custom_path": None
            }
        else:
            path = self.custom_path_var.get()
            return {
                "mode": "custom",
                "voice": None,
                "gender_filter": None,
                "custom_path": Path(path) if path != "No file selected" else None
            }
    
    def set_voice_config(self, mode: str, voice: Optional[str] = None, 
                        gender_filter: Optional[str] = None, 
                        custom_path: Optional[Path] = None):
        """Set voice configuration"""
        self.voice_mode.set(mode)
        self._on_mode_change()
        
        if mode == "predefined":
            # Set filter if provided
            if gender_filter and gender_filter in ["All", "Male", "Female"]:
                self._set_filter(gender_filter)
            
            # Set voice if provided
            if voice:
                self.selected_voice_var.set(voice)
        elif mode == "custom" and custom_path:
            self.custom_path_var.set(str(custom_path))
