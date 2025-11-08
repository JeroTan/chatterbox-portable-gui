"""
TTS Generation Feature
Handles audio generation using chatterbox-tts
"""

from pathlib import Path
from typing import Optional, Dict, Any
import traceback
import torchaudio as ta


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
            
            # Import chatterbox-tts
            from chatterbox.tts import ChatterboxTTS
            from chatterbox.mtl_tts import ChatterboxMultilingualTTS
            import torch
            
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
                self.model = ChatterboxTTS.from_pretrained(device=self.device)
                
                if loading_screen:
                    loading_screen.update_progress(50, "🌍 Loading Multilingual TTS model...")
                
                # Check for force stop
                if loading_screen and loading_screen.is_stopped():
                    print("⚠️ Loading cancelled by user")
                    return False
                
                # Initialize multilingual model
                self.multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=self.device)
                
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
            # Chatterbox uses: exaggeration (0.0-1.0) and cfg_weight (0.0-1.0)
            if expression_config.get("mode") == "parameters":
                # Map our energy (0-100) to exaggeration (0.0-1.0)
                exaggeration = expression_config.get("energy", 50) / 100.0
                # Map our emphasis (0-100) to cfg_weight (0.0-1.0)
                cfg_weight = expression_config.get("emphasis", 30) / 100.0
            else:
                # Default values for text mode
                exaggeration = 0.5
                cfg_weight = 0.5
            
            if progress_callback:
                status_msg = f"Synthesizing speech on {self.device_name}, please wait..."
                progress_callback(30, status_msg)
            
            # Generate audio (GPU: 2-10 seconds, CPU: 10-60 seconds depending on text length)
            if language_code == "en":
                # Use English-only model for better quality
                print(f"   Using English model (exaggeration={exaggeration:.2f}, cfg_weight={cfg_weight:.2f})")
                wav = self.model.generate(
                    text,
                    audio_prompt_path=audio_prompt_path,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
            else:
                # Use multilingual model
                print(f"   Using multilingual model (language={language_code}, exaggeration={exaggeration:.2f}, cfg_weight={cfg_weight:.2f})")
                wav = self.multilingual_model.generate(
                    text,
                    language_id=language_code,
                    audio_prompt_path=audio_prompt_path,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
            
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
