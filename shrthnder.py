import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from pynput import keyboard
import pyautogui
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class ShrthnderUI(QMainWindow):
    def __init__(self, keyboard_controller):
        super().__init__()
        self.keyboard_controller = keyboard_controller
        self.shorthand_map = self.load_shortcuts()
        self.setup_ui()
        
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
            
    def setup_ui(self):
        self.setWindowTitle("Shrthnder - Typing Efficiency Tool")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Status label
        self.status_label = QLabel("Shrthnder is running...")
        layout.addWidget(self.status_label)
        
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
        
    def add_shorthand(self):
        shorthand = self.shorthand_input.text().strip()
        expansion = self.expansion_input.text().strip()
        
        if shorthand and expansion:
            self.shorthand_map[shorthand] = expansion
            self.save_shortcuts()
            self.update_table()
            self.shorthand_input.clear()
            self.expansion_input.clear()
            
    def update_table(self):
        self.table.setRowCount(len(self.shorthand_map))
        for i, (shorthand, expansion) in enumerate(self.shorthand_map.items()):
            self.table.setItem(i, 0, QTableWidgetItem(shorthand))
            self.table.setItem(i, 1, QTableWidgetItem(expansion))

class KeyboardController:
    def __init__(self):
        self.current_word = ""
        self.shorthand_map = {}
        self.load_shortcuts()
        logging.info(f"Initialized KeyboardController with shortcuts: {self.shorthand_map}")
        
    def load_shortcuts(self):
        if os.path.exists('shortcuts.json'):
            with open('shortcuts.json', 'r') as f:
                self.shorthand_map = json.load(f)
                logging.info(f"Loaded shortcuts from file: {self.shorthand_map}")
        else:
            self.shorthand_map = {
                "btw": "by the way",
                "idk": "I don't know",
                "omw": "on my way"
            }
            logging.info(f"Using default shortcuts: {self.shorthand_map}")
    
    def on_press(self, key):
        try:
            if hasattr(key, 'char'):
                if key.char.isalpha():
                    self.current_word += key.char
                    logging.info(f"Current word buffer: {self.current_word}")
                elif key.char in [' ', '.', ',', '!', '?']:
                    logging.info(f"Punctuation detected: {key.char}, checking word: {self.current_word}")
                    self.process_word()
        except AttributeError:
            if key == keyboard.Key.space:
                logging.info(f"Space key detected, checking word: {self.current_word}")
                self.process_word()
            elif key == keyboard.Key.enter:
                logging.info(f"Enter key detected, checking word: {self.current_word}")
                self.process_word()

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
            
            # Type the expansion
            expansion = self.shorthand_map[self.current_word.lower()]
            logging.info(f"Expanding to: {expansion}")
            pyautogui.write(expansion)
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