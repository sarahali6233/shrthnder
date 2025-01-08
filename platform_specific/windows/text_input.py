import win32api
import win32con
import time

class WindowsTextInput:
    @staticmethod
    def delete_chars(count):
        for _ in range(count):
            # Simulate backspace key press
            win32api.keybd_event(win32con.VK_BACK, 0, 0, 0)  # Press
            win32api.keybd_event(win32con.VK_BACK, 0, win32con.KEYEVENTF_KEYUP, 0)  # Release
            time.sleep(0.01)  # Small delay to ensure proper key registration
        
    @staticmethod
    def insert_text(text):
        for char in text:
            # Get virtual key code and scan code for the character
            vk = win32api.VkKeyScan(char)
            if vk == -1:
                continue  # Skip characters that can't be typed

            # Extract virtual key code and shift state
            vk_code = vk & 0xFF
            shift_state = (vk >> 8) & 0xFF

            # Press shift if needed
            if shift_state & 1:
                win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)

            # Press and release the key
            win32api.keybd_event(vk_code, 0, 0, 0)
            win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)

            # Release shift if it was pressed
            if shift_state & 1:
                win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)

            time.sleep(0.01)  # Small delay to ensure proper key registration 