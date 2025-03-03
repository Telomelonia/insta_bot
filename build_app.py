import PyInstaller.__main__
import os
import shutil

# Define app details
APP_NAME = "InstagramAccountManager"
ICON_FILE = "instagram_icon.ico"  # You'll need to find/create this icon file

# Clean build directories
for dir_name in ["build", "dist"]:
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

# Create a simple script to download the icon if it doesn't exist
if not os.path.exists(ICON_FILE):
    import requests
    print("Downloading Instagram icon...")
    response = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png", stream=True)
    from PIL import Image
    import io
    # Convert PNG to ICO
    img = Image.open(io.BytesIO(response.content))
    img.save(ICON_FILE)

# Create the executable
PyInstaller.__main__.run([
    'instagram_bot.py',
    '--name=%s' % APP_NAME,
    '--onefile',
    '--windowed',
    '--icon=%s' % ICON_FILE,
    '--add-data=%s;.' % ICON_FILE,
    '--hidden-import=bs4',
    '--hidden-import=selenium',
    '--hidden-import=webdriver_manager'
])

print(f"Build complete! Executable is in the 'dist' folder: dist/{APP_NAME}.exe")