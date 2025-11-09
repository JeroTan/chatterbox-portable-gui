"""
TTS Generation Feature
Handles audio generation using chatterbox-tts
"""

from pathlib import Path
from typing import Optional, Dict, Any
import traceback
import torchaudio as ta
from tkinter import messagebox


class TTSGenerator:
    """
    Text-to-Speech generator using chatterbox-tts
    """
    
    def __init__(self):
        self.model = None
        self.multilingual_model = None
        self._initialized = False
        self.loading_screen = None
        self.device = "cpu"  # Default to CPU
        self.device_name = "CPU"
    
    def initialize(self, loading_screen=None, force_device=None) -> bool:
        """
        Initialize the TTS model
        This is done lazily on first use
        
        Args:
            loading_screen: Optional LoadingScreen instance for progress updates
            force_device: Optional device selection ("cpu" or "cuda"). If None, auto-detect.
            
        Returns:
            bool: Success status
        """
        if self._initialized:
            return True
        
        self.loading_screen = loading_screen
        
        try:
            if loading_screen:
                loading_screen.update_progress(5, "🔄 Preparing to load models...")
            
            print("🔄 Loading Chatterbox TTS models... (this may take a minute)")
            
            # Check for force stop
            if loading_screen and loading_screen.is_stopped():
                print("⚠️ Loading cancelled by user")
                return False
            
            # Set cache directory to user's home folder (works in both dev and frozen exe)
            import os
            cache_dir = Path.home() / ".cache" / "chatterbox_tts"
            cache_dir.mkdir(parents=True, exist_ok=True)
            os.environ['HF_HOME'] = str(cache_dir)
            os.environ['TRANSFORMERS_CACHE'] = str(cache_dir / "transformers")
            print(f"📁 Cache directory: {cache_dir}")
            
            # Import chatterbox-tts
            print("📦 Attempting to import chatterbox modules...")
            try:
                print("  - Importing torch...")
                import torch
                print(f"  ✅ Torch version: {torch.__version__}")
                
                print("  - Importing ChatterboxTTS...")
                from chatterbox.tts import ChatterboxTTS
                print("  ✅ ChatterboxTTS imported")
                
                print("  - Importing ChatterboxMultilingualTTS...")
                from chatterbox.mtl_tts import ChatterboxMultilingualTTS
                print("  ✅ ChatterboxMultilingualTTS imported")
                
            except ImportError as ie:
                error_msg = f"Failed to import chatterbox_tts library: {ie}"
                print(f"❌ {error_msg}")
                print("Full traceback:")
                traceback.print_exc()
                if loading_screen:
                    loading_screen.update_progress(0, "❌ Missing chatterbox_tts library")
                messagebox.showerror("Import Error", f"{error_msg}\n\nPlease ensure chatterbox_tts is installed:\npip install chatterbox-tts")
                return False
            
            # Handle device selection
            if force_device:
                # User explicitly chose a device
                if force_device == "cuda" and torch.cuda.is_available():
                    self.device = "cuda"
                    self.device_name = f"GPU ({torch.cuda.get_device_name(0)})"
                    print(f"✅ Using selected GPU: {self.device_name}")
                    print(f"   CUDA Version: {torch.version.cuda}")
                    print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
                else:
                    self.device = "cpu"
                    self.device_name = "CPU"
                    print(f"✅ Using selected CPU")
            else:
                # Auto-detect (fallback for backward compatibility)
                if torch.cuda.is_available():
                    self.device = "cuda"
                    self.device_name = f"GPU ({torch.cuda.get_device_name(0)})"
                    print(f"✅ GPU detected: {self.device_name}")
                    print(f"   CUDA Version: {torch.version.cuda}")
                    print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
                else:
                    self.device = "cpu"
                    self.device_name = "CPU"
                    print("⚠️ No GPU detected, using CPU (slower)")
            
            if loading_screen:
                loading_screen.update_progress(10, f"📦 Using {self.device_name}...")
            
            # Check for force stop
            if loading_screen and loading_screen.is_stopped():
                print("⚠️ Loading cancelled by user")
                return False
            
            # Monkey-patch torch.load to force CPU mapping for chatterbox models
            original_torch_load = torch.load
            def patched_torch_load(f, *args, **kwargs):
                # Force map_location to CPU if not specified
                if 'map_location' not in kwargs:
                    kwargs['map_location'] = torch.device('cpu')
                return original_torch_load(f, *args, **kwargs)
            
            torch.load = patched_torch_load
            
            try:
                if loading_screen:
                    loading_screen.update_progress(20, "🔊 Loading English TTS model...")
                
                # Check for force stop
                if loading_screen and loading_screen.is_stopped():
                    print("⚠️ Loading cancelled by user")
                    return False
                
                # Initialize English model
                print("📥 Calling ChatterboxTTS.from_pretrained()...")
                print(f"   Device: {self.device}")
                print(f"   Cache dir: {cache_dir}")
                print(f"   Cache dir exists: {cache_dir.exists()}")
                if cache_dir.exists():
                    print(f"   Cache dir contents: {list(cache_dir.iterdir())[:5]}")  # First 5 items
                
                try:
                    self.model = ChatterboxTTS.from_pretrained(device=self.device)
                    print("✅ English model loaded successfully")
                except Exception as model_error:
                    print(f"❌ Failed to load English model: {model_error}")
                    print(f"   Error type: {type(model_error).__name__}")
                    traceback.print_exc()
                    raise  # Re-raise to be caught by outer except
                
                if loading_screen:
                    loading_screen.update_progress(50, "🌍 Loading Multilingual TTS model...")
                
                # Check for force stop
                if loading_screen and loading_screen.is_stopped():
                    print("⚠️ Loading cancelled by user")
                    return False
                
                # Initialize multilingual model
                print("📥 Calling ChatterboxMultilingualTTS.from_pretrained()...")
                try:
                    self.multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=self.device)
                    print("✅ Multilingual model loaded successfully")
                except Exception as model_error:
                    print(f"❌ Failed to load Multilingual model: {model_error}")
                    print(f"   Error type: {type(model_error).__name__}")
                    traceback.print_exc()
                    raise  # Re-raise to be caught by outer except
                
                if loading_screen:
                    loading_screen.update_progress(90, "✨ Finalizing setup...")
            finally:
                # Restore original torch.load
                torch.load = original_torch_load
            
            if loading_screen:
                loading_screen.update_progress(100, "✅ Models loaded successfully!")
            
            print("✅ Chatterbox TTS models loaded successfully!")
            
            self._initialized = True
            return True
        except Exception as e:
            if loading_screen:
                loading_screen.update_progress(0, f"❌ Error: {str(e)[:50]}")
            print(f"❌ Error initializing TTS model: {e}")
            traceback.print_exc()
            return False
    
    def generate_audio(
        self,
        text: str,
        voice_config: Dict[str, Any],
        expression_config: Dict[str, Any],
        output_path: Path,
        language_code: str = "en",
        progress_callback=None
    ) -> Optional[Path]:
        """
        Generate audio from text
        
        Args:
            text: Input text to synthesize
            voice_config: Voice configuration dict (has 'mode', 'voice', 'custom_path')
            expression_config: Expression configuration dict (has 'mode', 'text' or parameters)
            output_path: Path where audio will be saved
            language_code: Language code (e.g., "en", "ja", "zh")
            progress_callback: Optional callback function(percentage, status) for progress updates
            
        Returns:
            Optional[Path]: Path to generated audio or None if failed
        """
        if not self.initialize():
            return None
        
        if not text.strip():
            print("❌ Cannot generate audio: Text is empty")
            return None
        
        try:
            if progress_callback:
                progress_callback(10, "Preparing generation...")
            
            print("\n🎤 Generating audio...")
            print(f"   Device: {self.device_name}")
            print(f"   Text: {text[:50]}..." if len(text) > 50 else f"   Text: {text}")
            print(f"   Voice Mode: {voice_config.get('mode', 'Default')}")
            print(f"   Language: {language_code}")
            
            # Get audio prompt path from voice configuration
            # Both predefined and custom voices provide audio files for voice cloning
            audio_prompt_path = None
            
            if voice_config.get("mode") == "predefined" and voice_config.get("voice_file"):
                # Predefined voice - use voice file from reference_voices folder
                audio_prompt_path = str(voice_config["voice_file"])
                print(f"   → Using predefined voice: {voice_config.get('voice')} ({audio_prompt_path})")
            elif voice_config.get("mode") == "custom" and voice_config.get("custom_path"):
                # Custom voice - use user-uploaded file
                audio_prompt_path = str(voice_config["custom_path"])
                print(f"   → Using custom voice: {audio_prompt_path}")
            else:
                print(f"   → Using default model voice (no reference audio)")

            
            # Get expression parameters
            # Chatterbox TTS API parameters:
            # - exaggeration (0.25-2.0): Controls expressiveness/exaggeration
            # - cfg_weight (0.01-1.0): Controls speech rate (lower = faster, higher = slower)
            # - temperature (0.05-5.0): Controls variation/emphasis in delivery
            # - pitch: Post-processing pitch shift in semitones (-12 to +12)
            mode = expression_config.get("mode", "preset")
            if mode in ["parameters", "preset"]:
                # Use values directly from config (works for both parameters and preset modes)
                exaggeration = expression_config.get("energy", 0.70)     # 0.25-2.0 (default: 0.7)
                cfg_weight = expression_config.get("speed", 0.40)        # 0.01-1.0 (default: 0.4) - speech rate
                temperature = expression_config.get("emphasis", 0.90)    # 0.05-5.0 (default: 0.9) - variation
                pitch_shift = expression_config.get("pitch", 0)          # semitones
            else:
                # Default values for text mode (Chatterbox official defaults)
                exaggeration = 0.70
                cfg_weight = 0.40
                temperature = 0.90
                pitch_shift = 0
            
            if progress_callback:
                status_msg = f"Synthesizing speech on {self.device_name}, please wait..."
                progress_callback(30, status_msg)
            
            # Track generation time for helpful messages
            import time
            import threading
            start_time = time.time()
            long_generation_warned = False
            generation_complete = False
            
            # Smooth progress bar animation
            current_progress = 30
            target_progress = 50  # First target
            
            def update_progress_smoothly():
                """Smoothly update progress bar using exponential approach"""
                nonlocal current_progress, target_progress, long_generation_warned, generation_complete
                
                while not generation_complete:
                    time.sleep(1)  # Update every 1 second
                    
                    if generation_complete:
                        break
                    
                    # Calculate new progress using formula:
                    # remaining = target - current
                    # new_progress = current + (remaining / 16)
                    remaining = target_progress - current_progress
                    
                    if remaining > 0.5:  # Only update if there's meaningful progress
                        current_progress = current_progress + (remaining / 16)
                        
                        # Update progress bar
                        if progress_callback:
                            progress_callback(int(current_progress), status_msg)
                    
                    # Check if we've been running for 30 seconds
                    elapsed = time.time() - start_time
                    if elapsed >= 30 and not long_generation_warned:
                        long_generation_warned = True
                        target_progress = 85  # Move target to 85
                        if progress_callback:
                            progress_callback(
                                int(current_progress), 
                                "⏳ This is taking a while... Longer or complex text may take 1-2 minutes on CPU"
                            )
                        print("   ⏳ Note: Generation taking longer than expected - this is normal for long/complex text on CPU")
                    
                    # If we're at 85, move to final phase
                    if current_progress >= 84 and target_progress == 85:
                        target_progress = 99  # Approach 99 but never reach 100
                    
                    # Cap at 99 until generation actually completes
                    if current_progress >= 99:
                        current_progress = 99
            
            # Start smooth progress animation
            progress_thread = threading.Thread(target=update_progress_smoothly, daemon=True)
            progress_thread.start()
            
            # Generate audio (GPU: 2-10 seconds, CPU: 10-60 seconds depending on text length)
            if language_code == "en":
                # Use English-only model for better quality
                print(f"   Using English model (exaggeration={exaggeration:.2f}, cfg_weight={cfg_weight:.2f}, temperature={temperature:.2f})")
                wav = self.model.generate(
                    text,
                    audio_prompt_path=audio_prompt_path,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight,
                    temperature=temperature
                )
            else:
                # Use multilingual model
                print(f"   Using multilingual model (language={language_code}, exaggeration={exaggeration:.2f}, cfg_weight={cfg_weight:.2f}, temperature={temperature:.2f})")
                wav = self.multilingual_model.generate(
                    text,
                    language_id=language_code,
                    audio_prompt_path=audio_prompt_path,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight,
                    temperature=temperature
                )
            
            # Mark that generation completed (stop the progress animation)
            generation_complete = True
            generation_time = time.time() - start_time
            print(f"   ✅ Generation completed in {generation_time:.1f} seconds")
            
            # Apply pitch shifting if needed (post-processing using Parselmouth/Praat)
            if pitch_shift != 0:
                if progress_callback:
                    progress_callback(85, f"Applying pitch shift ({pitch_shift:+d} semitones)...")
                
                # Warn about extreme pitch shifts
                if abs(pitch_shift) > 6:
                    print(f"   ⚠️ Warning: Large pitch shift ({pitch_shift:+d} semitones) may affect quality")
                    print(f"   💡 Tip: For best results, keep pitch shifts within ±6 semitones")
                
                print(f"   Applying pitch shift: {pitch_shift:+d} semitones with Praat (formant preservation)")
                
                try:
                    import parselmouth
                    from parselmouth.praat import call
                    import numpy as np
                    
                    # Convert tensor to numpy if needed
                    if hasattr(wav, 'cpu'):
                        wav_np = wav.cpu().numpy()
                    else:
                        wav_np = wav
                    
                    # Parselmouth expects shape (samples,) or (channels, samples)
                    # Handle multi-channel audio
                    if wav_np.ndim > 1:
                        # Process each channel separately to preserve quality
                        shifted_channels = []
                        for channel in wav_np:
                            # Create Parselmouth Sound object
                            sound = parselmouth.Sound(channel, sampling_frequency=self.model.sr)
                            
                            # Calculate pitch multiplication factor from semitones
                            # factor = 2^(semitones/12)
                            pitch_factor = 2 ** (pitch_shift / 12.0)
                            
                            # Use Praat's Manipulation to change pitch while preserving formants
                            manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
                            pitch_tier = call(manipulation, "Extract pitch tier")
                            call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, pitch_factor)
                            call([pitch_tier, manipulation], "Replace pitch tier")
                            sound_shifted = call(manipulation, "Get resynthesis (overlap-add)")
                            
                            # Get numpy array from result and flatten if needed
                            shifted_audio = sound_shifted.values
                            if shifted_audio.ndim > 1:
                                shifted_audio = shifted_audio.flatten()
                            shifted_channels.append(shifted_audio)
                        
                        wav_np = np.stack(shifted_channels)
                    else:
                        # Single channel processing
                        sound = parselmouth.Sound(wav_np, sampling_frequency=self.model.sr)
                        
                        # Calculate pitch multiplication factor
                        pitch_factor = 2 ** (pitch_shift / 12.0)
                        
                        # Apply pitch manipulation with formant preservation
                        manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
                        pitch_tier = call(manipulation, "Extract pitch tier")
                        call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, pitch_factor)
                        call([pitch_tier, manipulation], "Replace pitch tier")
                        sound_shifted = call(manipulation, "Get resynthesis (overlap-add)")
                        
                        # Get numpy array and flatten if needed
                        wav_np = sound_shifted.values
                        if wav_np.ndim > 1:
                            wav_np = wav_np.flatten()
                    
                    # Convert back to tensor if original was tensor
                    if hasattr(wav, 'cpu'):
                        import torch
                        wav = torch.from_numpy(wav_np).to(wav.device)
                    else:
                        wav = wav_np
                    
                    print(f"   ✅ Pitch shift applied with formant preservation (Praat)")
                    
                except ImportError:
                    print("   ⚠️ Parselmouth not installed. Falling back to librosa...")
                    print("   Install with: pip install praat-parselmouth")
                    
                    # Fallback to librosa
                    import librosa
                    import numpy as np
                    
                    if hasattr(wav, 'cpu'):
                        wav_np = wav.cpu().numpy()
                    else:
                        wav_np = wav
                    
                    if wav_np.ndim > 1:
                        shifted_channels = []
                        for channel in wav_np:
                            shifted = librosa.effects.pitch_shift(
                                channel, sr=self.model.sr, n_steps=pitch_shift, res_type='soxr_hq'
                            )
                            shifted_channels.append(shifted)
                        wav_np = np.stack(shifted_channels)
                    else:
                        wav_np = librosa.effects.pitch_shift(
                            wav_np, sr=self.model.sr, n_steps=pitch_shift, res_type='soxr_hq'
                        )
                    
                    if hasattr(wav, 'cpu'):
                        import torch
                        wav = torch.from_numpy(wav_np).to(wav.device)
                    else:
                        wav = wav_np
                    
                    print(f"   ✅ Pitch shift applied (librosa fallback)")
                    
                except Exception as e:
                    print(f"   ❌ Pitch shift failed: {str(e)}")
                    print(f"   Continuing with original audio...")
            
            if progress_callback:
                progress_callback(90, "Saving audio file...")
            
            # Save audio
            output_path.parent.mkdir(parents=True, exist_ok=True)
            ta.save(str(output_path), wav, self.model.sr)
            
            if progress_callback:
                progress_callback(100, "Audio generated successfully!")
            
            print(f"✅ Audio generated successfully: {output_path}")
            
            # Clear GPU cache if using CUDA
            if self.device == "cuda":
                import torch
                torch.cuda.empty_cache()
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            traceback.print_exc()
            return None
    
    def cleanup(self):
        """Cleanup resources"""
        if self.model:
            # Clear GPU memory if using CUDA
            if self.device == "cuda":
                import torch
                self.model = None
                self.multilingual_model = None
                torch.cuda.empty_cache()
                print("🧹 GPU memory cleared")
        self._initialized = False


# Global instance
tts_generator = TTSGenerator()
