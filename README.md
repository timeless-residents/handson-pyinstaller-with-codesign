# PyInstaller with Code Signing - Hands-on Tutorial

This repository demonstrates how to package a simple Python Tkinter application into a macOS DMG file using PyInstaller and dmgbuild, with optional code signing.

## Project Overview

This project includes:

- A simple Tkinter GUI application
- Configuration for PyInstaller to create a macOS app bundle
- Settings for dmgbuild to create a professional DMG installer
- GitHub Actions workflow for automated building
- Optional code signing support

## Prerequisites

- Python 3.12 or later
- macOS (for DMG creation and code signing)
- For code signing: Apple Developer account and valid certificate

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/handson-pyinstaller-with-codesign.git
   cd handson-pyinstaller-with-codesign
   ```

2. Install the required dependencies:
   ```
   pip install pyinstaller dmgbuild
   ```

## Running the Application

To run the application directly:

```
python main.py
```

## Building the Application

### Building the App Bundle with PyInstaller

```
pyinstaller --windowed --name "MyApp" main.py
```

This will create an app bundle in the `dist/` directory.

### Creating a DMG with dmgbuild

```
dmgbuild -s settings.py "My App" MyApp.dmg
```

## Code Signing (Optional)

To sign your application with your Apple Developer certificate:

1. Obtain a Developer ID Application certificate from Apple
2. Use the following command with PyInstaller:
   ```
   pyinstaller --windowed --name "MyApp" --codesign-identity "Developer ID Application: Your Name (XXXXXXXXXX)" main.py
   ```

## GitHub Actions Workflow

This repository includes a GitHub Actions workflow that automatically:

1. Sets up a macOS environment
2. Installs Python and dependencies
3. Builds the app bundle using PyInstaller
4. Creates a DMG file using dmgbuild
5. Creates GitHub Releases with the DMG file attached for easy downloading

The workflow runs on pushes to the main branch, pull requests, and when tags are pushed. The DMG file is made available through GitHub Releases in two scenarios:

- **Latest Build**: When code is pushed to the main branch, it creates or updates a "latest" release with the most recent DMG file.
- **Version Releases**: When a tag (e.g., v1.0.0) is pushed, it creates a standard release with that version.

You can download the DMG file directly from the Releases page of the repository:

```
https://github.com/<username>/<repository>/releases
```

### Creating a New Release Version

To create a new versioned release:

1. Tag your commit with a version number:
   ```
   git tag v1.0.0
   ```

2. Push the tag to GitHub:
   ```
   git push origin v1.0.0
   ```

The GitHub Actions workflow will automatically build the DMG and create a new release with the tag name.

## Configuration

### settings.py

The `settings.py` file contains configuration for the DMG creation, including:

- Volume name
- Window size and position
- Icon size
- Application placement within the DMG
- Optional background image
- Symbolic link to /Applications folder

You can customize these settings to match your branding and preferences.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
