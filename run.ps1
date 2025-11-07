# Chatterbox TTS - PowerShell Script Runner
# Similar to npm scripts in package.json

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host ""
    Write-Host "Chatterbox TTS - Available Commands:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  .\run.ps1 setup       " -NoNewline -ForegroundColor Green
    Write-Host "- Full setup (creates venv and installs dependencies)"
    Write-Host "  .\run.ps1 install     " -NoNewline -ForegroundColor Green
    Write-Host "- Install/update dependencies"
    Write-Host "  .\run.ps1 test        " -NoNewline -ForegroundColor Green
    Write-Host "- Test if chatterbox-tts is working"
    Write-Host "  .\run.ps1 activate    " -NoNewline -ForegroundColor Green
    Write-Host "- Activate virtual environment (use: & .\run.ps1 activate)"
    Write-Host "  .\run.ps1 clean       " -NoNewline -ForegroundColor Green
    Write-Host "- Remove virtual environment"
    Write-Host "  .\run.ps1 freeze      " -NoNewline -ForegroundColor Green
    Write-Host "- Update requirements-full.txt"
    Write-Host "  .\run.ps1 list        " -NoNewline -ForegroundColor Green
    Write-Host "- List all installed packages"
    Write-Host ""
    Write-Host "To activate environment in current session:" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1"
    Write-Host ""
}

function Invoke-Setup {
    Write-Host "Running full setup..." -ForegroundColor Cyan
    py -3.11 setup.py
}

function Invoke-Install {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
}

function Invoke-Test {
    Write-Host "Testing installation..." -ForegroundColor Cyan
    & .\.venv\Scripts\python.exe -c "import chatterbox_tts; print('✅ Chatterbox TTS is working!')"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "❌ Test failed!" -ForegroundColor Red
    }
}

function Invoke-Activate {
    Write-Host "To activate in current session, run:" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: This script cannot activate the environment for you." -ForegroundColor Yellow
    Write-Host "You must run the activation command directly in your terminal." -ForegroundColor Yellow
}

function Invoke-Clean {
    Write-Host "Cleaning virtual environment..." -ForegroundColor Cyan
    if (Test-Path .venv) {
        Remove-Item -Recurse -Force .venv
        Write-Host "✅ Virtual environment removed." -ForegroundColor Green
    } else {
        Write-Host "⚠️  No virtual environment found." -ForegroundColor Yellow
    }
}

function Invoke-Freeze {
    Write-Host "Updating requirements-full.txt..." -ForegroundColor Cyan
    & .\.venv\Scripts\python.exe -m pip freeze > requirements-full.txt
    Write-Host "✅ requirements-full.txt updated." -ForegroundColor Green
}

function Invoke-List {
    Write-Host "Installed packages:" -ForegroundColor Cyan
    & .\.venv\Scripts\python.exe -m pip list
}

# Main command router
switch ($Command.ToLower()) {
    "setup" { Invoke-Setup }
    "install" { Invoke-Install }
    "test" { Invoke-Test }
    "activate" { Invoke-Activate }
    "clean" { Invoke-Clean }
    "freeze" { Invoke-Freeze }
    "list" { Invoke-List }
    "help" { Show-Help }
    default { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help 
    }
}
