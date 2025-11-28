# VS Code Quick Reference - Audio Processor

Tham khảo nhanh các thao tác thường dùng khi develop Audio Processor trong VS Code.

---

## 🚀 Quick Start Commands

```bash
# 1. Open project
cd audio_processor
code .

# 2. Activate venv (trong VS Code terminal)
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows

# 3. Run main script
python main.py --help

# 4. Debug (press F5 in VS Code)
```

---

## ⌨️ Essential Keyboard Shortcuts

### Navigation
| Action | Shortcut | Description |
|--------|----------|-------------|
| Quick Open File | `Ctrl+P` | Type filename to open |
| Go to Definition | `F12` | Jump to function/class definition |
| Go Back | `Alt+←` | Return to previous location |
| Go to Symbol | `Ctrl+Shift+O` | List functions/classes in file |
| Find in Files | `Ctrl+Shift+F` | Search across all files |

### Editing
| Action | Shortcut | Description |
|--------|----------|-------------|
| Comment Line | `Ctrl+/` | Toggle comment |
| Format Document | `Shift+Alt+F` | Auto-format code |
| Rename Symbol | `F2` | Rename variable/function everywhere |
| Multi-cursor | `Alt+Click` | Edit multiple places at once |
| Duplicate Line | `Shift+Alt+↓` | Copy line down |
| Move Line | `Alt+↑/↓` | Move line up/down |
| Delete Line | `Ctrl+Shift+K` | Delete entire line |

### Running & Debugging
| Action | Shortcut | Description |
|--------|----------|-------------|
| Run File | `Ctrl+F5` | Run without debugging |
| Debug | `F5` | Start debugging |
| Toggle Breakpoint | `F9` | Add/remove breakpoint |
| Step Over | `F10` | Execute current line |
| Step Into | `F11` | Enter function |
| Continue | `F5` | Resume execution |

### Terminal & Panels
| Action | Shortcut | Description |
|--------|----------|-------------|
| Toggle Terminal | `` Ctrl+` `` | Show/hide terminal |
| New Terminal | `Ctrl+Shift+` ` | Create new terminal |
| Command Palette | `Ctrl+Shift+P` | Access all commands |
| Toggle Sidebar | `Ctrl+B` | Show/hide file explorer |

---

## 📁 File Structure Navigation

```
audio_processor/
├── config.py          → Press Ctrl+P, type "config"
├── transcriber.py     → Press Ctrl+P, type "trans"
├── segmenter.py       → Press Ctrl+P, type "seg"
├── processor.py       → Press Ctrl+P, type "proc"
├── main.py           → Press Ctrl+P, type "main"
├── worker.py         → Press Ctrl+P, type "work"
└── example.py        → Press Ctrl+P, type "exam"
```

**Tip:** Type `@` in Quick Open to see symbols (functions/classes)

---

## 🐛 Debug Configurations

### Available Configs (press F5)

1. **Python: Main Script**
   - Runs `main.py` with sample arguments
   - Good for: Testing full pipeline

2. **Python: Current File**
   - Runs currently open file
   - Good for: Testing individual modules

3. **Python: Example**
   - Runs `example.py`
   - Good for: Learning API usage

4. **Python: Worker**
   - Runs worker script
   - Good for: Testing distributed processing

### Quick Debug Tips

```python
# Set breakpoint: Click left of line number

# Inspect variables while debugging:
# 1. Hover over variable
# 2. Check VARIABLES panel
# 3. Use Debug Console to evaluate expressions

# Common debug console commands:
>>> len(segments)          # Check list length
>>> segments[0].text      # Inspect first segment
>>> config.whisper.model_size  # Check config
```

---

## 🔍 Search & Replace Patterns

### Find in Files (Ctrl+Shift+F)

**Example searches:**
```
# Find all function definitions
def.*\(

# Find all TODO comments
TODO:.*

# Find specific config usage
config\.whisper

# Find all print statements
print\(
```

### Replace Examples

**Change model size everywhere:**
```
Find:    model_size="base"
Replace: model_size="small"
```

**Update path separator (Windows → Unix):**
```
Find:    \\
Replace: /
Use Regex: Enable
```

---

## 💡 IntelliSense Quick Actions

### Code Completion
```python
# Type partial name and press Ctrl+Space
from processor import Aud|     # Suggests: AudioProcessor
config = App|                  # Suggests: AppConfig
```

### Quick Info
```python
# Hover over any function/class to see docstring
processor.process_single_file(  # Shows parameters and docs
```

### Parameter Hints
```python
# When typing function arguments, see parameter info
WhisperConfig(|    # Shows: model_size, device, language, etc.
```

---

## 🎨 Code Snippets

### Built-in Python Snippets

Type and press `Tab`:

```python
# Function
def|     → def function_name(args):

# Class
class|   → class ClassName:

# For loop
for|     → for item in items:

# Try-except
try|     → try: ... except:

# If-else
if|      → if condition:

# Main guard
ifmain|  → if __name__ == "__main__":
```

### Custom Snippets (Add your own)

**Settings → User Snippets → python.json**

---

## 🔧 Common Tasks

### 1. Add a New Feature

```
1. Create new file or edit existing
2. Write code with IntelliSense
3. Add docstrings (type """ and press Enter)
4. Test with F5 (debug)
5. Format with Shift+Alt+F
6. Save with Ctrl+S
```

### 2. Fix a Bug

```
1. Set breakpoint at suspected line (F9)
2. Start debug (F5)
3. Inspect variables in VARIABLES panel
4. Step through code (F10, F11)
5. Use Debug Console to test fixes
6. Fix and re-run
```

### 3. Refactor Code

```
1. Select code to extract
2. Right-click → "Extract Method" or "Extract Variable"
3. Or: Select + Ctrl+Shift+R
4. Rename symbol: F2
5. Format: Shift+Alt+F
```

### 4. Test Changes

```
1. Edit code
2. Save (Ctrl+S)
3. Run in terminal:
   python main.py --input test.wav --output ./test_out
4. Or debug with F5
5. Check output files
```

---

## 📊 Panel Overview

```
┌─────────────────────────────────────────────────────┐
│ 1. ACTIVITY BAR (Left)                              │
├─────────────────────────────────────────────────────┤
│ 📁 Explorer      - Files & folders                  │
│ 🔍 Search        - Find/replace in files            │
│ 🔀 Source Control - Git integration                 │
│ 🐛 Run & Debug   - Debug configurations            │
│ 🧩 Extensions    - Install/manage extensions       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 2. EDITOR AREA (Center)                             │
├─────────────────────────────────────────────────────┤
│ - Edit code here                                    │
│ - Multiple tabs for different files                │
│ - Split editor: Drag tab or Ctrl+\                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 3. PANEL (Bottom)                                   │
├─────────────────────────────────────────────────────┤
│ TERMINAL         - Run commands                     │
│ PROBLEMS         - Linting errors/warnings          │
│ OUTPUT          - Extension outputs                │
│ DEBUG CONSOLE   - Debug expressions                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 4. STATUS BAR (Bottom)                              │
├─────────────────────────────────────────────────────┤
│ Python 3.11 | venv | UTF-8 | Ln 45, Col 12 | ...  │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Workflow Examples

### Workflow 1: Add New Audio Format Support

```
1. Open segmenter.py (Ctrl+P → "seg")
2. Find load_audio() method (Ctrl+Shift+O → "load")
3. Add new format handling
4. Set breakpoint (F9)
5. Test with F5 (debug config: Python: Current File)
6. Verify in VARIABLES panel
7. Format code (Shift+Alt+F)
8. Save (Ctrl+S)
```

### Workflow 2: Change Default Model

```
1. Open config.py (Ctrl+P → "conf")
2. Find WhisperConfig class (Ctrl+Shift+O → "Whisper")
3. Change model_size default
4. Save (Ctrl+S)
5. Test: python main.py --help in terminal
6. Or: Run example.py (F5 → "Python: Example")
```

### Workflow 3: Debug Transcription Issue

```
1. Open transcriber.py
2. Set breakpoint in transcribe_to_sentences()
3. F5 → Select "Python: Example"
4. When breakpoint hits:
   - Check segments in VARIABLES
   - Evaluate in Debug Console: len(segments)
   - Step through with F10
5. Identify issue
6. Fix code
7. Restart debug (Ctrl+Shift+F5)
```

---

## 🔔 Status Bar Info

Click on status bar items for quick actions:

```
┌───────────────────────────────────────────────────┐
│ Python 3.11  |  venv  |  UTF-8  |  Spaces: 4    │
└───────────────────────────────────────────────────┘
     ↓             ↓         ↓            ↓
  Select      Select      Change      Change
Interpreter   venv     Encoding    Indentation
```

**Important indicators:**
- 🐍 **Python version** - Click to change interpreter
- 📦 **venv** - Shows active virtual environment
- ⚠️ **Errors/Warnings** - Click to see PROBLEMS panel
- 🔄 **Git branch** - Click for Git commands

---

## 📝 Quick Code Templates

### Add a New Processing Function

```python
def process_something(self, input_data: str) -> dict:
    """
    Description of what this does
    
    Args:
        input_data: Description
    
    Returns:
        dict: Result data
    """
    self.logger.info(f"Processing: {input_data}")
    
    try:
        # Your processing logic here
        result = {}
        
        self.logger.info("Processing complete")
        return result
        
    except Exception as e:
        self.logger.error(f"Error: {e}")
        raise
```

### Add a New CLI Argument

**In main.py:**
```python
parser.add_argument(
    '--your-option',
    type=str,
    default='default_value',
    help='Description of your option'
)
```

---

## 🚨 Common Errors & Quick Fixes

### ❌ "Module not found"
**Quick Fix:**
```bash
# In terminal (Ctrl+`)
pip install missing-module
```

### ❌ Red squiggles on imports
**Quick Fix:**
1. Bottom-left → Click Python version
2. Select correct interpreter (should show venv)
3. Reload: Ctrl+Shift+P → "Reload Window"

### ❌ "No Python interpreter selected"
**Quick Fix:**
1. Ctrl+Shift+P
2. "Python: Select Interpreter"
3. Choose ./venv/bin/python

### ❌ Formatting not working
**Quick Fix:**
```bash
pip install black
# Then: Shift+Alt+F
```

---

## 🎓 Pro Tips

### 1. Multi-cursor Editing
```
Alt+Click  → Add cursor at click position
Ctrl+Alt+↑/↓ → Add cursor above/below
Ctrl+D     → Select next occurrence
```

**Example:**
```python
# Change multiple variable names at once
# 1. Select "old_name"
# 2. Press Ctrl+D repeatedly
# 3. Type new name
```

### 2. Zen Mode (Distraction-free)
```
Ctrl+K Z   → Enter Zen mode
Esc Esc    → Exit Zen mode
```

### 3. Side-by-side Editing
```
Drag file tab to right → Split editor
Or: Ctrl+\
```

### 4. File Comparison
```
Right-click file → "Select for Compare"
Right-click another file → "Compare with Selected"
```

### 5. Peek Definition
```
Alt+F12    → Peek definition (inline view)
            No need to open new file
```

---

## 📚 Where to Find More

- **Command Palette:** `Ctrl+Shift+P` → type anything
- **Keyboard Shortcuts:** `Ctrl+K Ctrl+S` → full list
- **Settings:** `Ctrl+,` → search and configure
- **Extensions:** `Ctrl+Shift+X` → discover more tools

---

## ✅ Daily Workflow Checklist

- [ ] Open VS Code: `code .`
- [ ] Check Python interpreter (bottom-left)
- [ ] Activate venv if needed (terminal shows `(venv)`)
- [ ] Pull latest changes (Source Control)
- [ ] Edit code with IntelliSense
- [ ] Test with F5 (debug)
- [ ] Format code: `Shift+Alt+F`
- [ ] Check PROBLEMS panel (no errors)
- [ ] Commit changes (Source Control)

---

**💡 Remember:** Press `Ctrl+Shift+P` if you forget a shortcut - Command Palette has everything!

**🎯 Goal:** Speed up your development with VS Code superpowers!
