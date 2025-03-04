# Instagram Account Manager

A tool to analyze your Instagram data export file and identify follow requests and non-followers.

## Features

- Import and analyze Instagram data export files
- View pending follow requests
- Identify users who don't follow you back
- Open user profiles directly in your browser

## Installation & Usage

You have two options to install the Instagram Account Manager:

### Option 1: Download Pre-built Executable (Windows Only)

1. Download the latest release from the [Releases](https://github.com/YourUsername/InstagramAccountManager/releases) page
2. Extract the ZIP file
3. Double-click on `InstagramAccountManager.exe` to run the application

### Option 2: Run the Installation Script

If you prefer to build the application yourself or are on Mac/Linux:

1. Make sure you have [Python 3.6+](https://www.python.org/downloads/) installed
2. Download `install.py` from this repository
3. Run the script:
   ```
   python install.py
   ```
4. The installer will:
   - Install all required dependencies
   - Download the project files
   - Build the application
   - Place the executable on your desktop

## How to Use

1. **Export your Instagram data**:

   - Log into Instagram in a web browser
   - Go to Settings > Privacy and Security > Data Download
   - Request a download in HTML format (not JSON)
   - Wait for the email from Instagram and download your data

2. **Analyze your data**:

   - Open the Instagram Account Manager application
   - Click "Browse" and select your Instagram data ZIP file
   - Click "Import Data"
   - The application will extract and analyze your data

3. **View your data**:
   - Use the "Follow Requests" tab to see pending follow requests
   - Use the "Non-Followers" tab to see users who don't follow you back
   - Click on any URL to open the user's profile in your browser

## Requirements

If you're running from source code:

- Python 3.6+
- BeautifulSoup4
- tkinter (usually comes with Python)

## FAQ

**Q: Is my Instagram data safe?**
A: Yes, the application runs locally on your computer and does not send your data anywhere. It only reads the data files you provide.

**Q: Why does the application need an Instagram data export?**
A: Instagram does not provide a public API to access this information. Using your data export is the most reliable way to analyze your account.

**Q: How often should I update my data?**
A: Instagram data exports only provide a snapshot of your account. For the most current information, request a new data export from Instagram.

## Troubleshooting

If you encounter any issues:

1. Make sure you've downloaded your Instagram data in HTML format (not JSON)
2. Check that your ZIP file is not corrupted
3. Ensure you have sufficient disk space for extraction

For more help, please [open an issue](https://github.com/YourUsername/InstagramAccountManager/issues) on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
