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
        
        # Mode selection
        mode_frame = ttk.Frame(self.frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.expression_mode = tk.StringVar(value="text")
        
        ttk.Radiobutton(
            mode_frame,
            text="Text Description",
            variable=self.expression_mode,
            value="text",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            mode_frame,
            text="Parameter Controls",
            variable=self.expression_mode,
            value="parameters",
            command=self._on_mode_change
        ).pack(side=tk.LEFT)
        
        # Text mode
        self.text_frame = ttk.Frame(self.frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.text_frame, text="Describe the expression:").pack(anchor=tk.W, pady=(0, 5))
        
        self.expression_text = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            height=2,  # Reduced from 3 to 2
            relief=tk.SOLID,
            borderwidth=1
        )
        self.expression_text.pack(fill=tk.X)  # Changed to fill X only, not expand
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
            self.params_frame.pack_forget()
        else:
            self.text_frame.pack_forget()
            self.params_frame.pack(fill=tk.BOTH, expand=True)
        
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
        else:
            return {
                "mode": "parameters",
                "energy": self.energy_var.get(),       # exaggeration (0.25-2.0)
                "speed": self.speed_var.get(),         # cfg_weight (0.01-1.0)
                "emphasis": self.emphasis_var.get(),   # temperature (0.05-5.0)
                "pitch": self.pitch_var.get()          # pitch shift in semitones (-12 to +12)
            }
    
    def set_expression_config(self, config: dict):
        """Set expression configuration"""
        mode = config.get("mode", "text")
        self.expression_mode.set(mode)
        self._on_mode_change()
        
        if mode == "text":
            text = config.get("text", "")
            self.expression_text.delete("1.0", tk.END)
            self.expression_text.insert("1.0", text)
        else:
            self.energy_var.set(config.get("energy", 0.70))
            self.speed_var.set(config.get("speed", 0.40))
            self.emphasis_var.set(config.get("emphasis", 0.90))
            self.pitch_var.set(config.get("pitch", 0))
