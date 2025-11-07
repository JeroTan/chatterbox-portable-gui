# Quick Start Guide

## 🚀 For New Users (First Time Setup)

### Step 1: Install Prerequisites
1. Install **Python 3.11** from https://www.python.org/downloads/
2. Install **Microsoft C++ Build Tools** from https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Select "Desktop development with C++" workload

### Step 2: Clone Repository
```powershell
git clone https://github.com/JeroTan/chatterbox-pixuus-pixel-adventure.git
cd chatterbox-codebase
```

### Step 3: Automated Setup (Recommended)
```powershell
py -3.11 setup.py
```
This will:
- Create virtual environment
- Install all dependencies (~3 GB, takes 8-15 minutes)
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

---

## 📝 Basic Usage Example

```python
# Create a file: test_tts.py
from chatterbox_tts import ChatterboxTTS

# Your TTS code here
print("Chatterbox TTS is ready!")
```

Run it:
```powershell
python test_tts.py
```

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

- Total installation: ~3 GB
- Make sure you have at least 5 GB free space

---

## ✅ Checklist

- [ ] Python 3.11 installed
- [ ] Microsoft C++ Build Tools installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Installation verified
- [ ] Ready to code! 🎉
