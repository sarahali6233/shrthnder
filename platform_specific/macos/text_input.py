from Foundation import NSString, NSPasteboard
from AppKit import NSApplication, NSEvent, NSKeyUp, NSCommandKeyMask, NSStringPboardType
import Quartz
import time
import logging

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

class OptimizedMacTextInput:
    def __new__(cls):
        instance = super().__new__(cls)
        instance.__init__()
        return instance
        
    def __init__(self):
        self.logger = logging.getLogger('shrthnder')
        self.pasteboard = NSPasteboard.generalPasteboard()
        self.previous_content = None
        self.fallback = MacTextInput()
        
    def _save_clipboard(self):
        """Save current clipboard content."""
        self.previous_content = self.pasteboard.stringForType_(NSStringPboardType)
        
    def _restore_clipboard(self):
        """Restore previous clipboard content."""
        if self.previous_content is not None:
            self.pasteboard.clearContents()
            self.pasteboard.setString_forType_(self.previous_content, NSStringPboardType)
            
    @classmethod
    def delete_chars(cls, count):
        """Delete characters using optimized method."""
        instance = cls()
        try:
            # Create a sequence of backspace events
            events = []
            for _ in range(count):
                down_event = Quartz.CGEventCreateKeyboardEvent(None, 0x33, True)
                up_event = Quartz.CGEventCreateKeyboardEvent(None, 0x33, False)
                events.extend([down_event, up_event])
            
            # Post all events in rapid succession
            for event in events:
                Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
                
        except Exception as e:
            instance.logger.error(f"Error in optimized delete_chars: {e}")
            # Fallback to original implementation
            instance.fallback.delete_chars(count)
            
    @classmethod
    def insert_text(cls, text):
        """Insert text using clipboard for better performance."""
        instance = cls()
        try:
            # Save current clipboard
            instance._save_clipboard()
            
            # Set new text to clipboard
            instance.pasteboard.clearContents()
            instance.pasteboard.setString_forType_(text, NSStringPboardType)
            
            # Simulate Cmd+V
            time.sleep(0.01)  # Small delay to ensure clipboard is ready
            
            # Create Command key down event
            cmd_down = Quartz.CGEventCreateKeyboardEvent(None, 0x37, True)
            Quartz.CGEventSetFlags(cmd_down, NSCommandKeyMask)
            
            # Create 'v' key events
            v_down = Quartz.CGEventCreateKeyboardEvent(None, 0x09, True)
            v_up = Quartz.CGEventCreateKeyboardEvent(None, 0x09, False)
            cmd_up = Quartz.CGEventCreateKeyboardEvent(None, 0x37, False)
            
            # Set command flag for 'v' events
            Quartz.CGEventSetFlags(v_down, NSCommandKeyMask)
            Quartz.CGEventSetFlags(v_up, NSCommandKeyMask)
            
            # Post events in sequence
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, cmd_down)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, v_down)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, v_up)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, cmd_up)
            
            time.sleep(0.01)  # Small delay to ensure paste completes
            
            # Restore previous clipboard content
            instance._restore_clipboard()
            
        except Exception as e:
            instance.logger.error(f"Error in optimized insert_text: {e}")
            # Fallback to original implementation
            instance.fallback.insert_text(text) 