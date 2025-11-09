# Setup Summary - November 7, 2025

## What We Did

### 1. Environment Setup
- ✅ Created Python 3.11 virtual environment (`.venv/`)
- ✅ Switched from Python 3.14 to Python 3.11 for compatibility

### 2. Dependency Installation
Successfully installed the following packages:

#### Core TTS Package
- `chatterbox-tts==0.1.4` - Main text-to-speech engine

#### Deep Learning (Heavy packages ~2GB+)
- `torch==2.6.0` - PyTorch
- `torchaudio==2.6.0` - Audio processing for PyTorch
- `transformers==4.46.3` - Hugging Face transformers
- `diffusers==0.29.0` - Diffusion models
- `safetensors==0.5.3` - Safe tensor serialization

#### Audio Processing
- `librosa==0.11.0` - Audio analysis
- `soundfile` - Audio I/O
- `audioread` - Audio file reading
- `soxr` - High-quality audio resampling

#### NLP & Tokenization
- `pkuseg==0.0.25` - Chinese word segmentation (compiled from source)
- `pykakasi==2.3.0` - Japanese text processing
- `s3tokenizer` - Custom tokenizer
- `tokenizers` - Fast tokenizers

#### Web Interface
- `gradio==5.44.1` - Web UI framework
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `httpx` - HTTP client

#### Numerical Computing
- `numpy==1.25.2` - Numerical arrays
- `scipy` - Scientific computing
- `scikit-learn` - Machine learning
- `pandas` - Data analysis
- `numba` - JIT compiler

#### Neural Network Components
- `conformer==0.3.2` - Conformer architecture
- `resemble-perth==1.0.1` - Speech processing
- `einops` - Tensor operations

### 3. Build Tools & Compilation
- ✅ Installed Microsoft C++ Build Tools (required for pkuseg)
- ✅ Compiled pkuseg from source with numpy

### 4. Issues Resolved

#### Issue #1: Python 3.14 Incompatibility
**Problem:** `AttributeError: module 'pkgutil' has no attribute 'ImpImporter'`
**Root Cause:** Python 3.14 removed deprecated APIs that old packages still use
**Solution:** Recreated virtual environment with Python 3.11

#### Issue #2: setuptools Missing
**Problem:** `BackendUnavailable: Cannot import 'setuptools.build_meta'`
**Solution:** Installed setuptools and wheel in the virtual environment

#### Issue #3: pkuseg Build Failure
**Problem:** `error: invalid command 'bdist_wheel'` and missing numpy during build
**Solution:** 
1. Installed wheel package
2. Installed numpy first (pkuseg needs it at build time)
3. Used `--no-build-isolation` flag for pkuseg

#### Issue #4: Missing C++ Compiler
**Problem:** `error: Microsoft Visual C++ 14.0 or greater is required`
**Solution:** Installed Microsoft C++ Build Tools with "Desktop development with C++" workload

### 5. Files Created

```
chatterbox-portable-gui/
├── .gitignore              # Excludes .venv, models, cache files
├── README.md               # Complete documentation
├── requirements.txt        # Simplified dependencies (installs everything)
├── requirements-full.txt   # Complete pip freeze output
└── setup.py               # Automated setup script
```

## Git Repository Strategy

### ❌ DO NOT COMMIT TO GIT:
- `.venv/` directory (~2-3 GB) - Virtual environment
- Model files (*.pth, *.pt, *.safetensors)
- Cache files (`__pycache__/`, `.pytest_cache/`)
- Generated audio files
- Log files

### ✅ COMMIT TO GIT:
- `README.md` - Documentation
- `.gitignore` - Git ignore rules
- `requirements.txt` - Dependency list
- `setup.py` - Automated setup script
- Your source code files
- Configuration files

### Why Not Commit .venv?
1. **Size:** Virtual environment is 2-3 GB
2. **Platform-specific:** Contains compiled binaries for Windows
3. **Reproducible:** Can be recreated with `requirements.txt`
4. **Best Practice:** Never commit virtual environments

## One-Command Setup (Like npm install)

### For Fresh Clone:
```powershell
# Clone and setup
git clone https://github.com/JeroTan/chatterbox-portable-gui.git
cd chatterbox-portable-gui
py -3.11 setup.py
```

### The `setup.py` script does:
1. ✅ Checks Python 3.11 is installed
2. ✅ Creates virtual environment
3. ✅ Upgrades pip
4. ✅ Installs all dependencies in correct order
5. ✅ Handles numpy/pkuseg build dependency issue
6. ✅ Generates requirements.txt

## Alternative Manual Setup:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip wheel setuptools
pip install "numpy>=1.24.0,<1.26.0"
pip install --no-build-isolation pkuseg==0.0.25
pip install chatterbox-tts
```

## Team Workflow

### New team member joining:
```powershell
# 1. Clone repo
git clone https://github.com/JeroTan/chatterbox-portable-gui.git
cd chatterbox-portable-gui

# 2. Run automated setup
py -3.11 setup.py

# 3. Activate environment
.venv\Scripts\activate

# 4. Start working!
```

### After pulling updates:
```powershell
# Activate environment
.venv\Scripts\activate

# Update dependencies if requirements.txt changed
pip install -r requirements.txt
```

## Disk Space Requirements
- Virtual environment: ~2-3 GB
- PyTorch: ~2 GB
- Other dependencies: ~500 MB
- **Total: ~3 GB**

## Important Commands

```powershell
# Activate virtual environment
.venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Check installed packages
pip list

# Update all packages (not recommended unless needed)
pip install --upgrade -r requirements.txt

# Verify installation
python -c "import chatterbox_tts; print('Success!')"

# Check Python version
python --version  # Should show 3.11.x
```

## Next Steps

1. **Add your code** - Create your TTS scripts
2. **Test the installation** - Run a simple test
3. **Commit to Git** - Push README, requirements, setup script
4. **Document usage** - Add examples to README.md

## Installation Time & Size Summary

| Component | Size | Time |
|-----------|------|------|
| Virtual environment creation | - | 10 seconds |
| pip, wheel, setuptools | ~5 MB | 10 seconds |
| numpy | ~20 MB | 15 seconds |
| pkuseg (compile from source) | ~50 MB | 1-2 minutes |
| PyTorch + dependencies | ~2 GB | 5-10 minutes |
| chatterbox-tts + remaining | ~500 MB | 2-3 minutes |
| **Total** | **~2.5-3 GB** | **8-15 minutes** |

*Time varies based on internet speed and CPU for compilation*

## Dependencies Overview

Total packages installed: **100+** (including all transitive dependencies)

Major categories:
- Deep learning: PyTorch, transformers
- Audio: librosa, soundfile, torchaudio
- Web: gradio, fastapi
- Scientific: numpy, scipy, scikit-learn
- Utilities: requests, tqdm, pyyaml

All dependencies are pinned to specific versions for reproducibility.
