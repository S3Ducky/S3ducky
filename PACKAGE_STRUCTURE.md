# S3Ducky - Package Structure Documentation

## Overview
S3Ducky has been refactored from a monolithic script into a well-structured Python package for improved maintainability, readability, and modularity.

## Package Structure

```
s3ducky/
├── __init__.py                 # Package initialization and main exports
├── app.py                      # Main application controller
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── s3_client.py           # S3 connection and operations
│   └── file_manager.py        # File download and management
├── gui/                        # User interface components
│   ├── __init__.py
│   ├── main_window.py         # Main window manager
│   ├── credentials_page.py    # AWS credentials input page
│   ├── file_browser.py        # File browsing and selection page
│   └── footer.py              # Footer component with links
└── utils/                      # Utility functions
    ├── __init__.py
    ├── formatters.py          # File size formatting utilities
    └── image_utils.py         # Image loading and icon utilities
```

## Module Descriptions

### Core Modules (`s3ducky/core/`)

#### `s3_client.py`
- **Purpose**: Handles all S3 connection and basic operations
- **Key Features**:
  - Connection management with credentials validation
  - Bucket access testing
  - Object listing with pagination support
  - Single file download operations
  - Connection state management

#### `file_manager.py`
- **Purpose**: Manages file download operations and bulk operations
- **Key Features**:
  - Individual file downloads
  - Batch file downloads as ZIP archives
  - Asynchronous download operations
  - Progress tracking and callbacks

### GUI Modules (`s3ducky/gui/`)

#### `main_window.py`
- **Purpose**: Main window container and page management
- **Key Features**:
  - Root window setup and configuration
  - Page switching and navigation
  - Icon and branding management
  - Key binding management

#### `credentials_page.py`
- **Purpose**: AWS credentials input interface
- **Key Features**:
  - Credential form inputs (Access Key, Secret Key, Region, Bucket, Prefix)
  - Input validation and user feedback
  - Logo display and branding
  - Connection status updates

#### `file_browser.py`
- **Purpose**: File browsing and selection interface
- **Key Features**:
  - Tree view for file listing with columns (Serial No., Select, Name, Size, Modified)
  - File selection management (individual, select all, deselect all)
  - Download operation triggers
  - Progress and status display

#### `footer.py`
- **Purpose**: Footer component with links and branding
- **Key Features**:
  - Clickable GitHub repository link
  - MIT License link
  - Copyright information

### Utility Modules (`s3ducky/utils/`)

#### `formatters.py`
- **Purpose**: Data formatting utilities
- **Key Features**:
  - Human-readable file size formatting (B, KB, MB, GB, TB)

#### `image_utils.py`
- **Purpose**: Image handling and icon management
- **Key Features**:
  - PNG image loading with PIL support
  - Application icon setting
  - Image resizing for UI components
  - Graceful fallback when PIL unavailable

### Main Application (`s3ducky/app.py`)

The main application controller that orchestrates all components:
- **Purpose**: Central application logic and flow control
- **Key Features**:
  - Page navigation management
  - S3 connection coordination
  - Error handling and user feedback
  - Asynchronous operation management
  - Event binding and callback handling

## Entry Points

### `main.py`
The primary entry point for the application:
```python
from s3ducky import S3DuckyApp

def main():
    app = S3DuckyApp()
    app.run()
```

### Legacy Entry Point
The original `s3_bucket_viewer.py` is preserved for compatibility but should be considered deprecated.

## Build Configuration

### Updated Build Scripts
- **`build.py`**: Updated to use `main.py` as entry point
- **`build.bat`**: Updated batch script for Windows builds
- **`S3Ducky.spec`**: Updated PyInstaller specification file

### Build Process
```bash
# Using Python script
python build.py

# Using batch file (Windows)
build.bat

# Manual PyInstaller command
pyinstaller --onefile --windowed --name=S3Ducky --icon=asset/logo.png --add-data=asset;asset main.py
```

## Advantages of the New Structure

### 1. **Separation of Concerns**
- **Core logic** (S3 operations) separated from **UI components**
- **Utilities** are modular and reusable
- **Business logic** is independent of presentation layer

### 2. **Maintainability**
- Smaller, focused files are easier to understand and modify
- Clear module boundaries reduce coupling
- Bug fixes and features can be isolated to specific modules

### 3. **Testability**
- Individual components can be unit tested in isolation
- Mock objects can easily replace dependencies
- Core logic can be tested without GUI dependencies

### 4. **Extensibility**
- New GUI components can be added without affecting core logic
- Additional S3 operations can be added to the core modules
- New utility functions can be added without code duplication

### 5. **Reusability**
- Core S3 operations can be reused in other applications
- GUI components can be reused for similar applications
- Utilities are generic and broadly applicable

## Migration Notes

### From Monolithic Structure
The refactoring maintains full backward compatibility:
- All existing functionality is preserved
- Build process produces the same executable
- User interface and behavior remain identical
- Asset files (logo.png) work without changes

### Import Changes
With the new package structure, components can be imported individually:
```python
# Import the main application
from s3ducky import S3DuckyApp

# Import specific components
from s3ducky.core import S3Client, FileManager
from s3ducky.gui import MainWindow, CredentialsPage
from s3ducky.utils import format_file_size, load_png_image
```

## Development Workflow

### Running the Application
```bash
# Run from source
python main.py

# Or run the package directly
python -m s3ducky
```

### Testing Individual Components
```python
# Test S3 client
from s3ducky.core import S3Client
client = S3Client()

# Test utilities
from s3ducky.utils import format_file_size
print(format_file_size(1024))  # Output: "1.0 KB"
```

### Adding New Features
1. **Core functionality**: Add to appropriate module in `s3ducky/core/`
2. **UI components**: Add to `s3ducky/gui/`
3. **Utilities**: Add to `s3ducky/utils/`
4. **Update imports**: Add to relevant `__init__.py` files

## Future Enhancements

The modular structure enables easy implementation of:
- **Plugin system**: Additional S3 operations as plugins
- **Multiple cloud providers**: Azure Blob, Google Cloud Storage
- **Advanced UI features**: Progress bars, file previews
- **Configuration management**: Settings persistence
- **Logging system**: Comprehensive error and debug logging
- **Testing framework**: Comprehensive unit and integration tests

This refactored structure provides a solid foundation for continued development and maintenance of S3Ducky.
