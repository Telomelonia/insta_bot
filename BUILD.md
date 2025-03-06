# Building the Instagram Account Manager Application

This guide explains how to build the Instagram Account Manager application into a standalone executable (.exe) file that can be distributed and run on Windows systems without Python installed.

## Prerequisites

1. Python 3.6 or later installed
2. The Instagram Account Manager source code
3. (Optional) A custom icon file (.ico format)

## Installation

First, make sure you have the required packages installed:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

## Building the Application

### Using the build_app.py Script

The easiest way to build the application is to use the provided `build_app.py` script:

1. Open a command prompt in the project root directory
2. Run the build script:

```bash
python build_app.py
```

This will create a single executable file at `dist/InstagramAccountManager.exe`.

### Build Options

The `build_app.py` script supports several command-line options:

- `--dir`: Create a directory with multiple files instead of a single executable
- `--console`: Show a console window when the application runs (useful for debugging)
- `--icon=PATH`: Specify a custom icon file for the executable
- `--skip-cleanup`: Don't clean up previous build files before building

Examples:

```bash
# Build with a custom icon
python build_app.py --icon=resources/instagram_icon.ico

# Build with console window for debugging
python build_app.py --console

# Build as a directory instead of single file
python build_app.py --dir
```

## Manual Building with PyInstaller

If you prefer to use PyInstaller directly:

```bash
pyinstaller --name=InstagramAccountManager --onefile --noconsole --clean --noconfirm instagram_manager/main.py
```

## After Building

1. The executable file will be in the `dist` directory
2. You can distribute this file to users who don't have Python installed
3. Double-click the executable to run the application

## Troubleshooting

If you encounter issues with the built application:

1. Try building with the `--console` option to see error messages
2. Ensure all required data files are included by specifying them in the PyInstaller command
3. If there are missing DLLs, you may need to add them explicitly with the `--add-binary` PyInstaller option

## Including Resources

If your application uses additional resource files:

1. Create a `resources` directory in the project root
2. Place your resources there (like icon files, etc.)
3. The build script will automatically include this directory in the build
