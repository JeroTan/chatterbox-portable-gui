# Chatterbox TTS GUI - Feature Documentation

A desktop Text-to-Speech application for generating character voices, created for the **Pixuu's Pixel Adventure** animation project.

Complete list of features and capabilities.

---

## 🚀 Core Features

### 1. Device Selection (GPU/CPU)
**Location:** Startup Dialog

Choose your processing device for audio generation:

- **CPU Mode (Recommended)**
  - Generation time: 10-60 seconds
  - More stable and reliable
  - Works on all systems
  - No special hardware required

- **GPU Mode**
  - Generation time: 2-10 seconds (5-10x faster)
  - Requires NVIDIA GPU with CUDA support
  - Automatic detection of GPU capabilities
  - Shows GPU name and CUDA version
  - Memory information display

**User Flow:**
1. Device selector appears on app startup (before loading screen)
2. Window auto-sizes to fit content
3. CPU shown first as recommended option
4. GPU info displayed with green text if available
5. Closing dialog (X button) exits app without loading

---

## 🌍 Multilingual Support

### 2. Language Selection
**Location:** Language Selector Component

Generate speech in 23 languages:

**Supported Languages:**
- Arabic (ar)
- Danish (da)
- German (de)
- Greek (el)
- English (en)
- Spanish (es)
- Finnish (fi)
- French (fr)
- Hebrew (he)
- Hindi (hi)
- Italian (it)
- Japanese (ja)
- Korean (ko)
- Malay (ms)
- Dutch (nl)
- Norwegian (no)
- Polish (pl)
- Portuguese (pt)
- Russian (ru)
- Swedish (sv)
- Swahili (sw)
- Turkish (tr)
- Chinese (zh)

**Features:**
- Searchable dropdown with live filtering
- Language codes mapped to full names
- Reusable component architecture
- Grid layout for easy browsing

---

## 🎙️ Voice Selection

### 3. Voice Modes
**Location:** Voice Selector Component

Two ways to select voices:

#### Predefined Voices
- **Dynamic Loading:** Voices loaded from `src/assets/reference_voices/[language]/`
- **Language-Aware:** Voice list updates automatically when language changes
- **Male/Female/All Filtering:** Quick filter buttons with visual feedback
- **Fancy Grid Dropdown:** 3-column searchable popup
- **Default Voices:** Each language has male_default.wav and female_default.wav
- **Extensible:** Add voices by copying audio files to language folders
- **256 Samples:** Official voice samples available in `src/assets/downloads/`

**Voice Organization:**
```
reference_voices/
├── en/
│   ├── male_default.wav
│   ├── female_default.wav
│   └── [custom voices...]
├── ja/
│   ├── male_default.wav
│   └── female_default.wav
└── [23 languages total...]
```

#### Custom Voice (Reference Audio)
- Upload your own reference audio file
- Browse and select WAV/MP3/FLAC files
- Voice cloning from custom samples
- Path display for selected file

**Adding Custom Voices:**
1. Browse `src/assets/downloads/` for samples
2. Copy desired files to `reference_voices/[language]/`
3. Name descriptively (e.g., `male_british.wav`)
4. Voice appears automatically in dropdown!

---

## 🎭 Expression Controls

### 4. Expression Modes
**Location:** Expression Controls Component

#### Text Mode (Default)
- Free-form text description of emotion
- Examples: "happy and energetic", "calm narrator", "serious and professional"
- Placeholder text replaced with "default" if not changed
- Natural language processing

#### Parameter Mode
Fine-tune voice characteristics:
- **Emotion:** Predefined emotion selection
- **Energy:** 0-100 slider
- **Speed:** 0.5-2.0x multiplier
- **Pitch:** -12 to +12 semitones
- **Emphasis:** 0-100 intensity

---

## 🎵 Audio Generation

### 5. TTS Generation
**Location:** Generate Button

**Features:**
- Real-time progress tracking (percentage + status)
- Disabled UI during generation (prevents errors)
- Device information display (CPU/GPU)
- Honest progress messages (no fake progress)
- Thread-safe progress callbacks
- Temporary file management

**Generation Info Display:**
```
Generating audio...
   Device: CPU/GPU
   Text: [Your text]
   Voice: [Selected voice]
   Expression: [default or custom]
   Language: [Language code]
```

**Performance:**
- CPU: 10-60 seconds
- GPU: 2-10 seconds
- Progress updates in real-time
- Automatic error handling

---

## 🔊 Audio Playback

### 6. Built-in Audio Player
**Location:** Audio Player Component

**Features:**
- **Play/Pause Toggle Button** - Single button for both actions
- **Audio Scrubber** - Visual timeline with drag support
- **Millisecond Precision** - Time display in M:SS.mmm format
- **Click-to-Seek** - Click anywhere on timeline to jump
- **Real-time Updates** - Position updates while playing
- **Total Duration Display** - Shows full audio length
- **Event-based Controls** - No callback delays

**Player Controls:**
- Play/Pause: Space bar or button click
- Seek: Click or drag scrubber
- Position displayed as: `0:03.450 / 0:15.230`

---

## 💾 File Management

### 7. Auto-Export System
**Location:** Automatic on Generation

**Features:**
- Saves to `output/` folder automatically
- Smart naming: `audio_1.wav`, `audio_2.wav`, etc.
- Automatic duplicate handling with incremental numbers
- No file selection dialog (streamlined UX)
- Temporary files cleaned up automatically
- Single success notification

**File Naming Pattern:**
```
output/
├── audio_1.wav
├── audio_2.wav
├── audio_3.wav
└── ...
```

---

## 🎨 User Interface

### 8. Component Architecture
**Philosophy:** Modular, reusable components

**Components:**
- `DropdownComponent` - Reusable searchable dropdown
- `DeviceSelector` - GPU/CPU selection dialog
- `LanguageSelector` - 23 language dropdown
- `VoiceSelector` - Voice selection with filters
- `ExpressionControls` - Emotion/parameter controls
- `LoadingScreen` - Model loading with progress
- `AudioPlayer` - Built-in audio preview
- `TextInput` - Text entry area

**Design Principles:**
- Component reusability
- Props-based configuration
- Event callbacks
- Grid layouts
- Responsive sizing
- Auto-height windows

---

## ⏳ Loading Experience

### 9. Loading Screen
**Location:** After Device Selection

**Features:**
- Progress bar with percentage
- Status messages during loading
- Force Stop button to cancel loading
- Device information display
- Modal window (always on top)
- Centered on screen
- Dark theme

**Loading Phases:**
1. Preparing to load models (5%)
2. Loading device info (10%)
3. Loading ChatterboxTTS (30-50%)
4. Loading Multilingual model (60-80%)
5. Initialization complete (100%)

---

## 🎯 UX Improvements

### 10. User Experience Features

**During Generation:**
- All buttons disabled
- Progress shown in status bar
- Can't trigger multiple generations
- Clear device indicator

**Error Prevention:**
- Validation before generation
- Clear error messages
- No placeholder text in output
- Proper default values

**Visual Feedback:**
- Green text for available GPU
- Gray text for unavailable features
- Progress percentages
- Device name display
- Real-time status updates

**Smart Defaults:**
- Male voice as default
- CPU recommended for stability
- Expression defaults to "default"
- Sensible parameter values

---

## 🔧 Technical Features

### 11. GPU Acceleration

**CUDA Support:**
- PyTorch 2.5.1 with CUDA 12.1
- Automatic GPU detection
- Device memory information
- CUDA version display
- GPU cache clearing after generation
- Fallback to CPU if needed

**Optimizations:**
- Models loaded directly on selected device
- Memory-efficient processing
- Automatic cleanup
- Device-specific optimizations

### 12. Model Management

**Chatterbox Models:**
- ChatterboxTTS (English)
- ChatterboxMultilingualTTS (23 languages)
- Automatic model downloading
- hf_xet for faster downloads
- Model caching
- Loading progress tracking

---

## 🛠️ Developer Features

### 13. Code Quality

**Architecture:**
- Modular component structure
- Separation of concerns
- State management
- Event-driven callbacks
- Thread-safe UI updates

**Components:**
```
src/
├── components/     # Reusable UI components
├── features/       # Core functionality
├── utils/          # Helper functions
└── store/          # State management
```

**Best Practices:**
- Component reusability
- DRY principle
- Clean code structure
- Proper error handling
- Progress tracking
- Resource cleanup

---

## 📊 Performance

### Generation Times
| Device | Average Time | Range |
|--------|--------------|-------|
| CPU    | 20-30s       | 10-60s |
| GPU    | 5s           | 2-10s  |

### Resource Usage
| Component | Size |
|-----------|------|
| Base installation | ~3-4 GB |
| PyTorch + CUDA | ~2 GB |
| Models | ~1 GB |
| Generated audio | ~100-500 KB each |

---

## 🎨 UI Features Summary

✅ Device selection dialog with auto-sizing
✅ Loading screen with progress and force stop
✅ 23 language support with searchable dropdown
✅ Male/Female voice filtering
✅ Text or parameter-based expression control
✅ Built-in audio player with scrubber
✅ Auto-export to output folder
✅ Real-time progress tracking
✅ Disabled UI during generation
✅ Millisecond-precision timeline
✅ Click-to-seek and drag scrubber
✅ Play/pause toggle button
✅ Smart file naming with duplicates
✅ Default male voice
✅ Expression defaults to "default"
✅ CPU recommended for stability
✅ GPU option for speed

---

## 🚀 Future Enhancements

Potential features for future versions:

- [ ] Batch processing multiple texts
- [ ] Playlist management
- [ ] Voice mixing/blending
- [ ] Real-time preview while typing
- [ ] Export to multiple formats (MP3, OGG)
- [ ] Keyboard shortcuts
- [ ] Dark/light theme toggle
- [ ] Preset management
- [ ] Voice favorites
- [ ] Generation history
- [ ] Undo/redo support
- [ ] Project templates
- [ ] Cloud sync
- [ ] Voice training interface
- [ ] Voice sample preview before generation
- [ ] Bulk voice sample import/organization

---

## 📚 Related Documentation

- `README.md` - Main documentation and setup
- `QUICKSTART.md` - Quick start guide
- `GUI_REQUIREMENTS.md` - Original GUI specifications
- `download_voice_samples.py` - Voice sample downloader script

---

**Last Updated:** November 8, 2025
**Version:** 1.1.0
**Python:** 3.11
**PyTorch:** 2.5.1+cu121
**Chatterbox TTS:** 0.1.4
**Voice Samples:** 256 official samples (93 MB)
