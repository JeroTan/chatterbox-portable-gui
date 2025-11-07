# Chatterbox TTS - Pixuu's Pixel Adventure

> 📝 **Note:** This documentation was created with the assistance of **Claude Sonnet** (Anthropic's AI assistant) working through GitHub Copilot in VS Code. Claude helped troubleshoot installation issues, resolve Python compatibility problems, and generate comprehensive documentation to ensure a smooth setup experience.

A Text-to-Speech project using Chatterbox TTS for Pixuu's Pixel Adventure game.

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

- **chatterbox-tts** (0.1.4) - Main TTS engine
- **torch** (2.6.0) - PyTorch for deep learning
- **torchaudio** (2.6.0) - Audio processing
- **transformers** (4.46.3) - Hugging Face transformers
- **gradio** (5.44.1) - Web interface
- **librosa** (0.11.0) - Audio analysis
- And many more dependencies...

Total installation size: ~2-3 GB

## 🔧 Troubleshooting

### Issue: "AttributeError: module 'pkgutil' has no attribute 'ImpImporter'"
**Solution:** You're using Python 3.14. Downgrade to Python 3.11.

### Issue: "error: Microsoft Visual C++ 14.0 or greater is required"
**Solution:** Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Select "Desktop development with C++" workload
- This is needed to compile `pkuseg` dependency

### Issue: "ModuleNotFoundError: No module named 'numpy'"
**Solution:** This was resolved by installing numpy before pkuseg. The requirements.txt handles this automatically.

### Issue: Virtual environment not activating
**Solution:** 
```powershell
# If you see an execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Project Structure

```
chatterbox-codebase/
├── .venv/                  # Virtual environment (DO NOT commit)
├── .git/                   # Git repository
├── .gitignore              # Git ignore file
├── README.md               # This file
├── QUICKSTART.md           # Quick start guide
├── SETUP_SUMMARY.md        # Detailed setup documentation
├── package.json            # Project metadata (like npm package.json)
├── requirements.txt        # Python dependencies (simplified)
├── requirements-full.txt   # Complete pip freeze output
├── setup.py                # Automated setup script
├── run.ps1                 # PowerShell script runner
└── run.bat                 # Batch script runner
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

### For Developers (Current)
```python
# Activate virtual environment
.venv\Scripts\activate

# Run your application
python src/main.py
```

### For End Users (Portable Distribution)
Once the portable version is built:
1. Download `ChatterboxTTS-Portable.zip`
2. Extract to any location
3. Double-click `ChatterboxTTS.bat`
4. Application starts with GUI
5. No Python installation needed

See `PORTABLE_BUILD_GUIDE.md` for building distribution package.

## 📝 Development History

### Setup Process (November 7, 2025)

1. ✅ Created Python 3.11 virtual environment
2. ✅ Resolved setuptools compatibility issues
3. ✅ Installed Microsoft C++ Build Tools for pkuseg compilation
4. ✅ Installed numpy first to resolve pkuseg build dependencies
5. ✅ Successfully installed chatterbox-tts and all dependencies

## 🤝 Contributing

(Add contribution guidelines if this is a team project)

## 📄 License

(Add your license information)

## 🔗 Resources

- [Chatterbox TTS on PyPI](https://pypi.org/project/chatterbox-tts/)
- [Python 3.11 Download](https://www.python.org/downloads/)
- [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
