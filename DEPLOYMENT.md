# S3 Bucket Viewer - Deployment Guide

## Quick Start

The standalone executable `S3BucketViewer.exe` is ready to run on Windows systems without requiring Python installation.

### Running the Application

1. **Locate the executable**: `dist/S3BucketViewer.exe`
2. **Double-click to run** or execute from command line
3. **Enter your AWS credentials** in the first window
4. **Browse and download files** from your S3 bucket

## Distribution

The `S3BucketViewer.exe` file is completely self-contained and can be distributed to end users. No additional files or dependencies are required.

### System Requirements
- Windows 7 or higher
- No Python installation required
- Internet connection for AWS S3 access
- Minimum 50MB free disk space

## Development Setup

If you want to modify or rebuild the application:

### Prerequisites
- Python 3.7+ installed
- Virtual environment (recommended)

### Installation Steps

1. **Clone/download the project**
2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
3. **Test the application**:
   ```
   python test_app.py
   ```
4. **Run from source**:
   ```
   python s3_bucket_viewer.py
   ```

### Building the Executable

#### Option 1: Use the build script
```
python build.py
```

#### Option 2: Use the batch file (Windows)
```
build.bat
```

#### Option 3: Manual PyInstaller command
```
pip install pyinstaller
pyinstaller --onefile --windowed --name=S3BucketViewer s3_bucket_viewer.py
```

The executable will be created in the `dist/` folder.

## AWS Setup Guide

### Creating AWS Credentials

1. **Sign in to AWS Console**
2. **Go to IAM (Identity and Access Management)**
3. **Create a new user**:
   - Choose "Programmatic access"
   - No AWS Management Console access needed
4. **Set permissions**:
   - Attach existing policy: `AmazonS3ReadOnlyAccess`
   - Or create custom policy with minimal permissions
5. **Save credentials**:
   - Access Key ID
   - Secret Access Key

### Minimal IAM Policy

For security, create a custom policy with minimal permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

Replace `your-bucket-name` with your actual S3 bucket name.

## Application Features

### Page 1: Credential Input
- Secure credential entry with masked password field
- Region selection (defaults to us-east-1)
- Optional resource prefix filtering
- Connection validation with detailed error messages

### Page 2: File Browser
- Scrollable file list with file sizes and modification dates
- Multi-select functionality with checkboxes
- Select All/Deselect All buttons
- Two download options:
  - Individual file downloads
  - ZIP archive creation for multiple files
- Progress indicators during downloads
- Destination folder selection

## Troubleshooting

### Common Issues

1. **"Invalid AWS credentials"**
   - Verify Access Key ID and Secret Access Key
   - Check IAM user permissions

2. **"Bucket does not exist"**
   - Confirm bucket name spelling (case-sensitive)
   - Verify bucket region

3. **"Access denied"**
   - Check IAM permissions
   - Verify bucket policy

4. **Download failures**
   - Check internet connection
   - Verify file permissions in destination folder
   - Ensure sufficient disk space

### Getting Help

1. **Check the AWS IAM console** for user permissions
2. **Verify bucket exists** in the AWS S3 console
3. **Try a different region** if connection fails
4. **Check your internet connection** and firewall settings

## Security Notes

- Credentials are only stored in memory during the session
- No credentials are saved to disk or configuration files
- Secret keys are masked in the user interface
- Use IAM policies with minimal required permissions
- Consider using AWS STS temporary credentials for enhanced security

## File Structure

```
S3BucketViewer/
├── dist/
│   └── S3BucketViewer.exe          # Standalone executable
├── build/                          # PyInstaller build files
├── s3_bucket_viewer.py            # Main application source
├── requirements.txt               # Python dependencies
├── LICENSE.txt                    # MIT License
├── README.md                      # User documentation
├── config.py                      # Configuration examples
├── test_app.py                   # Test suite
├── build.py                      # Build script
└── build.bat                     # Windows build script
```

## License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.
