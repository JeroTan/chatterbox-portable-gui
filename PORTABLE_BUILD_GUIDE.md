# Creating Portable Chatterbox TTS Distribution

> ✅ **OFFICIAL DISTRIBUTION METHOD** - This is the chosen approach for distributing Chatterbox TTS to end users.

A step-by-step guide to create a portable Windows application that users can run without installing Python.

---

## 🎯 Goal

Create a folder that users can:
- ✅ Download and extract
- ✅ Double-click to run
- ✅ No Python installation needed
- ✅ No setup required
- ✅ Copy to any Windows PC

---

## 📋 Prerequisites

- Windows 10/11
- Working Chatterbox TTS installation (you have this!)
- Internet connection (for downloading embedded Python)
- ~5 GB free disk space

---

## 🔧 Method 1: Portable Folder ⭐ (OFFICIAL METHOD)

### Step 1: Create Distribution Folder

```powershell
# Create main folder
New-Item -ItemType Directory -Path "ChatterboxTTS-Portable"
cd ChatterboxTTS-Portable

# Create subfolders
New-Item -ItemType Directory -Path "app", "outputs", "projects", "reference_audio"
```

### Step 2: Download Python Embeddable Package

1. Go to https://www.python.org/downloads/windows/
2. Find **Python 3.11** (latest 3.11.x version)
3. Download **Windows embeddable package (64-bit)**
   - File name: `python-3.11.x-embed-amd64.zip`
4. Extract to `./python311/`

### Step 3: Enable pip in Embedded Python

```powershell
cd ChatterboxTTS-Portable

# Download get-pip.py
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"

# Uncomment site-packages in python311._pth
# Edit: ./python311/python311._pth
# Uncomment the line: import site

# Install pip
.\python311\python.exe get-pip.py

# Clean up
Remove-Item get-pip.py
```

**Or manually edit `./python311/python311._pth`:**
```
python311.zip
.

# Uncomment to run site.main() automatically
import site  ← Remove the # if present
```

### Step 4: Install Dependencies

```powershell
# Install all dependencies
.\python311\python.exe -m pip install chatterbox-tts gradio

# This will take 10-15 minutes and download ~2.5 GB
```

### Step 5: Copy Your Application

```powershell
# Copy your GUI code
Copy-Item -Path "..\src\main.py" -Destination ".\app\main.py"

# Copy any other necessary files
Copy-Item -Path "..\*.md" -Destination "."
```

### Step 6: Create Launcher

**Create `ChatterboxTTS.bat`:**

```batch
@echo off
title Chatterbox TTS - Voice Generator
cls
echo ============================================
echo   Chatterbox TTS - Voice Generator
echo ============================================
echo.
echo Starting application...
echo.
cd /d "%~dp0"
start "" python311\python.exe app\main.py
exit
```

Save this as `./ChatterboxTTS.bat`

### Step 7: Create README for Users

**Create `USER_README.txt`:**

```text
===============================================
  Chatterbox TTS - Portable Edition
===============================================

Thank you for downloading Chatterbox TTS!

QUICK START:
1. Double-click "ChatterboxTTS.bat" to start
2. Enter text in the text box
3. Press Enter or click Generate
4. Preview and export your audio!

REQUIREMENTS:
- Windows 10 or 11 (64-bit)
- ~5 GB disk space
- Internet connection (for first-time model downloads)

PORTABLE NOTES:
- This is a fully portable application
- No installation required
- Can be copied to USB drive
- All settings saved in "projects" folder

FOLDERS:
- outputs/         Generated audio files
- projects/        Saved project files
- reference_audio/ Custom voice samples
- logs/           Application logs

TROUBLESHOOTING:
- If nothing happens, check logs/ folder
- Make sure your antivirus isn't blocking it
- Try "Run as Administrator" if issues persist

VERSION: 1.0.0
CREATED: November 2025

For support: [Your contact/GitHub link]
===============================================
```

### Step 8: Test the Portable Version

```powershell
# Navigate to the portable folder
cd ChatterboxTTS-Portable

# Double-click ChatterboxTTS.bat
# OR run from terminal:
.\ChatterboxTTS.bat
```

### Step 9: Create Distribution Package

```powershell
# Compress for distribution
Compress-Archive -Path "ChatterboxTTS-Portable" -DestinationPath "ChatterboxTTS-v1.0-Portable.zip"

# Or use 7-Zip for better compression:
# 7z a -t7z -mx=9 ChatterboxTTS-v1.0-Portable.7z ChatterboxTTS-Portable
```

---

## 🚀 Method 2: Single .exe with PyInstaller (Alternative - Not Used)

### Prerequisites

```powershell
pip install pyinstaller
```

### Create .exe

```powershell
# Navigate to your project
cd path\to\chatterbox-portable-gui

# Activate virtual environment
.venv\Scripts\activate

# Basic .exe
pyinstaller --onefile src/main.py --name ChatterboxTTS

# With window (no console)
pyinstaller --onefile --windowed src/main.py --name ChatterboxTTS

# With icon
pyinstaller --onefile --windowed --icon=resources/icon.ico src/main.py --name ChatterboxTTS

# With hidden imports (if needed)
pyinstaller --onefile --windowed --hidden-import=chatterbox_tts src/main.py --name ChatterboxTTS
```

### Result

- `.exe` file created in `./dist/` folder
- **Size: 3-5 GB** (includes everything)
- Single file to distribute
- Slower first startup (unpacking)

---

## 📦 Final Folder Structure

```
ChatterboxTTS-Portable/
├── ChatterboxTTS.bat           ← Double-click to run
├── USER_README.txt             ← Instructions
├── LICENSE.txt                 ← Your license
├── CHANGELOG.txt               ← Version history
│
├── python311/                  ← Embedded Python (~50 MB)
│   ├── python.exe
│   ├── python311.dll
│   ├── python311.zip
│   ├── Scripts/
│   └── Lib/
│       └── site-packages/      ← All dependencies (~2.5 GB)
│
├── app/
│   └── main.py                 ← Your GUI application
│
├── outputs/                    ← Generated audio files
├── projects/                   ← Saved project files
├── reference_audio/            ← Custom voice samples
└── logs/                       ← Application logs
```

---

## 📊 Size Breakdown

```
Python Embeddable:              50 MB
PyTorch:                      2000 MB
Transformers + Models:         600 MB
Gradio + Dependencies:         150 MB
Other packages:                200 MB
Your Application:                5 MB
════════════════════════════════════
Total:                      ~3.0 GB

Compressed (ZIP):           ~2.2 GB
Compressed (7z):            ~1.8 GB
```

---

## 🎨 Optional: Create Icon

1. **Create or download icon** (256x256 PNG)
2. **Convert to .ico:**
   - Use online converter: https://convertio.co/png-ico/
   - Or use Python: `pip install Pillow`

```python
from PIL import Image
img = Image.open('icon.png')
img.save('icon.ico', sizes=[(256,256)])
```

3. **Use with PyInstaller:**
```powershell
pyinstaller --icon=icon.ico --onefile --windowed src/main.py
```

---

## 🔒 Code Signing (Optional)

To prevent antivirus warnings:

1. **Get Code Signing Certificate**
   - Purchase from CA (Sectigo, DigiCert)
   - Cost: ~$200-500/year

2. **Sign the .exe:**
```powershell
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com ChatterboxTTS.exe
```

---

## 🌐 Distribution Methods

### Option 1: GitHub Releases
```powershell
# Create release on GitHub
# Upload ChatterboxTTS-v1.0-Portable.zip
# Users download from Releases page
```

### Option 2: Google Drive / Dropbox
```
1. Upload ZIP to cloud storage
2. Create shareable link
3. Share with users
```

### Option 3: Installer (Advanced)

**Using Inno Setup:**

1. Download Inno Setup: https://jrsoftware.org/isinfo.php
2. Create setup script (`.iss` file)
3. Compile to installer
4. Professional installation experience

---

## ✅ Testing Checklist

Before distributing:

- [ ] Test on clean Windows 10 machine
- [ ] Test on clean Windows 11 machine
- [ ] Test without Python installed
- [ ] Test without internet (after first run)
- [ ] Test all features work
- [ ] Test file paths work correctly
- [ ] Check file size is acceptable
- [ ] Verify no absolute paths in code
- [ ] Test on different drive letters (C:, D:, E:)
- [ ] Test from USB drive
- [ ] Check antivirus doesn't flag it
- [ ] Verify README is clear

---

## 🐛 Common Issues & Solutions

### Issue: "Python not found"
**Solution:** Make sure `./python311/` folder exists and contains `python.exe`

### Issue: "Module not found"
**Solution:** Reinstall packages in embedded Python

### Issue: "Permission denied"
**Solution:** Run as administrator or change folder permissions

### Issue: Very slow startup
**Solution:** Normal for first run (PyTorch initialization)

### Issue: Antivirus blocks it
**Solution:** 
- Add to antivirus exclusions
- Consider code signing
- Use portable folder instead of .exe

---

## 📝 Update Process

When you update your app:

1. Modify `./app/main.py`
2. Update version in README
3. Test changes
4. Repackage and redistribute

Users can:
- Replace only `./app/main.py` (quick update)
- Or download full new package

---

## 💡 Pro Tips

1. **Keep dependencies minimal** - Less size, faster startup
2. **Test on different PCs** - Don't assume all systems are the same
3. **Include good README** - Reduce support requests
4. **Version your releases** - Users know what they have
5. **Changelog is helpful** - Users see what's new
6. **Consider auto-update** - Check for new versions on startup

---

## 🎯 Next Steps

1. ✅ Build portable version using Method 1
2. ✅ Test on another PC
3. ✅ Create GitHub release
4. ✅ Share with team/users
5. ✅ Gather feedback
6. ✅ Iterate and improve

---

**Last Updated:** November 7, 2025
**Guide Version:** 1.0
**Created by:** Claude Sonnet via GitHub Copilot
