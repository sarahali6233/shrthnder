# Shrthnder

A cross-platform text expansion tool that automatically expands your shorthand text into full phrases as you type.

## Requirements

- Python 3.8 or higher
- macOS 11+ or Windows 10+

## Installation

1. Clone this repository:

```bash
git clone https://github.com/sarahali6233/shrthnder.git
cd shrthnder
```

2. Create a virtual environment (recommended):

**For macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup & Running

### macOS Setup

1. Grant Accessibility Permissions:

   - Go to System Settings > Privacy & Security > Accessibility
   - Click the lock icon to make changes (requires password)
   - Click the + button
   - Navigate to and add your Terminal app (or IDE if running from there)
   - Ensure the checkbox next to the added application is checked

2. Run the application:

```bash
python3 shrthnder.py
```

### Windows Setup

1. Run as Administrator (first time):

   - Right-click your terminal or IDE
   - Select "Run as Administrator"
   - This gives the application necessary permissions for keyboard monitoring

2. Run the application:

```bash
python shrthnder.py
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
   - Simply type the shorthand followed by a space, period, or other punctuation
   - The shorthand will automatically expand to the full text

## Troubleshooting

### macOS Issues

1. If keyboard events aren't being captured:
   - Check System Settings > Privacy & Security > Accessibility
   - Ensure your terminal/IDE has permissions
   - Try running from a different terminal
   - Log out and log back in after granting permissions

### Windows Issues

1. If keyboard events aren't being captured:

   - Run the terminal/IDE as Administrator
   - Check Windows Security settings
   - Disable any conflicting keyboard monitoring software

2. If text expansion isn't working:
   - Check if any antivirus software is blocking keyboard monitoring
   - Try running from a different terminal or IDE

### General Issues

1. If the application doesn't work:
   - Ensure you've granted necessary permissions
   - Check that no other applications are capturing keyboard events
   - Verify that your Python environment is properly set up
   - Make sure all dependencies are installed correctly
