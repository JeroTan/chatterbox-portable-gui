"""
Expression Controls Component
Text-based or parameter-based expression controls
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class ExpressionControlsComponent:
    """
    Expression controls with text/parameter modes
    """
    
    def __init__(
        self,
        parent,
        emotions: list,
        on_expression_change: Optional[Callable] = None
    ):
        """
        Args:
            parent: Parent tkinter widget
            emotions: List of emotion options
            on_expression_change: Callback when expression changes
        """
        self.emotions = emotions
        self.on_expression_change = on_expression_change
        
        # Container frame
        self.frame = ttk.LabelFrame(parent, text="Expression Controls", padding="10")
        
        # Mode selection (hide text mode for now - only show Preset and Parameter)
        mode_frame = ttk.Frame(self.frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.expression_mode = tk.StringVar(value="preset")
        
        ttk.Radiobutton(
            mode_frame,
            text="Preset Emotions",
            variable=self.expression_mode,
            value="preset",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            mode_frame,
            text="Parameter Controls",
            variable=self.expression_mode,
            value="parameters",
            command=self._on_mode_change
        ).pack(side=tk.LEFT)
        
        # Note: Text mode radio button intentionally hidden
        # Text mode frame still exists for backward compatibility with saved projects
        
        # Preset mode (dropdown with predefined emotions/expressions)
        self.preset_frame = ttk.Frame(self.frame)
        self.preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.preset_frame, text="Select Expression:").pack(anchor=tk.W, pady=(0, 5))
        
        # Define preset emotions with their parameter values
        self.emotion_presets = {
            "🎭 Default (Neutral)": {"energy": 0.70, "speed": 0.40, "emphasis": 0.90, "pitch": 0},
            "😊 Happy": {"energy": 1.20, "speed": 0.35, "emphasis": 1.10, "pitch": 2},
            "😢 Sad": {"energy": 0.40, "speed": 0.60, "emphasis": 0.60, "pitch": -2},
            "😠 Angry": {"energy": 1.50, "speed": 0.35, "emphasis": 1.30, "pitch": 0},
            "😨 Fearful": {"energy": 1.00, "speed": 0.30, "emphasis": 1.20, "pitch": 3},
            "😌 Calm": {"energy": 0.50, "speed": 0.55, "emphasis": 0.70, "pitch": -1},
            "😄 Excited": {"energy": 1.40, "speed": 0.25, "emphasis": 1.40, "pitch": 4},
            "🥱 Tired": {"energy": 0.25, "speed": 0.01, "emphasis": 0.05, "pitch": -3},
            "😏 Sarcastic": {"energy": 0.80, "speed": 0.50, "emphasis": 1.00, "pitch": 1},
            "🤔 Thoughtful": {"energy": 0.60, "speed": 0.60, "emphasis": 0.80, "pitch": -1},
            "📢 Energetic": {"energy": 1.60, "speed": 0.30, "emphasis": 1.30, "pitch": 3},
            "😴 Sleepy": {"energy": 0.30, "speed": 0.75, "emphasis": 0.40, "pitch": -4},
            "🎤 Narrator": {"energy": 0.65, "speed": 0.50, "emphasis": 0.85, "pitch": 0},
            "👨‍🏫 Professional": {"energy": 0.75, "speed": 0.45, "emphasis": 0.80, "pitch": 0},
            "🧒 Childlike": {"energy": 1.30, "speed": 0.35, "emphasis": 1.20, "pitch": 5},
            "🧓 Elderly": {"energy": 0.45, "speed": 0.65, "emphasis": 0.65, "pitch": -3},
            "😱 Surprised": {"energy": 1.40, "speed": 0.28, "emphasis": 1.50, "pitch": 5},
            "🤗 Warm": {"energy": 0.90, "speed": 0.50, "emphasis": 1.00, "pitch": 1},
            "❄️ Cold": {"energy": 0.40, "speed": 0.55, "emphasis": 0.50, "pitch": -2},
            "🎭 Dramatic": {"energy": 1.80, "speed": 0.40, "emphasis": 1.60, "pitch": 2},
        }
        
        self.preset_var = tk.StringVar(value="🎭 Default (Neutral)")
        preset_dropdown = ttk.Combobox(
            self.preset_frame,
            textvariable=self.preset_var,
            values=list(self.emotion_presets.keys()),
            state="readonly",
            width=30
        )
        preset_dropdown.pack(fill=tk.X)
        preset_dropdown.bind("<<ComboboxSelected>>", self._on_preset_change)
        
        # Text mode (hidden by default)
        self.text_frame = ttk.Frame(self.frame)
        
        ttk.Label(self.text_frame, text="Describe the expression:").pack(anchor=tk.W, pady=(0, 5))
        
        self.expression_text = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            height=2,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.expression_text.pack(fill=tk.X)
        self.expression_text.insert("1.0", "e.g., 'happy and energetic' or 'calm narrator'")
        
        # Parameters mode
        self.params_frame = ttk.Frame(self.frame)
        
        # Create parameter controls with proper ranges based on Chatterbox TTS API
        # Energy -> exaggeration (0.25-2.0, default 0.7)
        # Speed -> cfg_weight (0.01-1.0, default 0.4) - controls speech rate
        # Emphasis -> temperature (0.05-5.0, default 0.9) - controls variation/emphasis
        # Pitch -> post-processing (-12 to +12 semitones, default 0)
        
        self.energy_var = tk.DoubleVar(value=0.70)  # exaggeration default (Chatterbox official)
        self.speed_var = tk.DoubleVar(value=0.40)  # cfg_weight default (Chatterbox official)
        self.emphasis_var = tk.DoubleVar(value=0.90)  # temperature default (Chatterbox official)
        self.pitch_var = tk.IntVar(value=0)  # pitch shift in semitones
        
        # Energy (Exaggeration) - with input box and reset
        self._create_param_with_input(
            self.params_frame,
            "Energy (Expressiveness):",
            self.energy_var,
            0.25, 2.0,
            0.70,
            "0.3-0.4: Very neutral\n0.5: Balanced\n0.7: Default (expressive)\n1.0+: Very dramatic",
            decimals=2
        )
        
        # Speed (CFG Weight) - with input box and reset
        self._create_param_with_input(
            self.params_frame,
            "Speed (Speech Rate):",
            self.speed_var,
            0.01, 1.0,
            0.40,
            "0.2-0.3: Faster speech\n0.4: Default\n0.5: Normal\n0.7-0.9: Slower, deliberate",
            decimals=2
        )
        
        # Emphasis (Temperature) - with input box and reset
        self._create_param_with_input(
            self.params_frame,
            "Emphasis (Variation):",
            self.emphasis_var,
            0.05, 5.0,
            0.90,
            "0.4-0.6: Consistent tone\n0.9: Default (varied)\n1.0+: Variable emphasis",
            decimals=2
        )
        
        # Pitch (Post-processing) - with input box and reset
        self._create_param_with_input(
            self.params_frame,
            "Pitch (Semitones):",
            self.pitch_var,
            -12, 12,
            0,
            "-12 to -6: Lower pitch\n0: No change\n+6 to +12: Higher pitch\nUses Praat for natural formant preservation\n💡 Best quality within ±6 semitones",
            decimals=0
        )
    
    def _create_slider(self, parent, label: str, variable, from_: float, to: float, resolution: float = 1):
        """Helper to create labeled slider"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text=label, width=15).pack(side=tk.LEFT)
        
        slider = ttk.Scale(
            frame,
            from_=from_,
            to=to,
            variable=variable,
            orient=tk.HORIZONTAL,
            command=lambda v: self._trigger_callback()
        )
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        value_label = ttk.Label(frame, textvariable=variable, width=8)
        value_label.pack(side=tk.LEFT)
    
    def _create_param_with_input(self, parent, label, variable, min_val, max_val, default_val, tooltip_text, decimals=2):
        """Create parameter control with slider, input box, and reset button"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        # Label with tooltip
        label_widget = ttk.Label(frame, text=label, width=20)
        label_widget.pack(side=tk.LEFT)
        self._create_tooltip(label_widget, tooltip_text)
        
        # Slider
        scale = ttk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            variable=variable,
            orient=tk.HORIZONTAL,
            command=lambda v: self._trigger_callback()
        )
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Input box with configurable decimal precision
        input_frame = ttk.Frame(frame)
        input_frame.pack(side=tk.LEFT, padx=2)
        
        input_box = ttk.Entry(input_frame, width=8)
        input_box.pack()
        
        # Format string based on decimals
        fmt = f"{{:.{decimals}f}}" if decimals > 0 else "{:.0f}"
        input_box.insert(0, fmt.format(default_val))
        
        # Sync slider to input box
        def on_slider_change(*args):
            val = variable.get()
            input_box.delete(0, tk.END)
            input_box.insert(0, fmt.format(val))
        
        variable.trace_add("write", on_slider_change)
        
        # Sync input box to slider
        def on_input_change(event=None):
            try:
                val = float(input_box.get())
                # Clamp to valid range
                val = max(min_val, min(max_val, val))
                # Round to specified decimal places
                val = round(val, decimals)
                variable.set(val)
                input_box.delete(0, tk.END)
                input_box.insert(0, fmt.format(val))
            except ValueError:
                # Reset to current slider value
                input_box.delete(0, tk.END)
                input_box.insert(0, fmt.format(variable.get()))
        
        input_box.bind("<Return>", on_input_change)
        input_box.bind("<FocusOut>", on_input_change)
        
        # Reset button
        def reset_param():
            variable.set(default_val)
            input_box.delete(0, tk.END)
            input_box.insert(0, fmt.format(default_val))
        
        reset_btn = ttk.Button(frame, text="↻", width=3, command=reset_param)
        reset_btn.pack(side=tk.LEFT, padx=2)
        self._create_tooltip(reset_btn, "Reset to default")
    
    def _create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief=tk.SOLID, borderwidth=1)
            label.pack()
            widget._tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, '_tooltip'):
                widget._tooltip.destroy()
                delattr(widget, '_tooltip')
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _on_mode_change(self):
        """Handle mode change"""
        mode = self.expression_mode.get()
        
        if mode == "text":
            self.text_frame.pack(fill=tk.BOTH, expand=True)
            self.preset_frame.pack_forget()
            self.params_frame.pack_forget()
        elif mode == "preset":
            self.preset_frame.pack(fill=tk.X, pady=(0, 10))
            self.text_frame.pack_forget()
            self.params_frame.pack_forget()
        else:  # parameters
            self.text_frame.pack_forget()
            self.preset_frame.pack_forget()
            self.params_frame.pack(fill=tk.BOTH, expand=True)
        
        self._trigger_callback()
    
    def _on_preset_change(self, event=None):
        """Handle preset selection change"""
        selected_preset = self.preset_var.get()
        preset_values = self.emotion_presets.get(selected_preset)
        
        if preset_values:
            # Update parameter variables to match the preset
            self.energy_var.set(preset_values["energy"])
            self.speed_var.set(preset_values["speed"])
            self.emphasis_var.set(preset_values["emphasis"])
            self.pitch_var.set(preset_values["pitch"])
            
            # Update input boxes to match
            for frame in self.params_frame.winfo_children():
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Entry):
                                var_name = None
                                # Find which variable this entry is for
                                if hasattr(frame, 'winfo_children'):
                                    label = frame.winfo_children()[0]
                                    if isinstance(label, ttk.Label):
                                        label_text = label.cget("text")
                                        if "Energy" in label_text:
                                            child.delete(0, tk.END)
                                            child.insert(0, f"{preset_values['energy']:.2f}")
                                        elif "Speed" in label_text:
                                            child.delete(0, tk.END)
                                            child.insert(0, f"{preset_values['speed']:.2f}")
                                        elif "Emphasis" in label_text:
                                            child.delete(0, tk.END)
                                            child.insert(0, f"{preset_values['emphasis']:.2f}")
                                        elif "Pitch" in label_text:
                                            child.delete(0, tk.END)
                                            child.insert(0, f"{preset_values['pitch']:.0f}")
        
        self._trigger_callback()
    
    def _trigger_callback(self):
        """Trigger expression change callback"""
        if self.on_expression_change:
            self.on_expression_change()
    
    def get_expression_config(self) -> dict:
        """Get current expression configuration"""
        mode = self.expression_mode.get()
        
        if mode == "text":
            text = self.expression_text.get("1.0", tk.END).strip()
            # If it's the placeholder text or empty, return "default"
            if not text or text.startswith("e.g.,"):
                text = "default"
            return {
                "mode": "text",
                "text": text
            }
        elif mode == "preset":
            # Return preset mode with parameters from the selected preset
            selected_preset = self.preset_var.get()
            preset_values = self.emotion_presets.get(selected_preset, self.emotion_presets["🎭 Default (Neutral)"])
            return {
                "mode": "preset",  # Keep mode as preset
                "preset": selected_preset,
                "energy": preset_values["energy"],
                "speed": preset_values["speed"],
                "emphasis": preset_values["emphasis"],
                "pitch": preset_values["pitch"]
            }
        else:  # parameters
            return {
                "mode": "parameters",
                "energy": self.energy_var.get(),       # exaggeration (0.25-2.0)
                "speed": self.speed_var.get(),         # cfg_weight (0.01-1.0)
                "emphasis": self.emphasis_var.get(),   # temperature (0.05-5.0)
                "pitch": self.pitch_var.get()          # pitch shift in semitones (-12 to +12)
            }
    
    def set_expression_config(self, config: dict):
        """Set expression configuration"""
        mode = config.get("mode", "preset")
        
        # Check if there's a preset specified
        if "preset" in config:
            self.expression_mode.set("preset")
            self.preset_var.set(config["preset"])
            self._on_mode_change()
            self._on_preset_change()
        elif mode == "text":
            self.expression_mode.set("text")
            self._on_mode_change()
            text = config.get("text", "")
            self.expression_text.delete("1.0", tk.END)
            self.expression_text.insert("1.0", text)
        else:  # parameters
            self.expression_mode.set("parameters")
            self._on_mode_change()
            self.energy_var.set(config.get("energy", 0.70))
            self.speed_var.set(config.get("speed", 0.40))
            self.emphasis_var.set(config.get("emphasis", 0.90))
            self.pitch_var.set(config.get("pitch", 0))
