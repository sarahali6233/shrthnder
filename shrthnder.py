import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QHBoxLayout, QComboBox, QInputDialog, QMessageBox, QFileDialog, QTimer
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
from platform_specific.window_detection_factory import WindowDetectionFactory
from keyboard_layouts import LayoutManager as KbLayoutManager
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class KeyboardLayoutManager:
    def __init__(self):
        system_locale = locale.getdefaultlocale()[0]
        self.layout = "qwertz" if system_locale and system_locale.startswith('de') else "qwerty"
        self.logger = logging.getLogger('shrthnder')
        self.layout_manager = KbLayoutManager(self.layout)
        # Physical keyboard mapping for common special characters
        self.physical_to_qwerty = {
            # German QWERTZ to QWERTY
            'z': 'y', 'y': 'z', 'ü': '[', 'ä': "'", 'ö': ';', 'ß': ']',
            # Keep QWERTY mappings as is
            'q': 'q', 'w': 'w', 'e': 'e', 'r': 'r', 't': 't', 'u': 'u',
            'i': 'i', 'o': 'o', 'p': 'p', 'a': 'a', 's': 's', 'd': 'd',
            'f': 'f', 'g': 'g', 'h': 'h', 'j': 'j', 'k': 'k', 'l': 'l',
            'x': 'x', 'c': 'c', 'v': 'v', 'b': 'b', 'n': 'n', 'm': 'm',
            # Special characters that need mapping
            ',': ',', '.': '.', '/': '/', '-': '/',
            # Shifted special characters
            ':': '.', '_': '/', ';': ',', '<': ',', '>': '.'
        }

    def get_char(self, key):
        try:
            # Handle special keys
            if hasattr(key, 'char') and key.char:
                # First map the physical key to its QWERTY position
                char = key.char.lower()
                qwerty_pos = self.physical_to_qwerty.get(char, char)
                
                # Then transform that position according to the selected layout
                result = self.layout_manager.transform_text(qwerty_pos)
                
                # Preserve original case
                return result.upper() if key.char.isupper() else result
            
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

    def transform_text(self, text):
        """Wrapper method to transform text using the layout manager."""
        return self.layout_manager.transform_text(text)

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
        self.window_detection = WindowDetectionFactory.get_window_detection()
        self.last_key_time = 0
        self.key_cooldown = 0.05  # 50ms cooldown between key presses
        self.current_app = "unknown"
        self.app_categories = {
            "code_editors": ["Visual Studio Code", "PyCharm", "Sublime Text", "Atom"],
            "browsers": ["Google Chrome", "Safari", "Firefox", "Microsoft Edge"],
            "word_processors": ["Microsoft Word", "Pages", "LibreOffice"],
            "terminals": ["Terminal", "iTerm", "Command Prompt"]
        }

    def setup_logger(self):
        logger = logging.getLogger('shrthnder')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def get_current_app_category(self):
        """Get the category of the currently active application."""
        try:
            self.current_app = self.window_detection.get_active_window()
            for category, apps in self.app_categories.items():
                if self.current_app in apps:
                    return category
            return "global"
        except Exception as e:
            self.logger.error(f"Error getting app category: {e}")
            return "global"

    def process_dynamic_content(self, expansion):
        """Process any dynamic content in the expansion string."""
        try:
            # Replace date/time placeholders
            if "{date}" in expansion:
                expansion = expansion.replace("{date}", datetime.now().strftime("%Y-%m-%d"))
            if "{time}" in expansion:
                expansion = expansion.replace("{time}", datetime.now().strftime("%H:%M"))
            
            # Get current app category for context-specific processing
            app_category = self.get_current_app_category()
            
            # Add context-specific processing
            if app_category == "code_editors":
                if "{fn}" in expansion:
                    expansion = expansion.replace("{fn}", "function")
                if "{cl}" in expansion:
                    expansion = expansion.replace("{cl}", "class")
            
            return expansion
        except Exception as e:
            self.logger.error(f"Error processing dynamic content: {e}")
            return expansion

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

        # Default profiles with context-aware shortcuts
        profiles = {
            "Default": {
                "global": {
                    "btw": "by the way",
                    "idk": "I don't know",
                    "omw": "on my way",
                    "date": "{date}",
                    "time": "{time}"
                },
                "code_editors": {
                    "fn": "function {name}() {\n    \n}",
                    "cl": "class {name} {\n    constructor() {\n        \n    }\n}",
                    "imp": "import {module} from '{path}'",
                    "log": "console.log({message})",
                    "pr": "print({message})"
                },
                "browsers": {
                    "email": "user@example.com",
                    "gh": "https://github.com/",
                    "so": "https://stackoverflow.com/"
                },
                "word_processors": {
                    "heading1": "# Heading 1",
                    "cite": "[Citation needed]",
                    "draft": "DRAFT - {date}"
                }
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
        # Stop any existing listener before starting a new one
        self.stop()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()
        self.logger.info(f"Started keyboard listener with {self.layout_manager.layout} layout")

    def stop(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
            self.logger.info("Stopped keyboard listener")

    def on_press(self, key):
        try:
            # Implement key press cooldown to prevent multiple transformations
            current_time = time.time()
            if current_time - self.last_key_time < self.key_cooldown:
                return
            self.last_key_time = current_time

            # If space is pressed, check for expansion
            if key == Key.space:
                if self.current_word.lower() in self.profiles[self.current_profile]:
                    self.check_and_expand()
                self.current_word = ""  # Reset current word
                return

            # Only process character keys
            if hasattr(key, 'char') and key.char:
                char = key.char
                transformed_char = char
                
                # Get the current layout
                layout = self.layout_manager.layout
                layout_map = self.layout_manager.layout_manager.current_layout
                
                # First map the physical key to its QWERTY position
                qwerty_pos = self.layout_manager.physical_to_qwerty.get(char.lower(), char.lower())
                
                # Special handling for QWERTY/QWERTZ y/z swap
                if layout == "qwerty":
                    if char.lower() == 'y':
                        self.text_input.delete_chars(1)
                        transformed_char = 'z' if char.islower() else 'Z'
                        self.text_input.insert_text(transformed_char)
                    elif char.lower() == 'z':
                        self.text_input.delete_chars(1)
                        transformed_char = 'y' if char.islower() else 'Y'
                        self.text_input.insert_text(transformed_char)
                # For QWERTZ, no transformation needed
                elif layout == "qwertz":
                    transformed_char = char
                # For all other layouts (AdNW, CMOS, Dvorak, etc.)
                else:
                    # Get the character that should be typed in this position
                    transformed = layout_map.get(qwerty_pos, qwerty_pos)
                    if transformed != char:
                        self.text_input.delete_chars(1)
                        # Respect original case for all characters
                        transformed_char = transformed.upper() if char.isupper() else transformed.lower()
                        self.text_input.insert_text(transformed_char)
                
                # Add the character to current word
                self.current_word += transformed_char
                self.logger.info(f"Key pressed: {char}, transformed to: {transformed_char} (Layout: {layout})")
                
        except Exception as e:
            self.logger.error(f"Error in on_press: {e}")

    def check_and_expand(self):
        if not self.current_word:
            return

        try:
            # Get current app category
            app_category = self.get_current_app_category()
            
            # Check app-specific shortcuts first
            expansion = None
            if app_category in self.profiles[self.current_profile]:
                expansion = self.profiles[self.current_profile][app_category].get(self.current_word.lower())
            
            # If no app-specific shortcut found, try global shortcuts
            if not expansion and "global" in self.profiles[self.current_profile]:
                expansion = self.profiles[self.current_profile]["global"].get(self.current_word.lower())
            
            if expansion:
                # Process any dynamic content
                expansion = self.process_dynamic_content(expansion)
                
                # Transform based on current layout
                transformed_expansion = self.layout_manager.transform_text(expansion)
                
                # Delete the original text plus space
                self.text_input.delete_chars(len(self.current_word) + 1)
                
                # Insert the expanded text
                self.text_input.insert_text(transformed_expansion + " ")
                
                self.logger.info(f"Expanded '{self.current_word}' to '{expansion}' in {app_category}")
                
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
        
        # Start context update timer
        self.context_timer = QTimer()
        self.context_timer.timeout.connect(self.update_context_indicator)
        self.context_timer.start(1000)  # Update every second

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
        language_label = QLabel("Keyboard Layout:")
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "German (QWERTZ)",
            "English (QWERTY)",
            "German (AdNW)",
            "German (CMOS)",
            "Programming (Dvorak)",
            "Programming (Colemak)",
            "Programming (Workman)",
            "Hamlak"
        ])
        # Set default based on current language
        default_layout = "English (QWERTY)" if self.keyboard_controller.input_language == "English" else "German (QWERTZ)"
        self.language_combo.setCurrentText(default_layout)
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        language_group.addWidget(language_label)
        language_group.addWidget(self.language_combo)
        settings_layout.addLayout(language_group)
        
        # Add context selector
        context_group = QVBoxLayout()
        context_label = QLabel("Context:")
        self.context_combo = QComboBox()
        self.context_combo.addItems(["global"] + list(self.keyboard_controller.app_categories.keys()))
        self.context_combo.currentTextChanged.connect(self.on_context_changed)
        
        # Add context indicator
        self.context_indicator = QLabel("Current Context: global")
        self.context_indicator.setStyleSheet("color: #666; font-style: italic;")
        
        context_group.addWidget(context_label)
        context_group.addWidget(self.context_combo)
        context_group.addWidget(self.context_indicator)
        settings_layout.addLayout(context_group)
        
        # Update shorthand section
        shorthand_layout = QVBoxLayout()
        shorthand_label = QLabel("Add Custom Shorthand:")
        shorthand_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        
        self.shorthand_input = QLineEdit()
        self.shorthand_input.setPlaceholderText("Enter shorthand (e.g., btw)")
        
        self.expansion_input = QLineEdit()
        self.expansion_input.setPlaceholderText("Enter expansion (e.g., by the way)")
        
        # Add dynamic content helper
        dynamic_helper = QLabel("Available placeholders: {date}, {time}, {name}, {message}, {module}, {path}")
        dynamic_helper.setStyleSheet("color: #666; font-size: 12px;")
        
        add_button = QPushButton("Add Shorthand")
        add_button.clicked.connect(self.add_shorthand)
        
        shorthand_layout.addWidget(shorthand_label)
        shorthand_layout.addWidget(self.shorthand_input)
        shorthand_layout.addWidget(self.expansion_input)
        shorthand_layout.addWidget(dynamic_helper)
        shorthand_layout.addWidget(add_button)
        layout.addLayout(shorthand_layout)
        
        # Table for shorthand rules
        table_label = QLabel("Available Shortcuts:")
        table_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(table_label)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Context", "Shorthand", "Expansion"])
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

    def on_language_changed(self, new_layout):
        # Map layout names to language and layout settings
        layout_map = {
            "English (QWERTY)": ("English", "qwerty"),
            "German (QWERTZ)": ("German", "qwertz"),
            "German (AdNW)": ("German", "adnw"),
            "German (CMOS)": ("German", "cmos"),
            "Programming (Dvorak)": ("English", "programmer_dvorak"),
            "Programming (Colemak)": ("English", "colemak_mod_dh"),
            "Programming (Workman)": ("English", "workman"),
            "Hamlak": ("English", "hamlak")
        }
        
        # Get language and layout from the map
        language, layout = layout_map.get(new_layout, ("English", "qwerty"))
        
        # Update language (for compatibility with existing code)
        self.keyboard_controller.input_language = language
        # Update layout
        self.keyboard_controller.layout_manager.layout = layout
        # Update layout manager
        self.keyboard_controller.layout_manager.layout_manager = KbLayoutManager(layout)
        
        logging.info(f"Changed to {new_layout} (Language: {language}, Layout: {layout})")

    def update_table(self):
        """Update the shortcuts table with context-aware information."""
        current_profile = self.keyboard_controller.current_profile
        selected_context = self.context_combo.currentText()
        
        # Get shortcuts for the current profile
        shortcuts = []
        profile_data = self.keyboard_controller.profiles[current_profile]
        
        if selected_context == "global":
            # Show shortcuts from all contexts
            for context, context_shortcuts in profile_data.items():
                for shorthand, expansion in context_shortcuts.items():
                    shortcuts.append((context, shorthand, expansion))
        else:
            # Show only shortcuts for the selected context
            if selected_context in profile_data:
                context_shortcuts = profile_data[selected_context]
                for shorthand, expansion in context_shortcuts.items():
                    shortcuts.append((selected_context, shorthand, expansion))
        
        # Update table
        self.table.setRowCount(len(shortcuts))
        for i, (context, shorthand, expansion) in enumerate(shortcuts):
            self.table.setItem(i, 0, QTableWidgetItem(context))
            self.table.setItem(i, 1, QTableWidgetItem(shorthand))
            self.table.setItem(i, 2, QTableWidgetItem(expansion))
        
        # Resize columns to content
        self.table.resizeColumnsToContents()

    def add_shorthand(self):
        """Add a new shorthand with context awareness."""
        shorthand = self.shorthand_input.text().strip()
        expansion = self.expansion_input.text().strip()
        context = self.context_combo.currentText()
        
        if shorthand and expansion:
            # Add to current profile under the selected context
            current_profile = self.keyboard_controller.current_profile
            
            # Initialize context dictionary if it doesn't exist
            if context not in self.keyboard_controller.profiles[current_profile]:
                self.keyboard_controller.profiles[current_profile][context] = {}
            
            # Add the shorthand
            self.keyboard_controller.profiles[current_profile][context][shorthand] = expansion
            self.keyboard_controller.save_profiles()
            
            # Update the table
            self.update_table()
            
            # Clear input fields
            self.shorthand_input.clear()
            self.expansion_input.clear()

    def update_context_indicator(self):
        """Update the context indicator with the current application context."""
        current_context = self.keyboard_controller.get_current_app_category()
        current_app = self.keyboard_controller.current_app
        self.context_indicator.setText(f"Current Context: {current_context} ({current_app})")

    def on_context_changed(self, context):
        """Handle context selection change."""
        self.update_table()

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