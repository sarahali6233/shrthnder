from AppKit import NSWorkspace

class MacWindowDetection:
    @staticmethod
    def get_active_window():
        """Get the currently active application name on macOS."""
        try:
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.activeApplication()
            return active_app['NSApplicationName']
        except Exception as e:
            print(f"Error getting active window: {e}")
            return "unknown" 