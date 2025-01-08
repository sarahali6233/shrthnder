import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QHBoxLayout, QComboBox, QInputDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from pynput import keyboard
import pyautogui
import json
import os
import logging
import locale
import platform
import time
from pynput.keyboard import Key
from platform_specific import TextInputFactory

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class KeyboardLayoutManager:
    def __init__(self):
        self.layout = "QWERTZ" if locale.getdefaultlocale()[0].startswith('de') else "QWERTY"
        self.logger = logging.getLogger('shrthnder')

    def get_char(self, key):
        try:
            # Handle special keys
            if hasattr(key, 'char') and key.char:
                return key.char
            
            # Map special keys based on layout
            if self.layout == "QWERTZ":
                special_keys = {
                    'z': 'y',
                    'y': 'z',
                }
                if hasattr(key, 'char') and key.char in special_keys:
                    return special_keys[key.char]
            
            # Return space for space key
            if key == Key.space:
                return ' '
            
            # Return newline for enter key
            if key == Key.enter:
                return '\n'
            
            return ''
        except Exception as e:
            self.logger.error(f"Error getting character: {e}")
            return ''

class KeyboardController:
    def __init__(self):
        self.logger = self.setup_logger()
        self.current_word = ""
        self.layout_manager = KeyboardLayoutManager()
        self.input_language = "English"  # Default input language
        self.current_profile = "Default"
        self.shortcuts = self.load_default_shortcuts()
        self.shorthand_map = self.shortcuts
        self.profiles = self.load_default_shortcuts()
        self.keyboard_listener = None
        self.text_input = TextInputFactory.get_text_input()

    def setup_logger(self):
        logger = logging.getLogger('shrthnder')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_default_shortcuts(self):
        # Try to load from file first
        profiles_file = 'shrthnder_profiles.json'
        if os.path.exists(profiles_file):
            try:
                with open(profiles_file, 'r') as f:
                    saved_profiles = json.load(f)
                self.logger.info("Loaded profiles from file")
                return saved_profiles
            except Exception as e:
                self.logger.error(f"Error loading profiles from file: {e}")

        # Default profiles if file doesn't exist or has error
        profiles = {
            "Default": {
                "btw": "by the way",
                "idk": "I don't know",
                "omw": "on my way"
            },
            "Developer": {
                "cls": "class",
                "fn": "function",
                "ret": "return",
                "imp": "import",
                "pr": "print"
            },
            "Medical": {
                "pt": "patient",
                "rx": "prescription",
                "dx": "diagnosis",
                "tx": "treatment",
                "hx": "history"
            },
            "Legal": {
                "def": "defendant",
                "plt": "plaintiff",
                "jdg": "judgment",
                "crt": "court",
                "att": "attorney"
            },
            "Student": {
                "asap": "as soon as possible",
                "tba": "to be announced",
                "tbd": "to be determined",
                "eg": "for example",
                "ie": "that is"
            }
        }
        # Save default profiles to file
        try:
            with open(profiles_file, 'w') as f:
                json.dump(profiles, f, indent=4)
            self.logger.info("Saved default profiles to file")
        except Exception as e:
            self.logger.error(f"Error saving default profiles to file: {e}")
        
        return profiles

    def start(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()
        self.logger.info(f"Started keyboard listener with {self.layout_manager.layout} layout")

    def stop(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None

    def on_press(self, key):
        try:
            # If space is pressed, check for expansion
            if key == Key.space:
                if self.current_word.lower() in self.profiles[self.current_profile]:
                    self.check_and_expand()
                self.current_word = ""  # Reset current word
                return

            # Get character and add to current word if it's alphanumeric
            if hasattr(key, 'char') and key.char:
                if key.char.isalpha() or key.char.isdigit():
                    self.current_word += key.char
        except AttributeError:
            pass

    def check_and_expand(self):
        if not self.current_word:
            return

        try:
            # Get the expansion
            expansion = self.profiles[self.current_profile].get(self.current_word.lower())
            
            # Handle QWERTZ mapping if needed
            if self.layout_manager.layout == "QWERTZ":
                modified_text = ""
                for char in expansion:
                    if char.lower() == 'y':
                        modified_text += 'z' if char.islower() else 'Z'
                    elif char.lower() == 'z':
                        modified_text += 'y' if char.islower() else 'Y'
                    elif char == "'":
                        modified_text += "#"  # Use hash key for apostrophe on German keyboard
                    else:
                        modified_text += char
                expansion = modified_text

            # Delete the original text plus one extra character to prevent duplication
            self.text_input.delete_chars(len(self.current_word) + 1)
            
            # Insert the expanded text with a space
            self.text_input.insert_text(expansion + " ")
                
        except Exception as e:
            self.logger.error(f"Error in check_and_expand: {e}")
            return

    def save_profiles(self):
        """Save all profiles to file."""
        try:
            self.logger.info("Saving profiles")
            # Update the current profile's shortcuts
            self.shortcuts = self.profiles[self.current_profile]
            self.shorthand_map = self.shortcuts
            
            # Save to file
            profiles_file = 'shrthnder_profiles.json'
            with open(profiles_file, 'w') as f:
                json.dump(self.profiles, f, indent=4)
            self.logger.info("Profiles saved to file successfully")
        except Exception as e:
            self.logger.error(f"Error saving profiles: {e}")

    def create_profile(self, profile_name):
        profile_name = profile_name.strip()  # Remove whitespace
        if profile_name.lower() not in [p.lower() for p in self.profiles.keys()]:
            self.profiles[profile_name] = {}
            self.current_profile = profile_name
            self.shortcuts = self.profiles[profile_name]
            self.shorthand_map = self.profiles[profile_name]  # Fix: use profiles directly
            self.save_profiles()
            self.logger.info(f"Created new profile: {profile_name}")

    def switch_profile(self, profile_name):
        profile_name = profile_name.strip()  # Remove whitespace
        # Case-insensitive profile lookup
        profile_dict = {k.lower(): k for k in self.profiles.keys()}
        if profile_name.lower() in profile_dict:
            actual_name = profile_dict[profile_name.lower()]
            self.set_profile(actual_name)
            self.logger.info(f"Switched to profile: {actual_name}")
        else:
            self.logger.error(f"Profile not found: {profile_name}")
            self.set_profile("Default")

    def set_profile(self, profile_name):
        if profile_name in self.profiles:
            self.current_profile = profile_name
            self.shortcuts = self.profiles[profile_name]
            self.shorthand_map = self.profiles[profile_name]  # Fix: use profiles directly
            self.logger.info(f"Switched to profile: {profile_name}")

    def get_profiles(self):
        return list(self.profiles.keys())

    def delete_profile(self, profile_name):
        if profile_name in self.profiles:
            del self.profiles[profile_name]
            self.current_profile = "Default"
            self.shortcuts = self.profiles[self.current_profile]
            self.shorthand_map = self.shortcuts
            self.save_profiles()
            self.logger.info(f"Deleted profile: {profile_name}")

    def set_input_language(self, language):
        self.input_language = language
        self.logger.info(f"Set input language to: {language}")

    def add_shorthand(self):
        shorthand = self.shorthand_input.text().strip()
        expansion = self.expansion_input.text().strip()
        
        if shorthand and expansion:
            # Add to current profile
            current_profile = self.keyboard_controller.current_profile
            self.keyboard_controller.profiles[current_profile][shorthand] = expansion
            self.keyboard_controller.save_profiles()
            # Update the controller's shorthand map
            self.keyboard_controller.shorthand_map = self.keyboard_controller.profiles[current_profile]
            self.update_table()
            self.shorthand_input.clear()
            self.expansion_input.clear()

class MainWindow(QMainWindow):
    def __init__(self, keyboard_controller):
        super().__init__()
        self.keyboard_controller = keyboard_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Shrthnder - Typing Efficiency Tool")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                margin: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
                min-width: 150px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 5px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Status label with better styling
        self.status_label = QLabel("Shrthnder is running...")
        self.status_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        layout.addWidget(self.status_label)
        
        # Profile selector
        settings_layout = QHBoxLayout()
        
        # Profile group
        profile_group = QVBoxLayout()
        profile_label = QLabel("Profile:")
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(self.keyboard_controller.get_profiles())
        self.profile_combo.setCurrentText(self.keyboard_controller.current_profile)
        self.profile_combo.currentTextChanged.connect(self.on_profile_changed)
        profile_group.addWidget(profile_label)
        profile_group.addWidget(self.profile_combo)
        settings_layout.addLayout(profile_group)
        
        # Language group
        language_group = QVBoxLayout()
        language_label = QLabel("Input Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "German"])
        self.language_combo.setCurrentText(self.keyboard_controller.input_language)
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        language_group.addWidget(language_label)
        language_group.addWidget(self.language_combo)
        settings_layout.addLayout(language_group)
        
        layout.addLayout(settings_layout)
        
        # Add shorthand section
        shorthand_layout = QVBoxLayout()
        shorthand_label = QLabel("Add Custom Shorthand:")
        shorthand_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        self.shorthand_input = QLineEdit()
        self.shorthand_input.setPlaceholderText("Enter shorthand (e.g., btw)")
        self.expansion_input = QLineEdit()
        self.expansion_input.setPlaceholderText("Enter expansion (e.g., by the way)")
        
        add_button = QPushButton("Add Shorthand")
        add_button.clicked.connect(self.add_shorthand)
        
        shorthand_layout.addWidget(shorthand_label)
        shorthand_layout.addWidget(self.shorthand_input)
        shorthand_layout.addWidget(self.expansion_input)
        shorthand_layout.addWidget(add_button)
        layout.addLayout(shorthand_layout)
        
        # Table for shorthand rules
        table_label = QLabel("Available Shortcuts:")
        table_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(table_label)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Shorthand", "Expansion"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.update_table()
        layout.addWidget(self.table)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_profile_changed(self, profile_name):
        self.keyboard_controller.switch_profile(profile_name)
        self.update_table()

    def update_profiles(self):
        # Update profile list in combo box
        self.profile_combo.clear()
        profiles = self.keyboard_controller.get_profiles()
        self.profile_combo.addItems(profiles)

    def on_language_changed(self, new_language):
        self.keyboard_controller.input_language = new_language
        logging.info(f"Input language changed to: {new_language}")

    def update_table(self):
        # Get shortcuts from current profile
        shortcuts = self.keyboard_controller.profiles[self.keyboard_controller.current_profile]
        self.table.setRowCount(len(shortcuts))
        for i, (shorthand, expansion) in enumerate(shortcuts.items()):
            self.table.setItem(i, 0, QTableWidgetItem(shorthand))
            self.table.setItem(i, 1, QTableWidgetItem(expansion))
        # Resize columns to content
        self.table.resizeColumnsToContents()

    def add_shorthand(self):
        shorthand = self.shorthand_input.text().strip()
        expansion = self.expansion_input.text().strip()
        
        if shorthand and expansion:
            # Add to current profile
            current_profile = self.keyboard_controller.current_profile
            self.keyboard_controller.profiles[current_profile][shorthand] = expansion
            self.keyboard_controller.save_profiles()
            # Update the controller's shorthand map
            self.keyboard_controller.shorthand_map = self.keyboard_controller.profiles[current_profile]
            self.update_table()
            self.shorthand_input.clear()
            self.expansion_input.clear()

def main():
    try:
        app = QApplication(sys.argv)
        keyboard_controller = KeyboardController()
        window = MainWindow(keyboard_controller)
        window.show()
        keyboard_controller.start()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 