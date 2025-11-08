"""
Audio Player Component
Built-in audio player with playback controls
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import threading
import time


class AudioPlayerComponent:
    """
    Built-in audio player with play/pause/stop controls with scrubber
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.audio_path = None
        self.is_playing = False
        self.is_paused = False
        self.playback_thread = None
        self.stop_playback = False
        self.audio_length = 0  # in seconds
        self.current_position = 0  # in seconds
        self.is_dragging_scrubber = False
        
        # Try to import pygame for audio playback
        try:
            import pygame
            pygame.mixer.init()
            self.pygame = pygame
            self.audio_available = True
        except ImportError:
            self.pygame = None
            self.audio_available = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the audio player UI"""
        self.frame = ttk.LabelFrame(self.parent, text="🎵 Audio Preview", padding="10")
        
        # Status label
        self.status_var = tk.StringVar(value="No audio loaded")
        status_label = ttk.Label(
            self.frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9)
        )
        status_label.pack(fill=tk.X, pady=(0, 10))
        
        # Time display and scrubber
        time_scrubber_frame = ttk.Frame(self.frame)
        time_scrubber_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Current time label
        self.current_time_var = tk.StringVar(value="0:00.000")
        current_time_label = ttk.Label(
            time_scrubber_frame,
            textvariable=self.current_time_var,
            font=("Segoe UI", 8),
            width=9
        )
        current_time_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Scrubber (Scale widget)
        self.scrubber = ttk.Scale(
            time_scrubber_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL
        )
        self.scrubber.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.scrubber.bind("<ButtonPress-1>", self._on_scrubber_press)
        self.scrubber.bind("<ButtonRelease-1>", self._on_scrubber_release)
        self.scrubber.bind("<B1-Motion>", self._on_scrubber_drag)
        
        # Total time label
        self.total_time_var = tk.StringVar(value="0:00.000")
        total_time_label = ttk.Label(
            time_scrubber_frame,
            textvariable=self.total_time_var,
            font=("Segoe UI", 8),
            width=9
        )
        total_time_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Controls frame
        controls = ttk.Frame(self.frame)
        controls.pack(fill=tk.X)
        
        # Play/Pause toggle button
        self.play_pause_btn = ttk.Button(
            controls,
            text="▶ Play",
            command=self._toggle_play_pause,
            state=tk.DISABLED,
            width=12
        )
        self.play_pause_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Stop button
        self.stop_btn = ttk.Button(
            controls,
            text="⏹ Stop",
            command=self._stop_audio,
            state=tk.DISABLED,
            width=12
        )
        self.stop_btn.pack(side=tk.LEFT)
        
        if not self.audio_available:
            self.status_var.set("⚠️ pygame not installed - audio preview unavailable")
    
    def load_audio(self, audio_path: Path):
        """
        Load an audio file for playback
        
        Args:
            audio_path: Path to the audio file
        """
        if not self.audio_available:
            return
        
        try:
            self._stop_audio()
            self.audio_path = audio_path
            self.pygame.mixer.music.load(str(audio_path))
            
            # Get audio length using multiple methods
            self.audio_length = 0
            
            # Method 1: Try pygame.mixer.Sound
            try:
                sound = self.pygame.mixer.Sound(str(audio_path))
                self.audio_length = sound.get_length()
                print(f"🎵 Audio length (pygame.Sound): {self.audio_length} seconds")
            except Exception as e:
                print(f"⚠️ pygame.Sound failed: {e}")
            
            # Method 2: If pygame failed, try wave module for WAV files
            if self.audio_length == 0:
                try:
                    import wave
                    with wave.open(str(audio_path), 'rb') as wav_file:
                        frames = wav_file.getnframes()
                        rate = wav_file.getframerate()
                        self.audio_length = frames / float(rate)
                        print(f"🎵 Audio length (wave): {self.audio_length} seconds")
                except Exception as e:
                    print(f"⚠️ wave module failed: {e}")
            
            # Method 3: Try reading with soundfile
            if self.audio_length == 0:
                try:
                    import soundfile as sf
                    info = sf.info(str(audio_path))
                    self.audio_length = info.duration
                    print(f"🎵 Audio length (soundfile): {self.audio_length} seconds")
                except Exception as e:
                    print(f"⚠️ soundfile failed: {e}")
            
            if self.audio_length > 0:
                self.scrubber.config(to=self.audio_length)
                self.total_time_var.set(self._format_time(self.audio_length))
            else:
                self.scrubber.config(to=100)
                self.total_time_var.set("Unknown")
                print("⚠️ Could not determine audio length")
            
            self.current_position = 0
            self.current_time_var.set("0:00.000")
            self.scrubber.set(0)
            
            self.status_var.set(f"Ready: {audio_path.name}")
            self.play_pause_btn.config(state=tk.NORMAL, text="▶ Play")
            self.stop_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.status_var.set(f"Error loading audio: {str(e)}")
            print(f"❌ Error loading audio: {e}")
    
    def _format_time(self, seconds: float) -> str:
        """Format time in seconds to MM:SS.mmm format"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{minutes}:{secs:02d}.{milliseconds:03d}"
    
    def _on_scrubber_press(self, event):
        """Handle scrubber press - start dragging"""
        self.is_dragging_scrubber = True
        # Update time display immediately when clicking
        position = float(self.scrubber.get())
        self.current_time_var.set(self._format_time(position))
    
    def _on_scrubber_drag(self, event):
        """Handle scrubber dragging - update time display"""
        if self.is_dragging_scrubber:
            position = float(self.scrubber.get())
            self.current_time_var.set(self._format_time(position))
    
    def _on_scrubber_release(self, event):
        """Handle scrubber release - seek to position"""
        if not self.audio_available or not self.audio_path:
            return
        
        self.is_dragging_scrubber = False
        
        # Get the position from scrubber
        position = float(self.scrubber.get())
        
        # Remember if we were playing
        was_playing = self.is_playing
        
        # Stop current playback
        if self.is_playing:
            self.pygame.mixer.music.stop()
            self.is_playing = False
            self.stop_playback = True
        
        # Reload and seek to position
        try:
            self.pygame.mixer.music.load(str(self.audio_path))
            
            # Set the new position
            self.current_position = position
            
            # Start playing from the new position
            if position > 0:
                self.pygame.mixer.music.play(start=position)
            else:
                self.pygame.mixer.music.play()
            
            # If we weren't playing before, pause immediately
            if not was_playing:
                self.pygame.mixer.music.pause()
                self.current_time_var.set(self._format_time(position))
            else:
                # Resume playing
                self.is_playing = True
                self.stop_playback = False
                self.play_pause_btn.config(text="⏸ Pause")
                self.stop_btn.config(state=tk.NORMAL)
                self.status_var.set(f"▶ Playing: {self.audio_path.name}")
                self._monitor_playback()
                
        except Exception as e:
            self.status_var.set(f"Error seeking: {str(e)}")
    
    def _toggle_play_pause(self):
        """Toggle between play and pause"""
        if self.is_playing:
            self._pause_audio()
        else:
            self._play_audio()
    
    def _play_audio(self):
        """Play or resume audio"""
        if not self.audio_available or not self.audio_path:
            return
        
        try:
            if self.is_paused:
                # Resume from pause (unpause)
                self.pygame.mixer.music.unpause()
                self.is_paused = False
                self.is_playing = True
            elif self.pygame.mixer.music.get_busy():
                # Already playing, just unpause if needed
                self.pygame.mixer.music.unpause()
                self.is_playing = True
            else:
                # Start fresh playback (either from beginning or from current_position)
                if self.current_position > 0:
                    self.pygame.mixer.music.play(start=self.current_position)
                else:
                    self.pygame.mixer.music.play()
                self.is_playing = True
            
            self.status_var.set(f"▶ Playing: {self.audio_path.name}")
            self.play_pause_btn.config(text="⏸ Pause")
            self.stop_btn.config(state=tk.NORMAL)
            
            # Monitor playback
            self._monitor_playback()
        except Exception as e:
            self.status_var.set(f"Error playing: {str(e)}")
    
    def _pause_audio(self):
        """Pause audio playback"""
        if not self.audio_available:
            return
        
        try:
            self.pygame.mixer.music.pause()
            # Update current position to the paused position
            self.current_position = self.scrubber.get()
            self.is_paused = True
            self.is_playing = False
            self.status_var.set(f"⏸ Paused: {self.audio_path.name}")
            self.play_pause_btn.config(text="▶ Play")
        except Exception as e:
            self.status_var.set(f"Error pausing: {str(e)}")
    
    def _stop_audio(self):
        """Stop audio playback"""
        if not self.audio_available:
            return
        
        try:
            self.pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.stop_playback = True
            self.current_position = 0
            
            # Reset scrubber and time
            self.scrubber.set(0)
            self.current_time_var.set("0:00.000")
            
            if self.audio_path:
                self.status_var.set(f"Ready: {self.audio_path.name}")
            else:
                self.status_var.set("No audio loaded")
            
            self.play_pause_btn.config(state=tk.NORMAL if self.audio_path else tk.DISABLED, text="▶ Play")
            self.stop_btn.config(state=tk.DISABLED if not self.audio_path else tk.NORMAL)
        except Exception as e:
            self.status_var.set(f"Error stopping: {str(e)}")
    
    def _monitor_playback(self):
        """Monitor playback and update UI when finished"""
        def check_playback():
            start_time = time.time()
            while self.is_playing and not self.stop_playback:
                if not self.pygame.mixer.music.get_busy():
                    # Playback finished
                    self.is_playing = False
                    self.parent.after(0, lambda: self._on_playback_finished())
                    break
                
                # Update scrubber position and time display
                if not self.is_dragging_scrubber:
                    elapsed = time.time() - start_time + self.current_position
                    if elapsed <= self.audio_length:
                        self.parent.after(0, lambda e=elapsed: self._update_playback_position(e))
                
                time.sleep(0.1)
            self.stop_playback = False
        
        if self.playback_thread and self.playback_thread.is_alive():
            return
        
        self.stop_playback = False
        self.playback_thread = threading.Thread(target=check_playback, daemon=True)
        self.playback_thread.start()
    
    def _update_playback_position(self, position: float):
        """Update scrubber and time display during playback"""
        if not self.is_dragging_scrubber:
            self.scrubber.set(position)
            self.current_time_var.set(self._format_time(position))
    
    def _on_playback_finished(self):
        """Handle playback finished"""
        # Reset to beginning
        self.current_position = 0
        self.scrubber.set(0)
        self.current_time_var.set("0:00.000")
        
        if self.audio_path:
            self.status_var.set(f"✓ Finished: {self.audio_path.name}")
        self.play_pause_btn.config(text="▶ Play")
    
    def clear(self):
        """Clear the loaded audio"""
        self._stop_audio()
        self.audio_path = None
        self.audio_length = 0
        self.current_position = 0
        self.scrubber.set(0)
        self.current_time_var.set("0:00.000")
        self.total_time_var.set("0:00.000")
        self.status_var.set("No audio loaded")
        self.play_pause_btn.config(state=tk.DISABLED, text="▶ Play")
        self.stop_btn.config(state=tk.DISABLED)
    
    def apply_theme(self, theme: dict):
        """Apply theme colors to this component"""
        # Stub - components will be themed via ttk styles
        pass
