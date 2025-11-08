# Chatterbox TTS - Quick Build Script
# Creates a single chatterbox-gui.exe file

param(
    [switch]$Clean
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Chatterbox TTS - Executable Builder" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

if ($Clean) {
    Write-Host "[*] Cleaning previous builds..." -ForegroundColor Yellow
    Remove-Item -Path "build", "dist", "*.spec" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "[+] Clean complete" -ForegroundColor Green
    Write-Host ""
}

# Check if PyInstaller is installed
Write-Host "[*] Checking PyInstaller..." -ForegroundColor Yellow
python -c "import PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[*] Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}
Write-Host "[+] PyInstaller ready" -ForegroundColor Green
Write-Host ""

# Run build script
Write-Host "[*] Building executable..." -ForegroundColor Yellow
Write-Host "    This will take 15-25 minutes..." -ForegroundColor Gray
Write-Host ""
python build_portable.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  [+] BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable: .\build\chatterbox-gui.exe" -ForegroundColor Cyan
    Write-Host "Run it: .\build\chatterbox-gui.exe" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[-] BUILD FAILED" -ForegroundColor Red
    Write-Host "Check the output above for errors" -ForegroundColor Red
    Write-Host ""
    exit 1
}

