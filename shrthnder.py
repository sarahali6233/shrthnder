import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from pynput import keyboard
import pyautogui
import json
import os
import logging
import locale
import platform

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class KeyboardLayoutManager:
    def __init__(self):
        self.layout = "QWERTY"  # Default layout
        self.detect_keyboard_layout()  # This will now just set an initial suggestion
        
    def detect_keyboard_layout(self):
        """Detect keyboard layout as a suggestion only"""
        self.os_name = platform.system()
        logging.info(f"Detected OS: {self.os_name}")
        
        if self.os_name == "Darwin":  # macOS
            try:
                import subprocess
                cmd = "defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources | grep -w 'KeyboardLayout Name' | awk -F'\"' '{print $4}'"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                layout_name = result.stdout.strip()
                
                # Map macOS keyboard names to actual keyboard layouts
                macos_layout_map = {
                    "German": "QWERTZ",
                    "German-DIN": "QWERTZ",
                    "Swiss German": "QWERTZ",
                    "ABC": "QWERTY",
                    "US": "QWERTY",
                    "British": "QWERTY",
                    "": "QWERTY"
                }
                
                # Just set as suggestion
                self.layout = macos_layout_map.get(layout_name, "QWERTY")
                logging.info(f"Suggested keyboard layout: {self.layout}")
            except Exception as e:
                logging.error(f"Error detecting keyboard layout: {e}")
                self.layout = "QWERTY"

class ShrthnderUI(QMainWindow):
    def __init__(self, keyboard_controller):
        super().__init__()
        self.keyboard_controller = keyboard_controller
        self.shorthand_map = keyboard_controller.shorthand_map
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Shrthnder - Typing Efficiency Tool")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Status label
        self.status_label = QLabel("Shrthnder is running...")
        layout.addWidget(self.status_label)
        
        # Settings section
        settings_layout = QHBoxLayout()
        
        # Language selector
        language_group = QVBoxLayout()
        language_label = QLabel("Input Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "German"])
        self.language_combo.setCurrentText(self.keyboard_controller.input_language)
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        language_group.addWidget(language_label)
        language_group.addWidget(self.language_combo)
        settings_layout.addLayout(language_group)
        
        # Keyboard layout selector
        keyboard_group = QVBoxLayout()
        keyboard_label = QLabel("Keyboard Layout:")
        self.keyboard_combo = QComboBox()
        self.keyboard_combo.addItems(["QWERTZ", "QWERTY", "AZERTY"])
        self.keyboard_combo.setCurrentText(self.keyboard_controller.layout_manager.layout)
        self.keyboard_combo.currentTextChanged.connect(self.on_keyboard_changed)
        keyboard_group.addWidget(keyboard_label)
        keyboard_group.addWidget(self.keyboard_combo)
        settings_layout.addLayout(keyboard_group)
        
        layout.addLayout(settings_layout)
        
        # Add shorthand section
        shorthand_layout = QVBoxLayout()
        self.shorthand_input = QLineEdit()
        self.shorthand_input.setPlaceholderText("Enter shorthand (e.g., btw)")
        self.expansion_input = QLineEdit()
        self.expansion_input.setPlaceholderText("Enter expansion (e.g., by the way)")
        
        add_button = QPushButton("Add Shorthand")
        add_button.clicked.connect(self.add_shorthand)
        
        shorthand_layout.addWidget(self.shorthand_input)
        shorthand_layout.addWidget(self.expansion_input)
        shorthand_layout.addWidget(add_button)
        layout.addLayout(shorthand_layout)
        
        # Table for shorthand rules
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Shorthand", "Expansion"])
        self.update_table()
        layout.addWidget(self.table)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_language_changed(self, new_language):
        self.keyboard_controller.input_language = new_language
        logging.info(f"Input language changed to: {new_language}")

    def on_keyboard_changed(self, new_layout):
        self.keyboard_controller.layout_manager.layout = new_layout
        logging.info(f"Keyboard layout changed to: {new_layout}")

    def load_shortcuts(self):
        if os.path.exists('shortcuts.json'):
            with open('shortcuts.json', 'r') as f:
                return json.load(f)
        return {
            "btw": "by the way",
            "idk": "I don't know",
            "omw": "on my way"
        }
        
    def save_shortcuts(self):
        with open('shortcuts.json', 'w') as f:
            json.dump(self.shorthand_map, f)
            # Update the keyboard controller's shortcuts
            self.keyboard_controller.shorthand_map = self.shorthand_map
            
    def update_table(self):
        self.table.setRowCount(len(self.shorthand_map))
        for i, (shorthand, expansion) in enumerate(self.shorthand_map.items()):
            self.table.setItem(i, 0, QTableWidgetItem(shorthand))
            self.table.setItem(i, 1, QTableWidgetItem(expansion))

    def add_shorthand(self):
        shorthand = self.shorthand_input.text().strip()
        expansion = self.expansion_input.text().strip()
        
        if shorthand and expansion:
            self.shorthand_map[shorthand] = expansion
            self.save_shortcuts()
            self.update_table()
            self.shorthand_input.clear()
            self.expansion_input.clear()
            
class KeyboardController:
    def __init__(self):
        self.current_word = ""
        self.layout_manager = KeyboardLayoutManager()
        self.shorthand_map = self.load_shortcuts()
        self.input_language = "English"  # Default input language
        logging.info(f"Initialized KeyboardController with shortcuts: {self.shorthand_map}")
        
    def load_shortcuts(self):
        if os.path.exists('shortcuts.json'):
            with open('shortcuts.json', 'r', encoding='utf-8') as f:
                shortcuts = json.load(f)
                logging.info(f"Loaded shortcuts from file: {shortcuts}")
                return shortcuts
        return {
            "btw": "by the way",
            "idk": "I don't know",
            "omw": "on my way"
        }
    
    def on_press(self, key):
        try:
            # Convert the key to string representation
            if isinstance(key, keyboard.KeyCode):
                char = key.char
            else:
                char = None
                
            if char:
                logging.info(f"Key pressed: {char}")
                if char.isalpha():
                    self.current_word += char
                    logging.info(f"Current word buffer: {self.current_word}")
                elif char in [' ', '.', ',', '!', '?']:
                    logging.info(f"Punctuation detected: {char}, checking word: {self.current_word}")
                    self.process_word()
            elif key == keyboard.Key.space:
                logging.info(f"Space key detected, checking word: {self.current_word}")
                self.process_word()
            elif key == keyboard.Key.enter:
                logging.info(f"Enter key detected, checking word: {self.current_word}")
                self.process_word()
            elif key == keyboard.Key.backspace:
                if self.current_word:
                    self.current_word = self.current_word[:-1]
                    logging.info(f"Backspace pressed, new buffer: {self.current_word}")
                    
        except AttributeError as e:
            logging.error(f"Error processing key: {e}")

    def on_release(self, key):
        try:
            if key == keyboard.Key.space:
                logging.info("Space key released")
        except AttributeError:
            pass
        return True

    def process_word(self):
        if not self.current_word:  # Skip empty words
            return
            
        logging.info(f"Processing word: {self.current_word}")
        logging.info(f"Available shortcuts: {self.shorthand_map}")
        logging.info(f"Is '{self.current_word.lower()}' in shortcuts? {self.current_word.lower() in self.shorthand_map}")
        self.check_and_expand()
        self.current_word = ""
                
    def check_and_expand(self):
        logging.info(f"Checking word '{self.current_word}' against shortcuts")
        if self.current_word.lower() in self.shorthand_map:
            logging.info(f"Found shorthand match for: {self.current_word}")
            # Delete the shorthand
            logging.info(f"Deleting {len(self.current_word)} characters")
            pyautogui.press('backspace', presses=len(self.current_word))
            
            # Get the expansion and ensure it's the exact string from the shortcuts
            expansion = self.shorthand_map[self.current_word.lower()]
            logging.info(f"Expanding to: {expansion} using {self.input_language} on {self.layout_manager.layout} keyboard")
            
            if self.input_language == "English" and self.layout_manager.layout == "QWERTZ":
                # Map for QWERTZ keyboard when typing English text
                qwertz_map = {
                    'y': 'z',
                    'z': 'y',
                    'Y': 'Z',
                    'Z': 'Y'
                }
                
                # Clear any pending keystrokes
                pyautogui.sleep(0.1)
                
                # Delete the shorthand again to ensure clean state
                pyautogui.press('backspace', presses=len(self.current_word))
                
                # Type with QWERTZ keyboard adjustments
                for char in expansion:
                    if char in qwertz_map:
                        pyautogui.press(qwertz_map[char].lower())
                    elif char == "I":
                        pyautogui.keyDown('shift')
                        pyautogui.press('i')
                        pyautogui.keyUp('shift')
                    elif char == "'":
                        pyautogui.press('#')
                    else:
                        pyautogui.press(char.lower())
                    pyautogui.sleep(0.02)
            else:
                # Normal typing for matching language and keyboard
                pyautogui.write(expansion)
                logging.info(f"Typed expansion: {expansion}")
        else:
            logging.info(f"No expansion found for: {self.current_word}")

def main():
    app = QApplication(sys.argv)
    
    # Initialize the keyboard controller
    keyboard_controller = KeyboardController()
    
    # Start the keyboard listener with both press and release callbacks
    listener = keyboard.Listener(
        on_press=keyboard_controller.on_press,
        on_release=keyboard_controller.on_release
    )
    listener.start()
    
    # Create and show the UI
    window = ShrthnderUI(keyboard_controller)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 