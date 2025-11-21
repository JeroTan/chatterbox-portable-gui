"""
Automated setup script for Chatterbox TTS project
Python 3.11 required

This script automates the entire setup process:
1. Checks Python version
2. Creates virtual environment
3. Installs dependencies
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python 3.11 is being used"""
    version = sys.version_info
    if version.major != 3 or version.minor != 11:
        print(f"❌ Error: Python 3.11 is required, but you're using Python {version.major}.{version.minor}.{version.micro}")
        print("Please install Python 3.11 and run this script with:")
        print("  py -3.11 setup.py")
        return False
    print(f"✅ Python version check passed: {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """Create virtual environment"""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists at .venv")
        response = input("Do you want to recreate it? (y/N): ").strip().lower()
        if response == 'y':
            print("Removing old virtual environment...")
            import shutil
            shutil.rmtree(venv_path)
        else:
            print("Using existing virtual environment")
            return True
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def get_pip_executable():
    """Get the path to pip in the virtual environment"""
    if os.name == 'nt':  # Windows
        return Path(".venv") / "Scripts" / "pip.exe"
    else:  # Unix-like
        return Path(".venv") / "bin" / "pip"


def upgrade_pip():
    """Upgrade pip to latest version"""
    print("Upgrading pip...")
    pip_exe = get_pip_executable()
    try:
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], check=True)
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to upgrade pip: {e}")
        return False


def install_dependencies():
    """Install all dependencies"""
    pip_exe = get_pip_executable()
    
    print("\n" + "="*60)
    print("Installing dependencies...")
    print("This may take several minutes and download ~2-3 GB")
    print("="*60 + "\n")
    
    # First install wheel and setuptools
    print("Step 1/4: Installing build tools...")
    try:
        subprocess.run([str(pip_exe), "install", "wheel", "setuptools"], check=True)
        print("✅ Build tools installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install build tools: {e}")
        return False
    
    # Install numpy first (required for pkuseg)
    print("\nStep 2/4: Installing numpy...")
    try:
        subprocess.run([str(pip_exe), "install", "numpy>=1.24.0,<1.26.0"], check=True)
        print("✅ Numpy installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install numpy: {e}")
        return False
    
    # Install pkuseg without build isolation
    print("\nStep 3/5: Installing pkuseg...")
    try:
        subprocess.run([str(pip_exe), "install", "--no-build-isolation", "pkuseg==0.0.25"], check=True)
        print("✅ Pkuseg installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install pkuseg: {e}")
        print("Make sure you have Microsoft C++ Build Tools installed!")
        return False
    
    # Install PyTorch with CUDA support
    print("\nStep 4/5: Installing PyTorch with CUDA 12.1 support...")
    print("This may take a while (downloading ~2 GB)...")
    try:
        subprocess.run([
            str(pip_exe), "install", 
            "torch", 
            "torchaudio", 
            "--index-url", 
            "https://download.pytorch.org/whl/cu121"
        ], check=True)
        print("✅ PyTorch with CUDA support installed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to install PyTorch with CUDA: {e}")
        print("Falling back to CPU-only PyTorch...")
        try:
            subprocess.run([str(pip_exe), "install", "torch", "torchaudio"], check=True)
            print("✅ PyTorch (CPU-only) installed")
        except subprocess.CalledProcessError as e2:
            print(f"❌ Failed to install PyTorch: {e2}")
            return False
    
    # Install chatterbox-tts and remaining dependencies
    print("\nStep 5/5: Installing chatterbox-tts and remaining dependencies...")
    print("This will download Gradio and other packages...")
    try:
        subprocess.run([
            str(pip_exe), "install", 
            "chatterbox-tts", 
            "pydub", 
            "python-dateutil", 
            "sv-ttk", 
            "pygame", 
            "praat-parselmouth"
        ], check=True)
        print("✅ Chatterbox TTS and all dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install chatterbox-tts: {e}")
        return False
    
    return True


def generate_requirements_txt():
    """Generate requirements.txt from installed packages"""
    print("\nGenerating requirements.txt...")
    pip_exe = get_pip_executable()
    try:
        result = subprocess.run(
            [str(pip_exe), "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        with open("requirements.txt", "w") as f:
            f.write("# Chatterbox TTS Dependencies\n")
            f.write("# Generated automatically\n")
            f.write("# Python 3.11 required\n\n")
            f.write(result.stdout)
        print("✅ requirements.txt generated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to generate requirements.txt: {e}")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("\n1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   .venv\\Scripts\\activate")
    else:  # Unix-like
        print("   source .venv/bin/activate")
    print("\n2. Verify installation:")
    print("   python -c \"import chatterbox_tts; print('Success!')\"")
    print("\n3. Start using Chatterbox TTS!")
    print("\nFor troubleshooting, see README.md")


def main():
    print("="*60)
    print("Chatterbox TTS - Automated Setup")
    print("="*60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Upgrade pip
    upgrade_pip()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed. Please check the errors above.")
        print("Common issues:")
        print("  - Missing Microsoft C++ Build Tools")
        print("  - Wrong Python version (must be 3.11)")
        print("  - Network issues during download")
        sys.exit(1)
    
    # Generate requirements.txt
    generate_requirements_txt()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
