import subprocess
import time

class LinuxTextInput:
    @staticmethod
    def delete_chars(count):
        # Use xdotool to simulate backspace key presses
        for _ in range(count):
            subprocess.run(['xdotool', 'key', 'BackSpace'])
            time.sleep(0.01)  # Small delay to ensure proper key registration
        
    @staticmethod
    def insert_text(text):
        # Use xdotool to type the text
        subprocess.run(['xdotool', 'type', text]) 