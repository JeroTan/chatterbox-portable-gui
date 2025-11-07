@echo off
REM Chatterbox TTS - Quick Start Script
REM Similar to npm scripts in package.json

if "%1"=="" goto help
if "%1"=="activate" goto activate
if "%1"=="install" goto install
if "%1"=="setup" goto setup
if "%1"=="test" goto test
if "%1"=="clean" goto clean
goto help

:activate
echo Activating virtual environment...
call .venv\Scripts\activate.bat
goto end

:install
echo Installing dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt
goto end

:setup
echo Running full setup...
py -3.11 setup.py
goto end

:test
echo Testing installation...
.venv\Scripts\python.exe -c "import chatterbox_tts; print('✅ Chatterbox TTS is working!')"
goto end

:clean
echo Cleaning virtual environment...
if exist .venv rmdir /s /q .venv
echo Virtual environment removed.
goto end

:help
echo Chatterbox TTS - Available Commands:
echo.
echo   run.bat setup      - Full setup (creates venv and installs dependencies)
echo   run.bat install    - Install/update dependencies
echo   run.bat test       - Test if chatterbox-tts is working
echo   run.bat clean      - Remove virtual environment
echo.
echo To activate environment manually:
echo   .venv\Scripts\activate
echo.
goto end

:end
