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
        
        # Create parameter controls
        self.emotion_var = tk.StringVar(value=emotions[0])
        self.energy_var = tk.IntVar(value=50)
        self.speed_var = tk.DoubleVar(value=1.0)
        self.pitch_var = tk.IntVar(value=0)
        self.emphasis_var = tk.IntVar(value=30)
        
        # Emotion
        emotion_frame = ttk.Frame(self.params_frame)
        emotion_frame.pack(fill=tk.X, pady=5)
        ttk.Label(emotion_frame, text="Emotion:", width=15).pack(side=tk.LEFT)
        ttk.Combobox(
            emotion_frame,
            textvariable=self.emotion_var,
            values=emotions,
            state="readonly",
            width=20
        ).pack(side=tk.LEFT)
        
        # Energy slider
        self._create_slider(
            self.params_frame,
            "Energy:",
            self.energy_var,
            0, 100
        )
        
        # Speed slider
        self._create_slider(
            self.params_frame,
            "Speed:",
            self.speed_var,
            0.5, 2.0,
            resolution=0.1
        )
        
        # Pitch slider
        self._create_slider(
            self.params_frame,
            "Pitch:",
            self.pitch_var,
            -12, 12
        )
        
        # Emphasis slider
        self._create_slider(
            self.params_frame,
            "Emphasis:",
            self.emphasis_var,
            0, 100
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
                "emotion": self.emotion_var.get(),
                "energy": self.energy_var.get(),
                "speed": self.speed_var.get(),
                "pitch": self.pitch_var.get(),
                "emphasis": self.emphasis_var.get()
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
            self.emotion_var.set(config.get("emotion", self.emotions[0]))
            self.energy_var.set(config.get("energy", 50))
            self.speed_var.set(config.get("speed", 1.0))
            self.pitch_var.set(config.get("pitch", 0))
            self.emphasis_var.set(config.get("emphasis", 30))
