import platform

class WindowDetectionFactory:
    @staticmethod
    def get_window_detection():
        """Get the appropriate window detection class for the current platform."""
        system = platform.system().lower()
        
        if system == 'darwin':
            from .macos.window_detection import MacWindowDetection
            return MacWindowDetection
        elif system == 'windows':
            from .windows.window_detection import WindowsWindowDetection
            return WindowsWindowDetection
        elif system == 'linux':
            from .linux.window_detection import LinuxWindowDetection
            return LinuxWindowDetection
        else:
            raise NotImplementedError(f"Platform {system} is not supported") 