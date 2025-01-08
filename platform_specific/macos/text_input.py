from Foundation import NSString
from AppKit import NSApplication, NSEvent, NSKeyUp
import Quartz

class MacTextInput:
    @staticmethod
    def delete_chars(count):
        for _ in range(count):
            event = Quartz.CGEventCreateKeyboardEvent(None, 0x33, True)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateKeyboardEvent(None, 0x33, False))
        
    @staticmethod
    def insert_text(text):
        # Create keyboard events for each character
        for char in text:
            # Regular character input
            event = Quartz.CGEventCreateKeyboardEvent(None, 0, True)
            Quartz.CGEventKeyboardSetUnicodeString(event, len(char), chr(ord(char)))
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateKeyboardEvent(None, 0, False)) 