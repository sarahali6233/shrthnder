# Shrthnder

A cross-platform text expansion tool that automatically expands your shorthand text into full phrases as you type.

## Requirements

- Python 3.8 or higher
- Platform-specific requirements:
  - **macOS**: macOS 11+ (Big Sur or newer)
  - **Windows**: Windows 10+
  - **Linux**: X11 desktop environment

## Installation and Setup

### Windows Setup

1. Open PowerShell as Administrator (right-click PowerShell and select "Run as Administrator")

2. Clone this repository:
```powershell
git clone https://github.com/sarahali6233/shrthnder.git
cd shrthnder
```

3. Create a new virtual environment:
```powershell
python -m venv venv
```

4. Allow PowerShell to run activation scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

5. Install pip in the virtual environment:
```powershell
.\venv\Scripts\python.exe -m ensurepip --upgrade
```

6. Install required packages:
```powershell
.\venv\Scripts\python.exe -m pip install PyQt5 pynput keyboard pyautogui pywin32
```

7. Run shrthnder:
```powershell
.\venv\Scripts\python.exe shrthnder.py
```

Important Notes:
- Always run PowerShell as Administrator when using shrthnder
- Allow any security prompts that appear
- Keep the GUI window open (you can minimize it) for the text expansion to work
- If you encounter any issues, check the Troubleshooting section below

### macOS Setup

1. Clone this repository:
```bash
git clone https://github.com/sarahali6233/shrthnder.git
cd shrthnder
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Grant Accessibility Permissions:
   - Go to System Settings > Privacy & Security > Accessibility
   - Click the lock icon to make changes (requires password)
   - Click the + button
   - Navigate to and add your Terminal app (or IDE if running from there)
   - Ensure the checkbox next to the added application is checked

5. Run the application:
```bash
python3 shrthnder.py
```

### Linux Setup

1. Clone this repository:
```bash
git clone https://github.com/sarahali6233/shrthnder.git
cd shrthnder
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install system dependencies:
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev python3-xlib xdotool

# For Fedora
sudo dnf install python3-devel python3-xlib xdotool

# For Arch Linux
sudo pacman -S python-xlib xdotool
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python3 shrthnder.py
```

## Usage

1. The application will start with a GUI window and begin listening for keyboard input globally.

2. Default shortcuts:
   - "btw" → "by the way"
   - "idk" → "I don't know"
   - "omw" → "on my way"

3. To add new shortcuts:
   - Enter the shorthand in the first text field
   - Enter the expansion in the second text field
   - Click "Add Shorthand"

4. To use shortcuts:
   - Simply type the shorthand followed by a space
   - The shorthand will automatically expand to the full text

5. Profiles:
   - Switch between different profiles for different contexts (Default, Developer, Medical, etc.)
   - Create new profiles for your specific needs
   - Each profile has its own set of shortcuts

## Troubleshooting

### Windows Issues

1. If keyboard events aren't being captured:
   - Verify PowerShell is running as Administrator
   - Check Windows Security settings
   - Disable any conflicting keyboard monitoring software
   - Make sure pywin32 is installed correctly: `.\venv\Scripts\python.exe -m pip show pywin32`

2. If text expansion isn't working:
   - Verify the GUI window is still running (can be minimized)
   - Check if any antivirus software is blocking keyboard monitoring
   - Try running from a different PowerShell window (as Administrator)

### macOS Issues

1. If keyboard events aren't being captured:
   - Check System Settings > Privacy & Security > Accessibility
   - Ensure your terminal/IDE has permissions
   - Try running from a different terminal
   - Log out and log back in after granting permissions

2. If text expansion isn't working:
   - Make sure you're using macOS 11 (Big Sur) or newer
   - Check if any other text expansion tools are running
   - Try running the application from a different terminal

### Linux Issues

1. If keyboard events aren't being captured:
   - Verify xdotool is installed: `which xdotool`
   - Check if X11 is running: `echo $DISPLAY`
   - Try running with sudo (not recommended for regular use)
   - Make sure you have necessary permissions

2. If text expansion isn't working:
   - Check if your desktop environment supports X11
   - Verify python-xlib is installed: `pip show python-xlib`
   - Try running from a different terminal

### General Issues

1. If the application doesn't start:
   - Verify Python version: `python --version`
   - Check all dependencies are installed: `pip list`
   - Look for error messages in the terminal

2. If shortcuts aren't working:
   - Check if the application is running (look for the GUI window)
   - Verify the shortcut exists in your current profile
   - Try adding a new shortcut to test functionality

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
