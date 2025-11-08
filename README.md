# Chatterbox TTS GUI

> 📝 **Note:** This documentation was created with the assistance of **Claude Sonnet** (Anthropic's AI assistant) working through GitHub Copilot in VS Code. Claude helped troubleshoot installation issues, resolve Python compatibility problems, and generate comprehensive documentation to ensure a smooth setup experience.

A desktop Text-to-Speech application using Chatterbox TTS, created to generate character voices for the **Pixuu's Pixel Adventure** animation project.

## 📋 Prerequisites

- **Python 3.11** (Required - NOT 3.12, 3.13, or 3.14)
- **Microsoft Visual C++ Build Tools** (Required for building certain dependencies)
- Git

## 🚀 Quick Start

### Windows Setup

1. **Clone the repository**
   ```powershell
   git clone <your-repo-url>
   cd chatterbox-codebase
   ```

2. **Run the setup script** (Recommended - Like `npm install`)
   ```powershell
   # Using PowerShell (Recommended)
   .\run.ps1 setup
   
   # OR using Batch
   run.bat setup
   
   # OR directly
   python setup.py
   ```

   OR manually:

3. **Create virtual environment with Python 3.11**
   ```powershell
   py -3.11 -m venv .venv
   ```

4. **Activate virtual environment**
   ```powershell
   .venv\Scripts\activate
   ```

5. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

## 📦 What Gets Installed

The setup process installs the following main packages:

### Core TTS Engine
- **chatterbox-tts** (0.1.4) - Main text-to-speech engine with multilingual support (23 languages)
- **torch** (2.5.1+cu121) - PyTorch with CUDA 12.1 support for GPU acceleration
- **torchaudio** (2.5.1+cu121) - Audio processing with GPU support
- **transformers** (4.46.3) - Hugging Face transformers
- **diffusers** (0.29.0) - Diffusion models

### Desktop GUI
- **tkinter** (built-in) - Native desktop interface with custom components

### Audio Processing & Playback
- **pygame** - Audio playback and scrubbing control
- **torchaudio** - Audio I/O and WAV file operations
- **hf_xet** - Faster HuggingFace model downloads

### Performance
- **CUDA Support** - GPU acceleration for 5-10x faster generation (2-10 seconds vs 10-60 seconds on CPU)
- **Device Selection** - Choose between CPU (stable) or GPU (fast) at startup

Total installation size: **~3-4 GB** (including CUDA libraries)

### Development Tools (Optional)
Install with: `pip install -r requirements-dev.txt`
- PyInstaller - Create portable executables
- Black, Flake8 - Code quality
- Pytest - Testing framework
- And more...

## 🔧 Troubleshooting

### Issue: "AttributeError: module 'pkgutil' has no attribute 'ImpImporter'"
**Solution:** You're using Python 3.14. Downgrade to Python 3.11.

### Issue: "error: Microsoft Visual C++ 14.0 or greater is required"
**Solution:** Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Select "Desktop development with C++" workload
- This is needed to compile `pkuseg` dependency

### Issue: "ModuleNotFoundError: No module named 'numpy'"
**Solution:** This was resolved by installing numpy before pkuseg. The requirements.txt handles this automatically.

### Issue: GPU not being used / "CUDA not available"
**Solution:** Install PyTorch with CUDA support:
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
This installs PyTorch with CUDA 12.1 support for GPU acceleration.

### Issue: "RuntimeError: Attempting to deserialize object on a CUDA device"
**Solution:** Already handled automatically - the app monkey-patches `torch.load` to map CUDA tensors to CPU when needed.

### Issue: Virtual environment not activating
**Solution:** 
```powershell
# If you see an execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Loading screen or device selector not showing
**Solution:** The windows show automatically at startup. Check if they're minimized or behind other windows. Press Alt+Tab to switch between windows.

## 📁 Project Structure

```
chatterbox-codebase/
├── .venv/                          # Virtual environment (DO NOT commit)
├── .git/                           # Git repository
├── src/                            # Source code
│   ├── main.py                     # Main application entry point
│   ├── components/                 # Reusable UI components
│   │   ├── device_selector.py      # GPU/CPU selection dialog
│   │   ├── dropdown.py             # Reusable dropdown component
│   │   ├── text_input.py           # Text input area
│   │   ├── language_selector.py    # Language dropdown (23 languages)
│   │   ├── voice_selector.py       # Voice selection with filters
│   │   ├── expression_controls.py  # Expression/emotion controls
│   │   ├── loading_screen.py       # Model loading screen with progress
│   │   └── audio_player.py         # Built-in audio player with scrubber
│   ├── features/                   # Core functionality
│   │   ├── generate.py             # TTS generation with GPU/CPU support
│   │   ├── project.py              # Project save/load
│   │   └── export.py               # Audio export
│   ├── utils/                      # Utility functions
│   │   ├── config.py               # Configuration constants
│   │   └── file_utils.py           # File operations
│   ├── store/                      # State management
│   │   └── state.py                # Application state
│   └── assets/                     # Voice samples and assets
│       ├── downloads/              # ALL downloaded voice samples (93 MB, 256 files)
│       └── reference_voices/       # Active voices organized by language
│           ├── en/                 # English voices (male_default.wav, female_default.wav)
│           ├── ja/                 # Japanese voices
│           ├── zh/                 # Chinese voices
│           └── [21 more languages...]
├── output/                         # Generated audio files (auto-created)
├── projects/                       # Saved project files
├── download_voice_samples.py       # Script to download official voice samples
├── .gitignore                      # Git ignore file
├── README.md                       # This file
├── FEATURES.md                     # Feature documentation
├── GUI_REQUIREMENTS.md             # Complete GUI feature specifications
├── QUICKSTART.md                   # Quick start guide
├── SETUP_SUMMARY.md                # Detailed setup documentation
├── PORTABLE_BUILD_GUIDE.md         # How to create portable distribution
├── requirements.txt                # Python dependencies (production)
├── requirements-dev.txt            # Development dependencies
├── requirements-full.txt           # Complete pip freeze output
├── setup.py                        # Automated setup script
├── run.ps1                         # PowerShell script runner
└── run.bat                         # Batch script runner
```

## 🎮 Script Commands (Like npm scripts)

Similar to Node.js `package.json` scripts, you can use these commands:

### PowerShell (Recommended)
```powershell
.\run.ps1 setup       # Full setup (creates venv + installs everything)
.\run.ps1 install     # Install/update dependencies
.\run.ps1 test        # Test if chatterbox-tts is working
.\run.ps1 clean       # Remove virtual environment
.\run.ps1 freeze      # Update requirements-full.txt
.\run.ps1 list        # List all installed packages
.\run.ps1 help        # Show all commands
```

### Batch (Alternative)
```batch
run.bat setup         # Full setup
run.bat install       # Install dependencies
run.bat test          # Test installation
run.bat clean         # Remove venv
```

### Manual Activation
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Deactivate
deactivate
```

## 🔒 What's Not in Git

The following directories are excluded from version control (too large):
- `.venv/` - Virtual environment (~2-3 GB)
- `__pycache__/` - Python cache files
- Model weights and downloads (if any)

## 💡 Important Notes

1. **Always activate the virtual environment** before running any Python commands:
   ```powershell
   .venv\Scripts\activate
   ```

2. **Python Version**: Chatterbox was developed and tested on **Python 3.11** on Debian 11. Use Python 3.11 for best compatibility.

3. **Dependencies are pinned** in the original `pyproject.toml` to ensure consistency.

4. **Large Installation**: The complete installation is around 2-3 GB due to PyTorch and models.

## 🎯 Usage

### Running the Application
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the desktop application
python src/main.py
```

### Application Features

#### 1. Device Selection (Startup)
On first launch, choose your processing device:
- **CPU (Recommended)** - Slower (10-60s) but more stable and reliable
- **GPU** - Faster (2-10s) if you have NVIDIA GPU with CUDA support

#### 2. Multilingual Support
Generate audio in 23 languages:
- English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese
- Arabic, Danish, Dutch, Finnish, Greek, Hebrew, Hindi, Malay, Norwegian, Polish, Swedish, Swahili, Turkish

#### 3. Voice Selection
- **Predefined Voices** - Dynamically loaded from `src/assets/reference_voices/[language]/`
  - Voices update automatically when language changes
  - Filter by Male/Female/All with fancy grid dropdown
  - Each language has default male and female voices
  - Add more voices by copying audio files to language folders
- **Custom Voice** - Upload reference audio for voice cloning
- **Default**: Male voice (male_default.wav for selected language)
- **256 voice samples** available in `src/assets/downloads/` for manual review

#### 4. Expression Controls
- **Text Mode** - Describe emotion: "happy and energetic", "calm narrator", etc.
- **Parameter Mode** - Fine-tune emotion, energy, speed, pitch, emphasis

#### 5. Audio Generation
- Real-time progress tracking
- Disabled UI during generation to prevent errors
- Device information display (CPU/GPU)

#### 6. Built-in Audio Player
- Play/Pause toggle button
- Audio scrubber with millisecond precision (M:SS.mmm)
- Click-to-seek and drag scrubber
- Real-time position updates

#### 7. Auto-Export
- Saves to `output/` folder automatically
- Smart naming: `audio_1.wav`, `audio_2.wav`, etc.
- Temporary files cleaned up automatically

### For End Users (Portable Distribution)
Once the portable version is built:
1. Download `ChatterboxTTS-Portable.zip`
2. Extract to any location
3. Double-click `ChatterboxTTS.bat`
4. Application starts with GUI
5. No Python installation needed

See `PORTABLE_BUILD_GUIDE.md` for building distribution package.

## 🎙️ Voice Samples Setup

### Downloading Official Voice Samples
The project includes 256 official voice samples from Chatterbox:

```powershell
# Download all voice samples (93 MB)
python download_voice_samples.py
```

This creates:
- `src/assets/downloads/` - ALL 256 samples for manual review
- `src/assets/reference_voices/[lang]/` - Default male/female voices for each language

### Adding Custom Voices
1. Browse `src/assets/downloads/` to find voices you like
2. Copy desired voice files to `src/assets/reference_voices/[language]/`
3. Name them descriptively (e.g., `male_british.wav`, `female_young.wav`)
4. They appear automatically in the voice dropdown!

Example:
```powershell
# Add a British male voice to English
cp src/assets/downloads/prompts/male_uk_chef.flac src/assets/reference_voices/en/male_british.wav

# Add a narrator voice to Japanese
cp src/assets/downloads/mtl_samples23lang/ja/infer-00.wav src/assets/reference_voices/ja/male_narrator.wav
```

Voices are organized by language:
```
reference_voices/
├── en/  # English voices
├── ja/  # Japanese voices
├── zh/  # Chinese voices
└── ...  # 23 languages total
```

## 📝 Development History

### Voice System Overhaul (November 8, 2025)
1. ✅ Downloaded all 256 official voice samples from Chatterbox (93 MB)
2. ✅ Organized voices by language in `reference_voices/[lang]/` structure
3. ✅ Dynamic voice loading - voices update automatically when language changes
4. ✅ Default male/female voices for all 23 languages
5. ✅ Voice selector now uses actual audio files for voice cloning
6. ✅ Fixed predefined voices to work with reference audio files
7. ✅ Created download script for easy voice sample management

### GPU Acceleration & Device Selection (November 7, 2025)
1. ✅ Installed PyTorch with CUDA 12.1 support for GPU acceleration
2. ✅ Added device selector dialog (CPU/GPU choice at startup)
3. ✅ Implemented GPU detection and automatic optimization
4. ✅ CPU marked as recommended (stable), GPU available for speed
5. ✅ Auto-height device selector that fits content

### UI/UX Improvements (November 7, 2025)
1. ✅ Component-based architecture that are reusable
2. ✅ Added DropdownComponent for language and voice selection
3. ✅ Searchable dropdown with 23 language support
4. ✅ Loading screen with progress bar and force stop button
5. ✅ Built-in audio player with millisecond scrubber and seeking
6. ✅ Play/Pause toggle button
7. ✅ Auto-export to output folder with smart naming
8. ✅ Disabled UI during generation to prevent errors
9. ✅ Progress message when generating
10. ✅ Expression defaults to "default" instead of sending the placeholder message
11. ✅ Default voice changed to first available voice in assets

### Initial Setup Process (November 7, 2025)
1. ✅ Created Python 3.11 virtual environment
2. ✅ Resolved setuptools compatibility issues
3. ✅ Installed Microsoft C++ Build Tools for pkuseg compilation
4. ✅ Installed numpy first to resolve pkuseg build dependencies
5. ✅ Successfully installed chatterbox-tts and all dependencies
6. ✅ Implemented TTS functionality with English + multilingual models
7. ✅ Created desktop GUI with Tkinter

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

This means:
- ✅ You can use, modify, and distribute this software
- ✅ You must keep it open source
- ✅ Any modifications must also be GPL-3.0
- ✅ You must state changes made to the code
- ✅ You must include the original copyright notice

**In short:** This ensures the software and all its derivatives remain free and open source forever.

See the [LICENSE](LICENSE) file for the full license text, or visit https://www.gnu.org/licenses/gpl-3.0.en.html

**Copyright © 2025 JeroTan**

---

**About Pixuu's Pixel Adventure:**  
This TTS GUI was created to generate character voices for the Pixuu's Pixel Adventure animation project. The tool provides an easy way to create consistent, high-quality voice performances across multiple languages.

## 🔗 Resources

- [Chatterbox TTS GitHub Repository](https://github.com/resemble-ai/chatterbox) - Official source code and documentation
- [Chatterbox TTS on PyPI](https://pypi.org/project/chatterbox-tts/)
- [Python 3.11 Download](https://www.python.org/downloads/)
- [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
