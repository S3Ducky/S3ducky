# S3Ducky

A modern Windows desktop application for browsing and downloading files from AWS S3 buckets with an intuitive GUI.

## Disclaimer
This project is not affiliated with or endorsed by Amazon Web Services, Inc. (AWS). It is an independent application developed for educational and personal use. Use at your own risk.

## Features

- **Secure Credential Input**: Enter AWS credentials securely with masked secret key input
- **S3 Bucket Browsing**: View all files in your S3 bucket with file sizes and modification dates
- **Prefix Filtering**: Filter files by prefix to narrow down your search
- **Multi-file Selection**: Select individual files or use Select All/Deselect All functionality
- **Flexible Downloads**: 
  - Download individual files to a chosen directory
  - Download multiple files as a compressed ZIP archive
- **Error Handling**: Comprehensive error handling for AWS connectivity and credential issues
- **Modern UI**: Clean, intuitive interface with logo branding and clickable footer links
- **Modular Architecture**: Well-structured package design for maintainability and extensibility

## Requirements

- Python 3.7 or higher
- AWS S3 credentials (Access Key, Secret Key)
- Internet connection
- Optional: Pillow (PIL) for PNG logo support

## Installation

1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running from Source

**Option 1: Using the main entry point**
```bash
python main.py
```

**Option 2: Running as a module**
```bash
python -m s3ducky
```

**Option 3: Legacy method (deprecated)**
```bash
python s3_bucket_viewer.py
```

### Building Standalone Executable

**Automated build (recommended):**
```bash
python build.py
```

**Windows batch script:**
```bash
build.bat
```

**Manual PyInstaller command:**
```bash
pyinstaller --onefile --windowed --name=S3Ducky --icon=asset/logo.png --add-data=asset;asset main.py
```

The executable will be created in the `dist` folder as `S3Ducky.exe`.

## Application Workflow

### Page 1: Credential Input
1. Enter your AWS Access Key
2. Enter your AWS Secret Key (masked for security)
3. Specify the AWS Region (defaults to us-east-1)
4. Enter the S3 Bucket Name
5. Optionally specify a Resource prefix to filter files
6. Click "Connect" to validate credentials and connect to S3

### Page 2: File Browser
1. View all files in the connected S3 bucket
2. Use checkboxes to select files for download
3. Use "Select All" or "Deselect All" for bulk operations
4. Choose download option:
   - **Download Selected**: Downloads files individually to a chosen folder
   - **Download as Zip**: Creates a ZIP archive of selected files
5. Use "← Back to Credentials" to return to the first page

## Security Notes

- Credentials are only stored in memory during the session
- Secret keys are masked in the input field
- No credentials are saved to disk

## Error Handling

The application handles various error scenarios:
- Invalid AWS credentials
- Non-existent S3 buckets
- Network connectivity issues
- Access permission problems
- File download failures

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Dependencies

- **boto3**: AWS SDK for Python
- **tkinter**: GUI framework (included with Python)
- **zipfile**: Archive creation (included with Python)
- **threading**: Background operations (included with Python)

## System Requirements

- Windows 7 or higher
- Python 3.7+
- Minimum 100MB free disk space
- Internet connection for AWS S3 access

## Package Structure

S3Ducky follows a modular package structure for better maintainability:

```
s3ducky/
├── __init__.py              # Package initialization
├── __main__.py              # Module entry point
├── app.py                   # Main application controller
├── core/                    # Core business logic
│   ├── s3_client.py        # S3 connection and operations
│   └── file_manager.py     # File download management
├── gui/                     # User interface components
│   ├── main_window.py      # Main window manager
│   ├── credentials_page.py # Credentials input page
│   ├── file_browser.py     # File browsing page
│   └── footer.py           # Footer component
└── utils/                   # Utility functions
    ├── formatters.py       # Data formatting utilities
    └── image_utils.py      # Image and icon utilities
```

For detailed information about the package structure, see [PACKAGE_STRUCTURE.md](PACKAGE_STRUCTURE.md).
