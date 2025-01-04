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
        self.detect_keyboard_layout()
        
    def detect_keyboard_layout(self):
        self.os_name = platform.system()
        logging.info(f"Detected OS: {self.os_name}")
        
        if self.os_name == "Darwin":  # macOS
            try:
                # Use Terminal Input Source command to get keyboard layout
                import subprocess
                cmd = "defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources | grep -w 'KeyboardLayout Name' | awk -F'\"' '{print $4}'"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                layout_name = result.stdout.strip()
                logging.info(f"Raw keyboard layout from system: {layout_name}")
                
                # Map macOS keyboard names to our layout names
                macos_layout_map = {
                    "German": "German",
                    "German-DIN": "German",
                    "ABC": "English",
                    "US": "English",
                    "British": "English",
                    "": "English"  # Default if empty
                }
                
                self.layout = macos_layout_map.get(layout_name, "English")
                logging.info(f"Mapped keyboard layout: {self.layout}")
            except Exception as e:
                logging.error(f"Error detecting keyboard layout: {e}")
                # Fallback to locale method
                self.detect_from_locale()
        else:
            # For other operating systems, use locale method
            self.detect_from_locale()
            
    def detect_from_locale(self):
        # Get system locale
        self.system_locale = locale.getdefaultlocale()[0]
        logging.info(f"Detected system locale: {self.system_locale}")
        
        # Map common layouts
        self.layout_map = {
            'de_DE': 'German',
            'de_AT': 'German',
            'de_CH': 'German',
            'en_US': 'English',
            'en_GB': 'English',
            'fr_FR': 'French',
            'es_ES': 'Spanish'
        }
        
        self.layout = self.layout_map.get(self.system_locale, 'English')
        logging.info(f"Using keyboard layout from locale: {self.layout}")
        
    def is_alpha(self, key):
        """Check if a key is alphabetic based on the current layout"""
        try:
            if hasattr(key, 'char'):
                # For German keyboard, include umlauts and ß
                if self.layout == 'German':
                    german_chars = 'abcdefghijklmnopqrstuvwxyzäöüßABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
                    return key.char in german_chars
                # Add more layout-specific characters as needed
                return key.char.isalpha()
            return False
        except AttributeError:
            return False

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
        
        # Status and keyboard layout label
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Shrthnder is running...")
        self.keyboard_label = QLabel(f"Detected Keyboard: {self.keyboard_controller.layout_manager.layout}")
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.keyboard_label)
        layout.addLayout(status_layout)
        
        # Language selector
        language_layout = QHBoxLayout()
        language_label = QLabel("Input Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "German"])
        self.language_combo.setCurrentText(self.keyboard_controller.input_language)
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        layout.addLayout(language_layout)
        
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
            if hasattr(key, 'char'):
                if self.layout_manager.is_alpha(key):
                    self.current_word += key.char
                    logging.info(f"Current word buffer: {self.current_word}")
                elif key.char in [' ', '.', ',', '!', '?']:
                    logging.info(f"Punctuation detected: {key.char}, checking word: {self.current_word}")
                    self.process_word()
            logging.info(f"Key pressed: {key}")  # Add this line for debugging
        except AttributeError:
            if key == keyboard.Key.space:
                logging.info(f"Space key detected, checking word: {self.current_word}")
                self.process_word()
            elif key == keyboard.Key.enter:
                logging.info(f"Enter key detected, checking word: {self.current_word}")
                self.process_word()
            logging.info(f"Special key pressed: {key}")  # Add this line for debugging

    def on_release(self, key):
        try:
            if key == keyboard.Key.space:
                logging.info("Space key released")
                self.process_word()
        except AttributeError:
            pass
        return True

    def process_word(self):
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
            for _ in range(len(self.current_word)):
                pyautogui.press('backspace')
            
            # Get the expansion and ensure it's the exact string from the shortcuts
            expansion = self.shorthand_map[self.current_word.lower()]
            logging.info(f"Expanding to: {expansion} using {self.input_language} on {self.layout_manager.layout} keyboard")
            
            if self.input_language == "English" and self.layout_manager.layout == "German":
                # Special handling for apostrophe on German keyboard
                for i, char in enumerate(expansion):
                    if char == "'":
                        # For apostrophe on German keyboard, press the key right of Ä (usually #39)
                        pyautogui.press("#")
                    elif char == "I":
                        # For capital I, use shift + i
                        pyautogui.keyDown('shift')
                        pyautogui.press('i')
                        pyautogui.keyUp('shift')
                    else:
                        pyautogui.write(char)
                    pyautogui.sleep(0.02)
                    logging.info(f"Typed character: {char}")
            else:
                # Normal typing for matching language and keyboard
                for char in expansion:
                    pyautogui.write(char)
                    pyautogui.sleep(0.02)
                    logging.info(f"Typed character: {char}")
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