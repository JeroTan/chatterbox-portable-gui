"""
Single-File Executable Build Script for Chatterbox TTS
Creates a standalone chatterbox-gui.exe with everything embedded
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Configuration
APP_NAME = "chatterbox-gui"
APP_VERSION = "0.1.4"
MAIN_SCRIPT = "src/main.py"
ICON_FILE = "src/assets/icon/logo.ico"

# Build directories
BUILD_DIR = Path("build")

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller found")
        return True
    except ImportError:
        print("❌ PyInstaller not found")
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
        return True

def clean_build():
    """Clean previous build artifacts"""
    print("\n🧹 Cleaning previous builds...")
    
    # Clean build directory
    if BUILD_DIR.exists():
        try:
            shutil.rmtree(BUILD_DIR)
            print(f"   Removed {BUILD_DIR}")
        except PermissionError:
            print(f"   ⚠️ Could not remove {BUILD_DIR} (file in use)")
            print(f"   💡 Tip: Close chatterbox-gui.exe if running")
            # Try to continue anyway
    
    # Clean PyInstaller generated folders in root
    for directory in [Path("dist"), Path("__pycache__")]:
        if directory.exists():
            try:
                shutil.rmtree(directory)
                print(f"   Removed {directory}")
            except PermissionError:
                print(f"   ⚠️ Could not remove {directory} (file in use)")
    
    # Remove .spec file
    spec_file = Path(f"{APP_NAME}.spec")
    if spec_file.exists():
        try:
            spec_file.unlink()
            print(f"   Removed {spec_file}")
        except PermissionError:
            print(f"   ⚠️ Could not remove {spec_file} (file in use)")
    
    print("✅ Clean complete")

def create_spec_file():
    """Create PyInstaller spec file for single-file executable"""
    print("\n📝 Creating spec file for single-file executable...")
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{MAIN_SCRIPT}'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/assets/reference_voices', 'assets/reference_voices'),  # Voice samples
        ('src/assets/downloads', 'assets/downloads'),  # TTS model cache folder
        ('src/assets/icon', 'assets/icon'),  # Application icons
        # Bundle perth pretrained checkpoint files
        (r'.venv/Lib/site-packages/perth/perth_net/pretrained', 'perth/perth_net/pretrained'),
        # Bundle pkuseg dictionary files for multilingual TTS
        (r'.venv/Lib/site-packages/pkuseg/dicts', 'pkuseg/dicts'),
        (r'.venv/Lib/site-packages/pkuseg/models', 'pkuseg/models'),
        (r'.venv/Lib/site-packages/pkuseg/postag', 'pkuseg/postag'),
    ],
    hiddenimports=[
        'chatterbox',
        'chatterbox.tts',
        'chatterbox.mtl_tts',
        'torch',
        'torchaudio',
        'transformers',
        'diffusers',
        'tkinter',
        'tkinter.ttk',
        'sv_ttk',
        'pygame',
        'pygame.mixer',
        'parselmouth',
        'librosa',
        'soundfile',
        'numpy',
        'scipy',
        'requests',
        'PIL',
        'PIL.Image',
        'pydub',
        'accelerate',
        'safetensors',
        'huggingface_hub',
        'tokenizers',
        'regex',
        'sentencepiece',
        'pkuseg',
        'pkuseg.feature_extractor',
        'pkuseg.inference',
        'perth',
        'perth.perth_net',
        'perth.perth_net.perth_net_implicit',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'IPython',
        'notebook',
        'jupyter',
        'pytest',
        'sphinx',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console window for debugging logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{ICON_FILE}',  # Set .exe icon
)
"""
    
    spec_file = Path(f"{APP_NAME}.spec")
    with open(spec_file, 'w') as f:
        f.write(spec_content)
    
    print(f"✅ Created {spec_file}")
    return spec_file

def build_executable(spec_file):
    """Build the single-file executable using PyInstaller"""
    print("\n🔨 Building single-file executable...")
    print("   This may take 15-25 minutes...")
    print("   Embedding all dependencies into chatterbox-gui.exe...\n")
    
    # Create build directory
    BUILD_DIR.mkdir(exist_ok=True)
    
    try:
        # Build single-file executable directly to build folder
        subprocess.run(
            [
                "pyinstaller",
                "--clean",
                "--distpath", str(BUILD_DIR),
                "--workpath", str(BUILD_DIR / "work"),
                str(spec_file)
            ],
            check=True
        )
        print("\n✅ Build complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False

def main():
    """Main build process"""
    print("=" * 70)
    print(f"  Chatterbox TTS - Single-File Executable Builder")
    print(f"  Version: {APP_VERSION}")
    print("=" * 70)
    
    # Check requirements
    if not Path(MAIN_SCRIPT).exists():
        print(f"❌ Main script not found: {MAIN_SCRIPT}")
        return 1
    
    # Step 1: Check PyInstaller
    if not check_pyinstaller():
        return 1
    
    # Step 2: Clean previous builds
    clean_build()
    
    # Step 3: Create spec file
    spec_file = create_spec_file()
    
    # Step 4: Build executable
    if not build_executable(spec_file):
        return 1
    
    # Get exe size
    exe_path = BUILD_DIR / f"{APP_NAME}.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        size_gb = size_mb / 1024
        
        print("\n" + "=" * 70)
        print("🎉 BUILD SUCCESSFUL!")
        print("=" * 70)
        print(f"\n✅ Executable: {exe_path.absolute()}")
        print(f"📦 Size: {size_mb:.1f} MB ({size_gb:.2f} GB)")
        print(f"\n🚀 To run: .\\build\\{APP_NAME}.exe")
        print(f"📤 To distribute: Share the {APP_NAME}.exe file")
        print(f"\n💡 NOTE:")
        print(f"   - This is a single standalone .exe file")
        print(f"   - Contains all dependencies embedded")
        print(f"   - No installation required")
        print(f"   - First run will download AI models (~2-3 GB)")
        print(f"   - Generated audio will be saved to output/ folder")
        print("=" * 70)
    else:
        print(f"\n❌ Executable not found: {exe_path}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
