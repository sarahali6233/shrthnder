# Shrthnder

A cross-platform text expansion tool that automatically expands your shorthand text into full phrases as you type.

## Requirements

- Python 3.8 or higher
- macOS 11+ or Windows 10+

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/shrthnder.git
cd shrthnder
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python shrthnder.py
```

2. The application will start with a GUI window and begin listening for keyboard input globally.

3. Default shortcuts:

   - "btw" → "by the way"
   - "idk" → "I don't know"
   - "omw" → "on my way"

4. To add new shortcuts:

   - Enter the shorthand in the first text field
   - Enter the expansion in the second text field
   - Click "Add Shorthand"

5. To use shortcuts:
   - Simply type the shorthand followed by a space, period, or other punctuation
   - The shorthand will automatically expand to the full text

## Note for macOS Users

On macOS, you'll need to grant accessibility permissions to the terminal or IDE you're using to run the application:

1. Go to System Preferences > Security & Privacy > Privacy > Accessibility
2. Click the lock icon to make changes
3. Add your terminal application or IDE to the list
4. Ensure it's checked

## Troubleshooting

If the application doesn't work:

1. Ensure you've granted necessary permissions
2. Try running the terminal/IDE as administrator
3. Check that no other applications are capturing keyboard events
