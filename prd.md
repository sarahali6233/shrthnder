# Product Requirements Document (PRD): Shrthnder - Cross-Platform Keyboard Event Listener and Text Injection System

## **Objective**
Develop an MVP for Shrthnder, a cross-platform desktop application that:
- Captures global keyboard events across all applications.
- Expands shorthand text into full text based on predefined rules.
- Injects the expanded text seamlessly into the active application.

--- btw idk omw ftgrph 

## **Scope**
Focus on creating a lightweight MVP with the following core functionalities:

1. **Global Keyboard Event Listener**:
   - Capture keypresses across all applications.
   - Detect predefined shorthand sequences.

2. **Text Expansion Logic**:
   - Implement a rule-based shorthand expansion system.

3. **Text Injection System**:
   - Inject expanded text into the active application seamlessly.

4. **Platform Support**:
   - Initial support for **Windows** and **macOS**.

5. **Simple UI**:
   - Allow users to configure shorthand rules and settings through an intuitive interface.

---
Btw idk omw	
## **Functional Requirements**

### **1. Global Keyboard Event Listener**
#### Description:
Capture keyboard events globally to detect shorthand sequences.

#### Implementation:
- Use platform-specific libraries for event hooking:
  - **Windows**: `pywin32` or `keyboard` library.
  - **macOS**: Quartz Event Services via `pynput` or `pyobjc`.

#### Example Code:
**Python Listener with `pynput`**
```python
from pynput import keyboard

def on_press(key):
    try:
        print(f"Key pressed: {key.char}")  # Logs character keys
    except AttributeError:
        print(f"Special key pressed: {key}")

# Start a global listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
```

---

### **2. Shorthand Expansion Logic**
#### Description:
Expand detected shorthand sequences into predefined full text.

#### Implementation:
- Use a dictionary to map shorthand to full text.
- Add support for real-time detection and expansion of shorthands.

#### Example Code:
**Rule-Based Expansion**
```python
# Define shorthand rules
shorthand_map = {
    "btw": "by the way",
    "idk": "I don't know",
    "omw": "on my way"
}

def expand_shorthand(input_text):
    return shorthand_map.get(input_text, input_text)

# Test example
print(expand_shorthand("btw"))  # Output: by the way
```

---

### **3. Text Injection System**
#### Description:
Inject expanded text into the active application where the user is typing.

#### Implementation:
- Use platform-specific libraries for simulating keystrokes:
  - **Windows**: `pywin32` or `pyautogui`.
  - **macOS**: `Quartz` or `pyobjc`.

#### Example Code:
**Injecting Text with `pyautogui`**
```python
import pyautogui

# Inject expanded text
expanded_text = "by the way"
pyautogui.typewrite(expanded_text)
```

---

### **4. Simple UI**
#### Description:
Provide a user-friendly interface for managing shorthand rules and application settings.

#### Features:
- **Rule Management**:
  - Add, edit, and delete shorthand rules.
  - View all configured rules in a table or list format.
- **Profile Management**:
  - Create and switch between profiles for different use cases (e.g., work, personal).
- **Settings Configuration**:
  - Enable/disable shorthand expansion.
  - Configure global keyboard listener settings (e.g., toggle hotkey).
- **Real-Time Testing**:
  - Allow users to test shorthand expansions directly within the UI.

#### Implementation:
- Use a GUI library such as:
  - **Windows/macOS/Linux**: `PyQt5` or `Tkinter`.

#### Example Code:
**Basic UI with PyQt5**
```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem

class ShrthnderUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shrthnder - Typing Efficiency Tool")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Button to add shorthand
        add_button = QPushButton("Add Shorthand")
        layout.addWidget(add_button)

        # Table for shorthand rules
        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Shorthand", "Expansion"])
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication([])
    window = ShrthnderUI()
    window.show()
    app.exec_()
```

---

## **Non-Functional Requirements**

### **1. Performance**
- Minimal latency in detecting, expanding, and injecting text.
- Lightweight, ensuring low CPU and memory usage.

### **2. Security**
- Store shorthand rules locally and securely.
- Ensure the application respects user privacy and does not log sensitive data.

### **3. Compatibility**
- Initial support for Windows 10+ and macOS 11+.

---

## **Development Plan**

### **Phase 1: Global Keyboard Listener**
- Implement a basic keyboard listener for Windows and macOS.
- Log all keypresses to verify functionality.

### **Phase 2: Shorthand Expansion**
- Create a dictionary-based shorthand expansion system.
- Test real-time detection and expansion.

### **Phase 3: Text Injection**
- Implement text injection using platform-specific tools.
- Test text injection in common applications (e.g., browsers, text editors).

### **Phase 4: UI Development**
- Build a simple UI for managing shorthand rules and profiles.
- Integrate the UI with the backend systems (listener, expansion, injection).

### **Phase 5: Integration**
- Integrate the listener, expansion, injection, and UI systems.
- Ensure seamless operation across platforms.

---

## **Testing Requirements**

1. **Functional Testing**:
   - Verify shorthand detection and expansion in real-time.
   - Test text injection across multiple applications.

2. **UI Testing**:
   - Ensure the UI is intuitive and responsive.
   - Test all user interactions (e.g., adding/editing rules, switching profiles).

3. **Performance Testing**:
   - Measure latency between detection and injection.
   - Ensure the application remains lightweight.

4. **Platform Testing**:
   - Ensure functionality on both Windows and macOS.

---

## **Future Enhancements**

1. **Linux Support**:
   - Add support for Linux using libraries like `evdev` or `xdotool`.

2. **Customizable Shorthands**:
   - Allow users to define their own shorthand rules via a GUI.

3. **Cloud Sync**:
   - Enable shorthand rules and profiles to sync across devices.

4. **Dynamic AI-Based Expansions**:
   - Integrate AI to suggest context-aware expansions.

