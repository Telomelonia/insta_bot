@echo off
echo Building Instagram Account Manager...

rem Install PyInstaller if not already installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

rem Clean previous build files
if exist build (
    echo Cleaning build directory...
    rmdir /s /q build
)
if exist dist (
    echo Cleaning dist directory...
    rmdir /s /q dist
)

rem Build the executable
echo Building executable...
pyinstaller --name=InstagramAccountManager --onefile --noconsole --clean --noconfirm instagram_manager/main.py

echo Build completed!
echo Executable is located at: %CD%\dist\InstagramAccountManager.exe
pause