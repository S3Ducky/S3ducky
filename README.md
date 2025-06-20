# S3 Bucket Viewer

<p align="center">
  <img src="asset/logo.png" alt="S3Ducky Logo" width="120"/>
</p>

A Windows desktop application for browsing and downloading files from AWS S3 buckets.

## Features

- **Secure Credential Input**: Enter AWS credentials securely with masked secret key input
- **S3 Bucket Browsing**: View all files in your S3 bucket with file sizes and modification dates
- **Multi-file Selection**: Select individual files or use Select All/Deselect All functionality
- **Flexible Downloads**: 
  - Download individual files to a chosen directory
  - Download multiple files as a compressed ZIP archive
- **Error Handling**: Comprehensive error handling for AWS connectivity and credential issues
- **User-friendly Interface**: Clean, intuitive Tkinter-based GUI

## Requirements

- Python 3.7 or higher
- AWS S3 credentials (Access Key, Secret Key)
- Internet connection

## Installation

A. Executable Installation (Recommended)
1. **Clone or download this repository**
2. Open a terminal or command prompt at the S3Ducky folder
3. Run the command:
   ```
   python build.py
   ```
   On windows, you can also double click on build.bat to build the executable.
   
B. Local Installation (from source)
1. **Clone or download this repository**
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running from Source
```
python s3_bucket_viewer.py
```

### Building Standalone Executable

1. **Install PyInstaller:**
   ```
   pip install pyinstaller
   ```

2. **Build the executable:**
   ```
   pyinstaller --onefile s3_bucket_viewer.py
   ```

3. **Find the executable in the `dist` folder**

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
