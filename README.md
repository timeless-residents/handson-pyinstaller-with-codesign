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

## Code Signing and Notarization

To ensure your application can be opened on macOS without security warnings, you need to sign and notarize it. The GitHub Actions workflow supports automatic code signing and notarization if you provide the necessary secrets.

### Setting Up GitHub Secrets for Code Signing

#### 1. Obtain a Developer ID Application Certificate

1. Enroll in the [Apple Developer Program](https://developer.apple.com/programs/) if you haven't already
2. Go to your [Apple Developer Account](https://developer.apple.com/account/)
3. Navigate to "Certificates, Identifiers & Profiles" > "Certificates"
4. Click the "+" button to create a new certificate
5. Select "Developer ID Application" and follow the instructions
6. Download the certificate and double-click to install it in your Keychain

#### 2. Export the Certificate as a .p12 File

1. Open Keychain Access on your Mac
2. Find your Developer ID Application certificate (it should include your private key)
3. Right-click on the certificate and select "Export"
4. Choose the .p12 format and set a strong password
5. Save the file to a secure location

#### 3. Base64 Encode the Certificate

```bash
base64 -i path/to/certificate.p12 | pbcopy
```

This command encodes the certificate and copies it to your clipboard.

To verify the encoding worked correctly, you can paste it into a file and decode it:

```bash
# Paste the encoded content into a file
pbpaste > encoded_cert.txt

# Decode it to verify it's valid
base64 -d encoded_cert.txt > decoded_cert.p12

# Compare the file sizes - they should be identical
ls -l path/to/certificate.p12 decoded_cert.p12
```

#### 4. Set Up GitHub Secrets

In your GitHub repository:
1. Go to "Settings" > "Secrets and variables" > "Actions"
2. Add the following secrets:

| Secret Name | Description | How to Obtain |
|-------------|-------------|---------------|
| `APPLE_CERTIFICATE_BASE64` | Base64-encoded .p12 certificate | From step 3 above |
| `APPLE_CERTIFICATE_PASSWORD` | Password for the .p12 certificate | Password you set when exporting the certificate |
| `KEYCHAIN_PASSWORD` | Password for the temporary keychain | Create any secure string |
| `APPLE_ID` | Your Apple ID email | Your Apple Developer account email |
| `APPLE_ID_PASSWORD` | App-specific password | Generate from [appleid.apple.com](https://appleid.apple.com) under "Security" > "App-Specific Passwords" |
| `APPLE_TEAM_ID` | Your Apple Developer Team ID | Found in your [Developer Account](https://developer.apple.com/account) (it's a 10-character string) |

#### 5. Verify Your Setup

To verify your certificate is valid for code signing:

```bash
# List identities that can be used for code signing
security find-identity -v -p codesigning

# You should see your Developer ID Application certificate in the list
```

### Manual Code Signing and Notarization

If you want to sign and notarize the application locally, follow these steps:

#### 1. Build and Sign the Application

```bash
# Build the app with code signing
pyinstaller --windowed --name "MyApp" --codesign-identity "Developer ID Application: Your Name (XXXXXXXXXX)" main.py
```

To verify the app is properly signed:

```bash
# Verify code signature
codesign -dv --verbose=2 dist/MyApp.app

# Verify Gatekeeper acceptance
spctl -a -t exec -vv dist/MyApp.app
```

#### 2. Create a DMG

```bash
# Create the DMG
dmgbuild -s settings.py "My App" MyApp.dmg
```

#### 3. Notarize the DMG

```bash
# Create a ZIP archive of the DMG for notarization
ditto -c -k --keepParent MyApp.dmg MyApp.zip

# Submit for notarization
xcrun notarytool submit MyApp.zip --apple-id "your.email@example.com" --password "app-specific-password" --team-id "TEAMID" --wait

# Alternatively, you can submit and get a request ID
REQUEST_ID=$(xcrun notarytool submit MyApp.zip --apple-id "your.email@example.com" --password "app-specific-password" --team-id "TEAMID" | grep "id:" | awk '{print $2}')

# Check status later
xcrun notarytool info $REQUEST_ID --apple-id "your.email@example.com" --password "app-specific-password" --team-id "TEAMID"
```

#### 4. Staple the Notarization Ticket

Once notarization is complete, staple the ticket to the DMG:

```bash
xcrun stapler staple MyApp.dmg

# Verify stapling
xcrun stapler validate MyApp.dmg
```

#### 5. Troubleshooting

If notarization fails, you can get detailed logs:

```bash
# Get the log URL from the notarization info
LOG_URL=$(xcrun notarytool info $REQUEST_ID --apple-id "your.email@example.com" --password "app-specific-password" --team-id "TEAMID" | grep "LogFileURL:" | awk '{print $2}')

# Download and view the log
curl -O $LOG_URL
```

Common issues include:
- Missing entitlements
- Hardened runtime issues
- Unsigned frameworks or libraries
- Invalid code signatures

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
https://github.com/timeless-residents/handson-pyinstaller-with-codesign/releases
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
