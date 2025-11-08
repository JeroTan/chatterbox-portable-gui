# Building Portable Executable - Quick Guide

## 🚀 Quick Start (Automated)

### Method 1: PowerShell Script (Recommended)
```powershell
# Build portable executable
.\build.ps1

# Clean build (remove previous builds first)
.\build.ps1 -Clean
```

### Method 2: Python Script
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run build script
python build_portable.py
```

---

## 📦 What Gets Built

The build process creates:

```
ChatterboxTTS-Portable/
├── ChatterboxTTS.bat          # Double-click to run
├── README.txt                 # User instructions
├── LICENSE.txt                # GPL v3.0 license
├── app/                       # Application files
│   ├── ChatterboxTTS.exe      # Main executable
│   ├── Python DLLs
│   ├── PyTorch libraries
│   └── All dependencies
├── output/                    # Generated audio (created on first run)
└── projects/                  # Saved projects (created on first run)
```

**Compressed Archive:**
- `ChatterboxTTS-v0.1.4-Portable.zip` (~2-3 GB)

---

## ⏱️ Build Time & Size

- **Build Time:** 10-20 minutes
- **Disk Space Needed:** ~10 GB during build
- **Final Size:** 
  - Uncompressed: ~4-5 GB
  - ZIP: ~2-3 GB
  - 7z: ~1.5-2 GB

---

## 🧪 Testing the Build

```powershell
# Navigate to portable folder
cd ChatterboxTTS-Portable

# Run the application
.\ChatterboxTTS.bat

# Or run executable directly
.\app\ChatterboxTTS.exe
```

**Test Checklist:**
- [ ] App starts without errors
- [ ] Device selector appears
- [ ] Models load successfully
- [ ] GUI displays correctly in dark mode
- [ ] Can generate audio
- [ ] Can save/load projects
- [ ] Audio player works
- [ ] Theme switching works

---

## 📤 Distribution

### Option 1: GitHub Release
1. Go to your repository
2. Click "Releases" → "Create new release"
3. Upload `ChatterboxTTS-v0.1.4-Portable.zip`
4. Add release notes
5. Publish release

### Option 2: Direct File Sharing
Upload to:
- Google Drive
- Dropbox
- OneDrive
- Mega.nz

Share the download link with users.

---

## 🔧 Manual Build (Advanced)

If the automated scripts don't work, you can build manually:

### Step 1: Install PyInstaller
```powershell
pip install pyinstaller
```

### Step 2: Create Spec File
```powershell
pyi-makespec --name ChatterboxTTS --windowed src/main.py
```

### Step 3: Edit Spec File
Add hidden imports and data files (see `build_portable.py` for template)

### Step 4: Build
```powershell
pyinstaller --clean ChatterboxTTS.spec
```

### Step 5: Package
1. Copy `dist/ChatterboxTTS/` folder
2. Rename to `ChatterboxTTS-Portable`
3. Create `ChatterboxTTS.bat` launcher
4. Add README.txt
5. Create ZIP archive

---

## 🐛 Troubleshooting

### Build fails with "module not found"
**Solution:** Add to `hiddenimports` in spec file:
```python
hiddenimports=[
    'missing_module_name',
]
```

### Executable is too large (>5 GB)
**Solution:** Exclude unnecessary packages in spec file:
```python
excludes=[
    'matplotlib',
    'notebook',
    'jupyter',
]
```

### "Access denied" errors during build
**Solution:**
1. Close the app if running
2. Run PowerShell as Administrator
3. Disable antivirus temporarily
4. Try `build.ps1 -Clean`

### Missing DLL errors when running
**Solution:** Run on a clean Windows machine to verify. If DLLs are missing, copy them from your `.venv\Lib\site-packages\` to the app folder.

---

## 🔄 Updating the Build

When you update the code:

1. Make changes to `src/` files
2. Test locally with `python src/main.py`
3. Run `.\build.ps1 -Clean`
4. Test the new build
5. Update version number in:
   - `build_portable.py` (APP_VERSION)
   - README.txt
6. Create new distribution

---

## 📋 Build Customization

### Change App Icon
1. Create/download 256x256 PNG icon
2. Convert to .ico format
3. Save as `icon.ico` in project root
4. Build script will automatically include it

### Change App Name
Edit `build_portable.py`:
```python
APP_NAME = "YourAppName"
```

### Add More Files
Edit spec file's `datas` section:
```python
datas=[
    ('src/assets', 'assets'),
    ('docs/', 'docs/'),
],
```

---

## 🎯 Next Steps After Building

1. ✅ Test on your PC
2. ✅ Test on a clean Windows machine (no Python)
3. ✅ Test on Windows 10 and 11
4. ✅ Get feedback from beta testers
5. ✅ Create GitHub release
6. ✅ Share with users
7. ✅ Monitor for issues
8. ✅ Iterate based on feedback

---

**Built with:** PyInstaller 6.0+
**Target:** Windows 10/11 64-bit
**Python:** 3.11
**License:** GNU GPL v3.0
