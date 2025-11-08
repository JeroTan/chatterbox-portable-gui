# Chatterbox TTS GUI - Application Requirements

## 📋 Project Overview

A user-friendly graphical interface for Chatterbox TTS that allows users to generate high-quality voice audio from text input with advanced customization options.

---

## 🎯 Target Users

- Users familiar with web/JavaScript interfaces
- Content creators needing voice generation
- Game developers (Pixuu's Pixel Adventure)
- Users who prefer GUI over command-line tools

---

## 🖥️ Main Interface Components

### 1. **Text Input Area**
**Component:** Multi-line text box

**Features:**
- Large, prominent text area for input
- Support for multi-line text entry
- Keyboard shortcuts:
  - `Enter` → Trigger audio generation
  - `Shift + Enter` → Create new line (skip generation)
- Auto-disable during audio generation
- Re-enable after generation completes
- Clear placeholder text: "Enter text to convert to speech..."

**Behavior:**
```
User Types Text
    ↓
Press Enter → Generate Audio
    OR
Press Shift+Enter → New Line (continue typing)
    ↓
Textbox disabled during generation
    ↓
Generation complete → Textbox re-enabled
```

---

### 2. **Control Buttons**

#### **Primary Buttons (Always Visible)**

1. **Generate Button**
   - Primary action button
   - Triggers voice generation
   - Disabled when textbox is empty
   - Shows loading state during generation
   - Label: "Generate Voice"

2. **Set Output Folder Button**
   - Opens folder picker dialog
   - Displays current output path
   - Default: `./outputs/` in project directory
   - Label: "Set Output Folder"

3. **Export Audio Button**
   - Saves generated audio to output folder
   - Only enabled after successful generation
   - Shows success/error notification
   - Label: "Export Audio"

4. **Save Project Button**
   - Saves current session/project
   - Includes: text, settings, parameters, generated audio reference
   - Keyboard shortcut: `Ctrl + S`
   - Saves to custom file format (`.cbx` or `.json`)
   - Label: "💾 Save Project"

5. **Load Project Button**
   - Opens file picker to load saved project
   - Restores: text, voice settings, parameters
   - Keyboard shortcut: `Ctrl + O`
   - Label: "📂 Load Project"

---

### 3. **Audio Preview Section**

**Component:** Audio player widget

**Features:**
- Embedded audio player
- Play/Pause controls
- Volume control
- Playback progress bar
- Duration display
- Only visible after generation
- "Preview before export" functionality

**Layout:**
```
[========== Audio Player ==========]
[▶️ Play] [⏸️ Pause] [🔊 Volume] [0:00 / 0:05]
[==================Progress Bar==================]
```

---

### 4. **Output Path Display**

**Component:** Read-only text field with folder icon

**Features:**
- Shows current output directory
- Click to open folder in file explorer
- Truncates long paths with "..."
- Default: `./outputs/`

**Example:**
```
📁 Output: C:\Projects\chatterbox-codebase\outputs\
```

---

## 🔧 Advanced Mode

### **Collapsible Section (Dropdown/Accordion)**

**Toggle Button:** "⚙️ Advanced Settings" 

When expanded, shows:

---

### Advanced Feature 1: **Voice Selection**

**Component:** Searchable dropdown with two modes

#### **Mode A: Pre-defined Voices**
- Dropdown list of Chatterbox's built-in voices
- Search/filter functionality
- Voice categories (if available):
  - Male voices
  - Female voices
  - Character voices
  - Language-specific voices
- Preview sample for each voice (if possible)

**UI Design:**
```
┌─────────────────────────────────────┐
│ 🔍 Search voices...                 │
├─────────────────────────────────────┤
│ ✓ Default Voice (Female, Neutral)   │
│   Professional Male                  │
│   Energetic Female                   │
│   Character - Deep                   │
│   ... (scrollable list)              │
└─────────────────────────────────────┘
```

#### **Mode B: Reference Audio**
- Tab/button to switch to "Custom Voice"
- File picker to import audio file
- Supported formats: WAV, MP3, FLAC
- Display selected file name
- Clear/Remove button

**UI Design:**
```
[Pre-defined Voices] [Custom Voice] ← Tabs

When "Custom Voice" selected:
┌─────────────────────────────────────┐
│ 📁 Import Reference Audio           │
│                                      │
│ Selected: voice_sample.wav     [❌] │
└─────────────────────────────────────┘
```

---

### Advanced Feature 2: **Expression & Emotion Control**

**Two Approaches (Based on Chatterbox Capabilities):**

#### **Approach A: Text Description (Preferred if supported)**
**Component:** Text input field

**Purpose:** Describe the desired tone, emotion, and expression

**Features:**
- Multi-line text box
- Character counter
- Helpful placeholder examples

**Example UI:**
```
┌─────────────────────────────────────────────────┐
│ Expression & Tone Description                    │
├─────────────────────────────────────────────────┤
│ Describe how the voice should sound:             │
│                                                   │
│ [Text box with placeholder:]                     │
│ "Excited and energetic, like announcing          │
│  a victory. Upbeat tone with emphasis."          │
│                                                   │
│ Examples: happy, sad, angry, calm, excited,      │
│ professional, friendly, mysterious               │
└─────────────────────────────────────────────────┘
```

#### **Approach B: Parameter Controls (If text description not supported)**
**Components:** Sliders and dropdowns

**Parameters:**
1. **Emotion Selector**
   - Dropdown: Neutral, Happy, Sad, Angry, Excited, Calm, Fearful
   
2. **Energy Level**
   - Slider: Low (0) ←→ High (100)
   
3. **Speaking Speed**
   - Slider: Slow (0.5x) ←→ Fast (2.0x)
   
4. **Pitch**
   - Slider: Low (-12) ←→ High (+12)

5. **Emphasis/Intensity**
   - Slider: Subtle (0) ←→ Strong (100)

**Example UI:**
```
┌──────────────────────────────────────┐
│ Emotion: [Dropdown: Neutral ▼]       │
│                                      │
│ Energy:    [====●====----------] 50% │
│ Speed:     [========●----------] 1.0x│
│ Pitch:     [----------●--------] 0   │
│ Emphasis:  [------●------------] 30% │
└──────────────────────────────────────┘
```

---

## 🎨 UI/UX Design Guidelines

### Layout Structure

```
┌──────────────────────────────────────────────────────┐
│  Chatterbox TTS - Voice Generator                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────────────────────────────────────┐     │
│  │ Enter text to convert to speech...          │     │
│  │                                             │     │
│  │ [Text Input Area - Multi-line]              │     │
│  │                                             │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  [🎤 Generate Voice]  [📁 Set Output Folder]         │
│                                                       │
│  📁 Output: C:\...\outputs\                          │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ 🔊 Audio Preview                             │    │
│  │ [▶️] [⏸️] [🔊] [============●====] 0:03/0:05  │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  [💾 Export Audio]                                   │
│                                                       │
│  ▼ ⚙️ Advanced Settings                             │
│  ┌─────────────────────────────────────────────┐    │
│  │ Voice Selection:                             │    │
│  │ [Pre-defined ●] [Custom Audio ○]            │    │
│  │ 🔍 [Search voices...]                        │    │
│  │                                              │    │
│  │ Expression & Tone:                           │    │
│  │ [Text description box or parameter sliders] │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
└──────────────────────────────────────────────────────┘
```

### Design Principles

1. **Simplicity First**
   - Basic features prominently displayed
   - Advanced features hidden by default
   - Clean, uncluttered interface

2. **Visual Feedback**
   - Loading indicators during generation
   - Success/error notifications
   - Disabled states clearly visible
   - Auto-save indicator (saved/unsaved changes)

3. **Keyboard Friendly**
   - `Enter` - Generate audio
   - `Shift+Enter` - New line in text
   - `Ctrl+S` - Save project
   - `Ctrl+O` - Open/Load project
   - `Tab` - Navigate between fields
   - `Escape` - Cancel operations

4. **Responsive States**
   - Generating: Show progress/spinner
   - Success: Enable preview and export
   - Error: Show error message with details
   - Modified: Show unsaved changes indicator (*)

---

## 🔄 User Workflow

### **Basic Workflow (Simple Mode)**
```
1. User opens app
   ↓
2. Types text in input box
   ↓
3. Presses Enter (or clicks Generate)
   ↓
4. Textbox disables, loading indicator shows
   ↓
5. Audio generates
   ↓
6. Preview player appears with audio
   ↓
7. User plays audio to preview
   ↓
8. User clicks "Export Audio"
   ↓
9. File saved to output folder
   ↓
10. Success notification shown
```

### **Advanced Workflow**
```
1-2. [Same as basic]
   ↓
3. User expands "Advanced Settings"
   ↓
4. Selects voice from dropdown OR imports custom audio
   ↓
5. (Optional) Adds expression/emotion description
   ↓
6. Presses Enter or clicks Generate
   ↓
7-10. [Same as basic workflow]
```

---

## 📁 File Organization

### Output Files Naming Convention
```
Format: {timestamp}_{first_5_words}.wav

Examples:
- 20251107_143052_hello_world_this_is.wav
- 20251107_150312_welcome_to_the_adventure.wav
```

### Project Files Format

**File Extension:** `.cbx` (ChatterBox project) or `.json`

**File Contents (JSON structure):**
```json
{
  "version": "1.0",
  "created": "2025-11-07T14:30:52Z",
  "modified": "2025-11-07T15:45:12Z",
  "text": "The text that was entered for generation",
  "output_folder": "C:\\path\\to\\outputs",
  "voice": {
    "mode": "predefined",  // or "custom"
    "selected_voice": "Professional Female",
    "custom_audio_path": null  // or path if custom mode
  },
  "expression": {
    "mode": "text",  // or "parameters"
    "description": "Excited and energetic tone",
    "parameters": {
      "emotion": "happy",
      "energy": 75,
      "speed": 1.2,
      "pitch": 0,
      "emphasis": 60
    }
  },
  "generated_audio": {
    "path": "outputs/20251107_143052_hello_world.wav",
    "duration": 5.3,
    "sample_rate": 22050
  }
}
```

### Folder Structure
```
chatterbox-codebase/
├── outputs/              ← Generated audio files
│   ├── 20251107_143052_hello_world.wav
│   └── 20251107_150312_welcome_to.wav
├── projects/             ← Saved project files (NEW)
│   ├── my_voice_project.cbx
│   ├── game_dialogue_001.cbx
│   └── character_intro.cbx
├── reference_audio/      ← User's custom voice samples
│   └── my_voice.wav
└── src/
    └── main.py          ← GUI application
```

---

## ⚙️ Technical Requirements

### Framework Suggestions
- **Gradio** (Recommended) - Web-based, easy to use, Python-friendly
- **Tkinter** - Native Python GUI (desktop app)
- **PyQt5/PySide6** - Advanced desktop app
- **Streamlit** - Quick web interface

### Deployment Options

#### Option 1: Portable .exe (Standalone Application)

**Yes, it's possible!** Python apps can be packaged as `.exe` files using:

**PyInstaller** (Recommended)
```powershell
# Install PyInstaller
pip install pyinstaller

# Create standalone .exe (includes all dependencies)
pyinstaller --onefile --windowed --name "ChatterboxTTS" src/main.py

# With icon
pyinstaller --onefile --windowed --icon=app.ico --name "ChatterboxTTS" src/main.py
```

**Pros:**
- ✅ Double-click to run (no Python installation needed)
- ✅ Portable - can copy to any Windows PC
- ✅ All packages bundled inside
- ✅ Professional feel

**Cons:**
- ❌ Large file size (~3-5 GB due to PyTorch)
- ❌ Slower first startup (unpacking)
- ❌ Antivirus may flag it (false positive)

---

**Alternative Tools:**

1. **py2exe** - Windows-specific packager
2. **cx_Freeze** - Cross-platform packager
3. **Nuitka** - Compiles to C++ (faster, smaller)
4. **PyOxidizer** - Rust-based packager

---

#### Option 2: Portable Folder (Recommended for Large Apps)

**Better for this project due to size:**

Create a portable folder structure:
```
ChatterboxTTS-Portable/
├── ChatterboxTTS.exe          ← Launcher script
├── python311/                  ← Embedded Python
│   ├── python.exe
│   └── Lib/                   ← All packages
├── app/
│   └── main.py                ← Your GUI
├── outputs/                    ← Generated audio
├── projects/                   ← Saved projects
└── README.txt                 ← Usage instructions
```

**Setup Steps:**

1. **Download Python Embeddable Package**
   - Get from python.org (Python 3.11 embeddable)
   - Extract to `python311/` folder

2. **Install Dependencies**
   ```powershell
   .\python311\python.exe -m pip install chatterbox-tts gradio
   ```

3. **Create Launcher** (`ChatterboxTTS.exe` or `.bat`)
   ```batch
   @echo off
   cd /d "%~dp0"
   start python311\python.exe app\main.py
   ```

**Pros:**
- ✅ Portable (copy entire folder)
- ✅ No installation needed
- ✅ Faster startup
- ✅ Easy to update (replace files)
- ✅ Can inspect/modify if needed

**Cons:**
- ❌ Folder is ~3 GB
- ❌ User sees folder structure

---

#### Option 3: Installer Package

**Use Inno Setup or NSIS:**

Creates proper installer like commercial software:
- Start menu shortcuts
- Desktop icon
- Uninstaller
- Registry entries
- File associations (.cbx opens in app)

**Best for:** Distribution to end-users

---

### ✅ Recommended Approach for This Project (CHOSEN)

**For Development/Team:** Virtual environment (current setup)

**For Distribution:** Portable Folder + Launcher ⭐ **SELECTED**

**Why Portable Folder:**
1. PyTorch models are huge (~2-3 GB)
2. Single .exe would be 4-5 GB and slower startup
3. Portable folder is more practical (~3 GB)
4. Easier to debug and update
5. Users can see what's inside if curious
6. Less likely to trigger antivirus false positives
7. Faster startup after first run

**Distribution Package:**
```
ChatterboxTTS-Portable.zip (~2.2 GB compressed)
  └── ChatterboxTTS-Portable/
      ├── ChatterboxTTS.bat  ← Double-click to run
      ├── python311/         ← Embedded Python + packages
      ├── app/              ← Your GUI application
      ├── outputs/          ← Generated audio
      └── projects/         ← Saved projects
```

**User Experience:**
1. Download and extract ZIP
2. Double-click `ChatterboxTTS.bat`
3. Application starts
4. No installation required

---

### Creating Portable Distribution

**Step-by-step Guide:**

```powershell
# 1. Create distribution folder
New-Item -ItemType Directory -Path "ChatterboxTTS-Portable"

# 2. Download Python 3.11 embeddable
# https://www.python.org/downloads/windows/
# Extract to ChatterboxTTS-Portable/python311/

# 3. Install get-pip in embedded Python
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
.\ChatterboxTTS-Portable\python311\python.exe get-pip.py

# 4. Install dependencies
.\ChatterboxTTS-Portable\python311\python.exe -m pip install chatterbox-tts gradio

# 5. Copy your app
Copy-Item -Recurse src/* ChatterboxTTS-Portable/app/

# 6. Create launcher.bat
@"
@echo off
cd /d "%~dp0"
start python311\python.exe app\main.py
"@ | Out-File -Encoding ASCII ChatterboxTTS-Portable\ChatterboxTTS.bat

# 7. Create README.txt with instructions

# 8. Zip and distribute
Compress-Archive -Path ChatterboxTTS-Portable -DestinationPath ChatterboxTTS-v1.0-Portable.zip
```

---

### Package Structure Examples

**Minimal Portable Package:**
```
ChatterboxTTS/
├── run.bat                     ← Double-click to start
├── python/                     ← Embedded Python (~50 MB)
├── Lib/                        ← Dependencies (~2.5 GB)
│   └── site-packages/
├── app/
│   └── main.py
├── outputs/
├── projects/
└── README.txt
```

**Professional Package:**
```
ChatterboxTTS/
├── ChatterboxTTS.exe           ← Beautiful launcher
├── python/
├── app/
├── resources/
│   ├── icon.ico
│   └── logo.png
├── outputs/
├── projects/
├── logs/
├── README.txt
├── LICENSE.txt
└── CHANGELOG.txt
```

---

### Creating a Windows Launcher Executable

**Option A: Batch File (Simple)**
```batch
@echo off
title Chatterbox TTS
echo Starting Chatterbox TTS...
cd /d "%~dp0"
python\python.exe app\main.py
pause
```

**Option B: VBS Launcher (No Console Window)**
```vbscript
Set objShell = CreateObject("WScript.Shell")
objShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
objShell.Run "python\python.exe app\main.py", 0, False
```

**Option C: C# Launcher (Professional)**
- Create small C# app that launches Python
- Can add splash screen, checking dependencies, etc.
- Compile to `ChatterboxTTS.exe`

**Option D: AutoIt Script**
- Create GUI wrapper
- Compile to .exe
- Looks professional

---

### File Size Considerations

**Component Sizes (Approximate):**
```
Python Embeddable:        50 MB
PyTorch:                2000 MB
Transformers:            500 MB
Gradio + dependencies:   100 MB
Other packages:          350 MB
Your code:                 1 MB
--------------------------------
Total:                 ~3 GB
```

**Optimization Tips:**
1. Remove unnecessary packages
2. Use PyTorch CPU-only version (smaller)
3. Don't include development dependencies
4. Compress with 7-Zip (better than ZIP)

---

### Distribution Methods

**For End Users:**
1. **Portable ZIP** - Download and extract
2. **Installer** - Professional installation
3. **Cloud Link** - Google Drive, Dropbox
4. **GitHub Releases** - Version tracking

**For Developers:**
1. **Git Repository** - Clone and run setup.py
2. **Docker Container** - Consistent environment
3. **Requirements.txt** - Virtual environment

---

### Must-Have Features
✅ Multi-line text input with keyboard shortcuts
✅ Output folder selection
✅ Audio preview before export
✅ Voice selection (pre-defined + custom)
✅ Expression/emotion control
✅ Loading states and error handling
✅ File export functionality

### Nice-to-Have Features
- ✅ **Save/Load project files** (text + settings + parameters)
- ✅ **Recent projects menu** for quick access
- Auto-save with crash recovery
- Batch processing (multiple texts)
- Voice presets/templates library
- Audio format selection (WAV, MP3, FLAC)
- Audio editing (trim, fade in/out)
- History of generated audio
- Copy text from clipboard button
- Project export/import for sharing
- Cloud sync (save to cloud storage)

---

## 💾 Save/Load Project Feature

### Purpose
Allow users to save their work-in-progress, including text, settings, and parameters, so they can:
- Continue work later
- Share configurations with team members
- Create templates for different voice styles
- Keep a library of commonly used settings

---

### Save Feature

**Button:** "💾 Save Project"
**Keyboard Shortcut:** `Ctrl + S`

**What Gets Saved:**
1. ✅ Input text content
2. ✅ Selected voice (pre-defined name or custom audio path)
3. ✅ Expression/emotion settings (text description or parameter values)
4. ✅ Output folder path
5. ✅ Generated audio file path (if exists)
6. ✅ Timestamp (created and last modified)

**Save Behavior:**
- First time: Opens "Save As" dialog
- Subsequent saves: Overwrites current file
- Shows "*" indicator when unsaved changes exist
- Confirmation before closing with unsaved changes

**File Format Options:**

**Option A: `.cbx` (ChatterBox project file)** - Custom extension
```
Pros: 
- Professional look
- Clearly identifies file type
- Can associate with app icon

Cons:
- Needs custom handler
- Not human-readable
```

**Option B: `.json`** - Standard JSON format (Recommended)
```
Pros:
- Human-readable
- Easy to edit manually
- Universal format
- Simple to implement

Cons:
- Generic extension
```

**Recommended:** Use `.json` for simplicity and readability

---

### Load Feature

**Button:** "📂 Load Project"
**Keyboard Shortcut:** `Ctrl + O`

**Load Behavior:**
1. Opens file picker dialog (filter: `.json` or `.cbx` files)
2. Checks if current project has unsaved changes
3. Prompts to save if changes exist
4. Loads file and validates format
5. Restores all settings to UI
6. Shows success notification

**What Gets Restored:**
- Text input field populated
- Voice selection restored
- Expression settings applied
- Output folder path set
- If generated audio path exists and file found, load into preview

**Error Handling:**
- Invalid file format → Show error message
- Missing audio files → Show warning, continue with other settings
- Corrupted file → Show detailed error

---

### UI Components

**Menu Bar Addition:**
```
┌──────────────────────────────────────┐
│ File                                  │
├──────────────────────────────────────┤
│ New Project          Ctrl+N          │
│ Open Project...      Ctrl+O          │
│ Save Project         Ctrl+S          │
│ Save As...           Ctrl+Shift+S    │
│ ─────────────────────────────────    │
│ Recent Projects      ▶               │
│ ─────────────────────────────────    │
│ Exit                 Alt+F4          │
└──────────────────────────────────────┘
```

**Or Toolbar Buttons:**
```
[📂 New] [📁 Open] [💾 Save] [💾 Save As]
```

**Status Bar:**
```
┌────────────────────────────────────────────┐
│ 💾 my_project.json - Saved 2 minutes ago  │
└────────────────────────────────────────────┘

OR (if unsaved changes):
┌────────────────────────────────────────────┐
│ 💾 my_project.json * (unsaved changes)    │
└────────────────────────────────────────────┘
```

---

### Example Project File Structure

```json
{
  "version": "1.0",
  "project_name": "Character Dialogue - Hero Intro",
  "created": "2025-11-07T14:30:52Z",
  "modified": "2025-11-07T15:45:12Z",
  
  "text": "Welcome, brave adventurer! Your journey begins now in the mystical land of Pixuu.",
  
  "output_folder": "C:\\Projects\\chatterbox\\outputs",
  
  "voice": {
    "mode": "predefined",
    "selected_voice": "Heroic Male",
    "custom_audio_path": null,
    "search_term": "hero"
  },
  
  "expression": {
    "mode": "text",
    "description": "Epic and inspiring, with a sense of adventure and excitement. Confident and welcoming tone.",
    "parameters": {
      "emotion": "excited",
      "energy": 80,
      "speed": 1.0,
      "pitch": 2,
      "emphasis": 70
    }
  },
  
  "generated_audio": {
    "exists": true,
    "path": "outputs/20251107_143052_welcome_brave_adventurer.wav",
    "filename": "20251107_143052_welcome_brave_adventurer.wav",
    "duration": 8.5,
    "sample_rate": 22050,
    "file_size_mb": 1.2
  },
  
  "metadata": {
    "app_version": "1.0.0",
    "chatterbox_version": "0.1.4"
  }
}
```

---

### Workflow Integration

**New User Workflow with Save:**
```
1. User types text and sets parameters
   ↓
2. Generates audio
   ↓
3. Likes the result
   ↓
4. Presses Ctrl+S or clicks "Save Project"
   ↓
5. Names and saves project: "hero_intro.json"
   ↓
6. Can load this project later to:
   - Generate similar audio
   - Tweak settings
   - Use as template
```

**Team Collaboration Workflow:**
```
1. Developer A creates voice profile
   ↓
2. Saves as "character_villain.json"
   ↓
3. Commits to Git repository
   ↓
4. Developer B loads "character_villain.json"
   ↓
5. Uses same settings for consistency
   ↓
6. Modifies text for different dialogues
```

---

### Recent Projects Feature (Nice-to-Have)

**Quick Access Menu:**
```
Recent Projects:
├─ hero_intro.json (Today, 3:45 PM)
├─ villain_taunt.json (Today, 2:30 PM)
├─ narrator_scene1.json (Yesterday)
├─ narrator_scene2.json (Yesterday)
└─ character_template.json (Nov 5)

[Clear Recent] [Pin/Unpin]
```

---

### Auto-Save Feature (Optional Enhancement)

**Settings:**
- Enable/disable auto-save
- Auto-save interval (1, 5, 10 minutes)
- Auto-save location: `projects/autosave/`
- Keep last 5 auto-saves
- Recover from crash

**UI Indicator:**
```
Status: Auto-saving... ●
Status: All changes saved ✓
Status: Last auto-save: 30 seconds ago
```

---

## 🎯 Success Criteria

1. **Usability**: Non-technical users can generate voice audio within 30 seconds
2. **Clarity**: All controls are self-explanatory
3. **Feedback**: User always knows what the app is doing
4. **Flexibility**: Basic users get simple interface, advanced users get full control
5. **Reliability**: Proper error handling and recovery

---

## 🚀 Development Phases

### Phase 1: MVP (Minimum Viable Product)
- Text input with Enter/Shift+Enter
- Generate button
- Basic audio generation
- Simple preview and export

### Phase 2: Core Features
- Output folder selection
- Loading states
- Error handling
- Audio player controls

### Phase 3: Advanced Features
- Voice selection dropdown
- Search functionality
- Custom voice import
- Expression controls

### Phase 4: Save/Load System
- Save project to JSON file
- Load project from file
- Keyboard shortcuts (Ctrl+S, Ctrl+O)
- Unsaved changes detection
- Recent projects list

### Phase 5: Polish
- UI improvements
- Auto-save feature
- Better error messages
- Performance optimization
- Project templates/presets

### Phase 6: Portable Distribution
- ✅ Create portable folder structure
- ✅ Build launcher script (ChatterboxTTS.bat)
- ✅ Package with embedded Python 3.11
- ✅ Include all dependencies (~3 GB)
- ✅ Write USER_README.txt
- ✅ Test on clean Windows machine
- ✅ Create ZIP for distribution (~2.2 GB)
- See `PORTABLE_BUILD_GUIDE.md` for detailed steps

---

## 📝 Notes for Developer

- Keep code simple and well-commented (JS developer background)
- Use descriptive variable names
- Separate UI logic from audio generation logic
- Add comments explaining Python-specific features
- Consider using Gradio for fastest development
- Test with various text lengths and special characters
- Handle edge cases (empty text, missing files, etc.)

---

## 🤝 Collaboration Note

This requirements document was created with assistance from Claude Sonnet (Anthropic's AI assistant) to translate user requirements into a structured, professional specification document.

---

**Last Updated:** November 7, 2025
**Version:** 1.0
**Status:** Ready for Development
