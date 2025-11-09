# Quick Start Guide

## � About This Project

This is a desktop TTS (Text-to-Speech) application built with Chatterbox TTS, created to generate character voices for the **Pixuu's Pixel Adventure** animation project.

---

## �🚀 For New Users (First Time Setup)

### Step 1: Install Prerequisites
1. Install **Python 3.11** from https://www.python.org/downloads/
2. Install **Microsoft C++ Build Tools** from https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Select "Desktop development with C++" workload
3. **(Optional but Recommended)** If you have an NVIDIA GPU and want faster generation:
   - Ensure you have updated GPU drivers
   - PyTorch with CUDA support will be installed automatically

### Step 2: Clone Repository
```powershell
git clone https://github.com/JeroTan/chatterbox-portable-gui.git
cd chatterbox-portable-gui
```

### Step 3: Automated Setup (Recommended)
```powershell
py -3.11 setup.py
```
This will:
- Create virtual environment
- Install all dependencies (~3-4 GB, takes 8-15 minutes)
- Install PyTorch with CUDA support for GPU acceleration
- Set everything up automatically

### Step 4: Activate Environment
```powershell
.venv\Scripts\activate
```

You should see `(.venv)` at the start of your prompt.

### Step 5: Verify Installation
```powershell
python -c "import chatterbox_tts; print('✅ Chatterbox TTS installed successfully!')"
```

---

## 🔄 For Returning Users (Already Set Up)

Every time you work on the project:

```powershell
# 1. Navigate to project
cd path\to\chatterbox-codebase

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Start coding!
```

---

## 📦 Manual Setup (Alternative)

If automated setup fails:

```powershell
# 1. Create virtual environment
py -3.11 -m venv .venv

# 2. Activate it
.venv\Scripts\activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install wheel setuptools
pip install "numpy>=1.24.0,<1.26.0"
pip install --no-build-isolation pkuseg==0.0.25
pip install chatterbox-tts
```

---

## 🆘 Troubleshooting

### "py -3.11 not found"
- Python 3.11 is not installed
- Install from https://www.python.org/downloads/

### "Cannot be loaded because running scripts is disabled"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Microsoft Visual C++ 14.0 or greater is required"
- Install Microsoft C++ Build Tools
- Select "Desktop development with C++" workload

### "No module named 'chatterbox_tts'"
- Make sure virtual environment is activated (you should see `(.venv)` in prompt)
- Run: `.venv\Scripts\activate`

### GPU not being used / slow generation
- Install PyTorch with CUDA:
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
- Restart the application and select GPU option

### Device selector or loading screen not showing
- Check if windows are minimized or behind other windows
- Press Alt+Tab to switch between windows
- Close with X button on device selector to exit app

---

## 📝 Basic Usage

### Running the Application
```powershell
# Make sure virtual environment is activated
.venv\Scripts\activate

# Run the desktop app
python src/main.py
```

### First Launch
1. **Device Selection** - Choose CPU (stable) or GPU (fast) for audio generation
2. **Loading Screen** - Wait for models to load (first time takes longer)
3. **Main Window** - Ready to generate audio!

### Download Voice Samples (Recommended)
```powershell
# Download 256 official voice samples (93 MB)
python download_voice_samples.py
```
This provides:
- Default male/female voices for all 23 languages
- 256 additional samples to choose from in `src/assets/downloads/`

### Using the Application
1. **Enter Text** - Type or paste text in the text input area
2. **Select Language** - Choose from 23 supported languages
3. **Choose Voice** - Select predefined voice (updates automatically per language) or upload custom reference audio
   - Predefined voices loaded from `src/assets/reference_voices/[language]/`
   - Filter by Male/Female/All with fancy dropdown
   - Add custom voices by copying files to language folders
4. **Set Expression** - Describe emotion ("happy", "calm", etc.) or use parameter controls
5. **Generate** - Click "Generate Audio" button
6. **Preview** - Use built-in player with scrubber to listen
7. **Auto-Save** - Audio automatically saved to `output/` folder

### Generation Speed
- **CPU Mode**: 10-60 seconds (stable, recommended)
- **GPU Mode**: 2-10 seconds (fast, requires NVIDIA GPU with CUDA)

---

## 🎯 Common Commands

```powershell
# Activate environment
.venv\Scripts\activate

# Deactivate environment
deactivate

# Check Python version
python --version

# List installed packages
pip list

# Update a package
pip install --upgrade package-name

# Install new package
pip install package-name
```

---

## 📚 More Information

- Full documentation: `README.md`
- Setup details: `SETUP_SUMMARY.md`
- All dependencies: `requirements-full.txt`

---

## ⏱️ Expected Times

| Task | Time |
|------|------|
| First-time setup | 8-15 minutes |
| Activate environment | 2 seconds |
| Install new package | Varies |

---

## 💾 Disk Space

- Total installation: ~3-4 GB (including CUDA libraries)
- Make sure you have at least 6 GB free space

---

## ✅ Checklist

- [ ] Python 3.11 installed
- [ ] Microsoft C++ Build Tools installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Installation verified
- [ ] Ready to code! 🎉
