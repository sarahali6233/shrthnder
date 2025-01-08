import platform
import sys

class TextInputFactory:
    @staticmethod
    def get_text_input():
        system = platform.system().lower()
        
        if system == 'darwin':
            from .macos.text_input import MacTextInput
            return MacTextInput
        elif system == 'windows':
            from .windows.text_input import WindowsTextInput
            return WindowsTextInput
        elif system == 'linux':
            from .linux.text_input import LinuxTextInput
            return LinuxTextInput
        else:
            raise NotImplementedError(f"Platform {system} is not supported") 