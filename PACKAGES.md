# Chatterbox TTS Voice Generator - Package List

This document lists all required packages for the Chatterbox TTS Voice Generator v1.0

## Installation Commands

```powershell
# Production packages (required for running the app)
pip install -r requirements.txt

# Development packages (optional, for building and testing)
pip install -r requirements-dev.txt
```

## Production Packages (~2.5-3 GB)

### Core TTS Engine
| Package | Version | Purpose |
|---------|---------|---------|
| chatterbox-tts | 0.1.4 | Main text-to-speech engine |
| torch | 2.6.0 | PyTorch deep learning framework |
| torchaudio | 2.6.0 | Audio processing for PyTorch |
| transformers | 4.46.3 | Hugging Face transformer models |
| diffusers | 0.29.0 | Diffusion models for generation |
| safetensors | 0.5.3 | Safe tensor serialization |

### Audio Processing
| Package | Version | Purpose |
|---------|---------|---------|
| librosa | 0.11.0 | Audio analysis and feature extraction |
| soundfile | >=0.12.1 | Audio file I/O (WAV, FLAC, etc.) |
| audioread | >=2.1.9 | Audio file reading |
| soxr | >=0.3.2 | High-quality audio resampling |
| pydub | >=0.25.0 | Audio manipulation and export |

### GUI Framework
| Package | Version | Purpose |
|---------|---------|---------|
| gradio | 5.44.1 | Web-based GUI framework |
| fastapi | >=0.115.2 | Web framework backend |
| uvicorn | >=0.14.0 | ASGI web server |
| httpx | >=0.24.1 | Async HTTP client |

### Numerical & Scientific
| Package | Version | Purpose |
|---------|---------|---------|
| numpy | >=1.24.0,<1.26.0 | Array operations and math |
| scipy | >=1.6.0 | Scientific computing |
| scikit-learn | >=1.1.0 | Machine learning utilities |
| numba | >=0.51.0 | JIT compilation for performance |

### NLP & Tokenization
| Package | Version | Purpose |
|---------|---------|---------|
| s3tokenizer | latest | Custom tokenizer |
| pkuseg | 0.0.25 | Chinese word segmentation |
| pykakasi | 2.3.0 | Japanese text processing |

### Neural Network Components
| Package | Version | Purpose |
|---------|---------|---------|
| conformer | 0.3.2 | Conformer architecture |
| resemble-perth | 1.0.1 | Speech processing |
| einops | >=0.6.1 | Tensor operations |

### Utilities
| Package | Version | Purpose |
|---------|---------|---------|
| python-dateutil | >=2.8.0 | Date/time handling |
| tqdm | >=4.27 | Progress bars |
| requests | >=2.28.0 | HTTP requests |
| pyyaml | >=5.0 | YAML configuration |
| packaging | >=23.0 | Version handling |
| filelock | >=3.12.0 | File locking |

**Total Production Packages:** ~100+ (including dependencies)
**Total Size:** ~2.5-3 GB

---

## Development Packages (~200 MB)

### Build Tools
| Package | Version | Purpose |
|---------|---------|---------|
| pyinstaller | >=6.0.0 | Create standalone executables |
| auto-py-to-exe | >=2.40.0 | GUI for PyInstaller |

### Code Quality
| Package | Version | Purpose |
|---------|---------|---------|
| black | >=23.0.0 | Code formatter |
| isort | >=5.12.0 | Import sorter |
| flake8 | >=6.0.0 | Linting |
| pylint | >=3.0.0 | Code analysis |
| mypy | >=1.0.0 | Type checking |

### Testing
| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=7.0.0 | Testing framework |
| pytest-cov | >=4.0.0 | Coverage reporting |
| pytest-mock | >=3.12.0 | Mocking utilities |

### Documentation
| Package | Version | Purpose |
|---------|---------|---------|
| sphinx | >=7.0.0 | Documentation generator |
| sphinx-rtd-theme | >=1.3.0 | ReadTheDocs theme |

### Debugging & Profiling
| Package | Version | Purpose |
|---------|---------|---------|
| ipdb | >=0.13.0 | IPython debugger |
| ipython | >=8.0.0 | Enhanced shell |
| memory-profiler | >=0.61.0 | Memory profiling |
| line-profiler | >=4.0.0 | Line profiling |

### Version Control
| Package | Version | Purpose |
|---------|---------|---------|
| pre-commit | >=3.5.0 | Git hooks for quality |

**Total Development Packages:** ~15-20
**Total Size:** ~200 MB

---

## Built-in Python Modules (No Installation Needed)

The following are used but don't require installation:
- `json` - Save/load project files
- `pathlib` - File path handling
- `datetime` - Timestamp generation
- `os` - File system operations
- `sys` - System operations
- `typing` - Type hints
- `collections` - Data structures

---

## Platform-Specific Notes

### Windows
- **Microsoft Visual C++ Build Tools** required for pkuseg compilation
- All packages have pre-built wheels for Windows x64

### macOS / Linux
- May require additional system libraries for audio processing
- Build tools (gcc/clang) needed for compilation

---

## Version Compatibility

- **Python:** 3.11 (Required - NOT 3.12, 3.13, or 3.14)
- **Windows:** 10 or 11 (64-bit)
- **RAM:** Minimum 8 GB recommended (16 GB for optimal performance)
- **Disk Space:** 5 GB free (3 GB for packages + 2 GB workspace)

---

## Update Strategy

### Updating Packages
```powershell
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade gradio
```

### Checking for Updates
```powershell
# List outdated packages
pip list --outdated

# Show package info
pip show chatterbox-tts
```

### Freezing Current Versions
```powershell
# Generate complete dependency list
pip freeze > requirements-full.txt

# Use run.ps1 script
.\run.ps1 freeze
```

---

## Troubleshooting Package Issues

### Import Errors
```powershell
# Verify package is installed
pip show package-name

# Reinstall package
pip uninstall package-name
pip install package-name
```

### Dependency Conflicts
```powershell
# Check dependency tree
pip install pipdeptree
pipdeptree

# Create fresh environment
.\run.ps1 clean
.\run.ps1 setup
```

### Build Errors
- Ensure Microsoft C++ Build Tools installed
- Update pip: `python -m pip install --upgrade pip`
- Try pre-release: `pip install --pre package-name`

---

**Last Updated:** November 7, 2025
**Version:** 1.0.0
**Document Status:** Production Ready
