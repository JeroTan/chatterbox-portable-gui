# Developer Guide - Modular Desktop App

## Architecture Overview

This is a **modular desktop application** following separation of concerns:

```
┌─────────────────┐
│    main.py      │  Entry point - wires everything together
└────────┬────────┘
         │
    ┌────┴───────────┬────────────────┬─────────────┐
    │                │                │             │
┌───▼──────┐  ┌──────▼───────┐  ┌─────▼─────┐  ┌────▼──────┐
│  UI      │  │   Features   │  │   Store   │  │  Utils    │
│Components│  │  (Logic)     │  │  (State)  │  │ (Helpers) │
└──────────┘  └──────────────┘  └───────────┘  └───────────┘
```

---

## File Roles

### `src/main.py`
**Role:** Application shell
- Creates main window
- Instantiates components
- Wires events
- Handles menu/shortcuts

**DON'T:** Put business logic here
**DO:** Keep it as a thin orchestration layer

### `src/components/*.py`
**Role:** Reusable UI widgets
- Self-contained visual components
- Accept callbacks for events
- Expose get/set methods

**Example:**
```python
class MyComponent:
    def __init__(self, parent, on_change=None):
        self.frame = ttk.Frame(parent)
        # Build UI here
        
    def get_value(self):
        # Return component value
        
    def set_value(self, val):
        # Update component
```

### `src/features/*.py`
**Role:** Business logic
- TTS generation
- File operations
- API calls
- Data processing

**Example:**
```python
def generate_audio(text, config, output_path):
    # TTS logic here
    return audio_path
```

### `src/store/state.py`
**Role:** Global state manager
- Single source of truth
- Observable (notify on changes)
- Like Redux/Vuex

**Usage:**
```python
# Update
app_state.update(text="Hello", speed=1.5)

# Subscribe
app_state.subscribe(my_callback)

# Access
current_text = app_state.text_input
```

### `src/utils/*.py`
**Role:** Helper functions
- No side effects
- Reusable utilities
- Configuration constants

---

## Adding New Features

### Adding a New UI Component

1. **Create file** in `src/components/my_component.py`
2. **Define class**:
```python
import tkinter as tk
from tkinter import ttk

class MyComponent:
    def __init__(self, parent, on_something=None):
        self.on_something = on_something
        self.frame = ttk.LabelFrame(parent, text="My Component")
        # Add widgets to self.frame
        
    def get_data(self):
        return self.some_value
```
3. **Use in main.py**:
```python
from components.my_component import MyComponent

# In __init__:
self.my_comp = MyComponent(parent, on_something=self._handle_it)
self.my_comp.frame.pack()
```

### Adding New Business Logic

1. **Create file** in `src/features/my_feature.py`
2. **Define functions/classes**:
```python
def do_something(data):
    # Logic here
    return result
```
3. **Import and use**:
```python
from features.my_feature import do_something

result = do_something(my_data)
```

### Adding State Variables

1. **Edit** `src/store/state.py`
2. **Add to __init__**:
```python
def __init__(self):
    # ... existing ...
    self.my_new_var = "default"
```
3. **Use anywhere**:
```python
from store.state import app_state

app_state.update(my_new_var="new value")
print(app_state.my_new_var)
```

---

## Common Patterns

### Pattern: Component with Callback

**Component:**
```python
class MyInput:
    def __init__(self, parent, on_change=None):
        self.on_change = on_change
        self.var = tk.StringVar()
        self.var.trace_add("write", lambda *_: self._trigger())
        
    def _trigger(self):
        if self.on_change:
            self.on_change()
            
    def get_value(self):
        return self.var.get()
```

**Usage:**
```python
def _on_input_change(self):
    value = self.my_input.get_value()
    app_state.update(my_field=value)

self.my_input = MyInput(parent, on_change=self._on_input_change)
```

### Pattern: Feature with Error Handling

```python
def risky_operation(data):
    try:
        result = do_something(data)
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        messagebox.showerror("Error", str(e))
        return None
```

### Pattern: State with Observers

```python
# In component __init__:
app_state.subscribe(self._update_ui)

def _update_ui(self):
    # Sync UI with state
    self.text_var.set(app_state.some_value)
```

---

## Keyboard Shortcuts

Defined in `src/utils/config.py`:
```python
SHORTCUTS = {
    "generate": "<Return>",
    "save": "<Control-s>",
    # ...
}
```

Bound in `main.py`:
```python
self.root.bind(SHORTCUTS["save"], lambda e: self._save())
```

---

## Testing Strategy

### Unit Tests
Test individual features:
```python
def test_generate_filename():
    result = generate_audio_filename("Hello world")
    assert result.endswith(".wav")
    assert "hello" in result.lower()
```

### Integration Tests
Test component + feature:
```python
def test_generate_button():
    app = ChatterboxApp()
    app.text_input.set_text("Test")
    app._generate_audio()
    assert app_state.generated_audio_path is not None
```

---

## Debugging Tips

### Print State
```python
# In any file:
from store.state import app_state
print(app_state.get_state_dict())
```

### Component Inspection
```python
# Check component value:
print(f"Text input: {self.text_input.get_text()}")
print(f"Voice config: {self.voice_selector.get_voice_config()}")
```

### Feature Testing
Test features without UI:
```python
from features.generate import tts_generator

result = tts_generator.generate_audio(
    "Test",
    {"mode": "predefined", "voice": "Default"},
    {"mode": "text", "text": "happy"},
    Path("test.wav")
)
```

---

## Performance Tips

### Lazy Loading
```python
class HeavyFeature:
    def __init__(self):
        self.model = None
        
    def initialize(self):
        if not self.model:
            # Load only when needed
            self.model = load_heavy_model()
```

### Async Operations
For long tasks:
```python
import threading

def _generate_audio(self):
    self.status.set("Generating...")
    
    def bg_task():
        result = tts_generator.generate_audio(...)
        self.root.after(0, lambda: self._on_complete(result))
    
    threading.Thread(target=bg_task).start()
```

---

## Code Style

### Naming Conventions
- **Classes:** `PascalCase` (e.g., `TextInputComponent`)
- **Functions:** `snake_case` (e.g., `generate_audio`)
- **Private methods:** `_leading_underscore` (e.g., `_setup_ui`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `APP_NAME`)

### File Organization
Each file should have:
```python
"""
File docstring explaining purpose
"""

import stdlib  # Standard library first
import third_party  # Then third-party
from local import stuff  # Then local imports

# Constants
SOME_CONSTANT = "value"

# Classes/functions
class MyClass:
    pass
```

### Comments
- Use `#` for single-line comments
- Use `"""docstrings"""` for classes/functions
- Mark TODOs: `# TODO: description`
- Mark placeholders: `# PLACEHOLDER: will implement later`

---

## Common Issues

### Import Errors
**Problem:** `ImportError: attempted relative import`
**Solution:** Use absolute imports from src:
```python
# ❌ from ..utils import config
# ✅ from utils import config
```

### State Not Updating UI
**Problem:** Changed state but UI doesn't update
**Solution:** Subscribe to state changes:
```python
app_state.subscribe(self._update_ui)
```

### Component Not Showing
**Problem:** Created component but not visible
**Solution:** Remember to pack/grid/place it:
```python
self.my_component.frame.pack()
```

---

## Folder Structure Cheatsheet

```
src/
├── main.py              # → App shell, wiring
├── components/          # → Visual widgets
│   ├── text_input.py
│   ├── voice_selector.py
│   └── expression_controls.py
├── features/            # → Business logic
│   ├── generate.py      # → TTS generation
│   ├── project.py       # → Save/load
│   └── export.py        # → Export audio
├── store/               # → State management
│   └── state.py
└── utils/               # → Helpers
    ├── config.py        # → Constants
    └── file_utils.py    # → File ops
```

**Remember:**
- **Components** = What users see
- **Features** = What app does
- **Store** = What app remembers
- **Utils** = Helper tools

---

## Quick Reference

### Run App
```powershell
.\.venv\Scripts\python.exe src\main.py
```

### Import Patterns
```python
# Components
from components.text_input import TextInputComponent

# Features
from features.generate import tts_generator

# State
from store.state import app_state

# Config
from utils.config import APP_NAME, SHORTCUTS

# File utils
from utils.file_utils import generate_audio_filename
```

### Event Flow
```
User Action (UI)
    ↓
Event Handler (main.py method)
    ↓
Update State (app_state.update)
    ↓
Call Feature (features/*.py function)
    ↓
Return Result
    ↓
Update UI
```

---

This architecture keeps code **clean, testable, and maintainable**! 🎉
