Automated Data Extractor

A configurable command-line tool for automatically fetching and exporting structured data from web APIs or JSON endpoints.
The extracted data can be exported to multiple formats including .xlsx, .csv, and .json.

b8;

Features
	b
"	Command-line interface with interactive configuration.
	b
"	Supports multiple URLs or APIs in a single run.
	b
"	Automatically saves configuration for future use (config.json).
	b
"	Exports data to Excel (.xlsx), CSV, or JSON.
	b
"	Simple and offline-friendly b
ash: no: not found
	b
"	Designed for security, flexibility, and ease of automation.

b8;

Requirements

Before running the tool, ensure you have the following installed:
	b
"	Python 3.8+
	b
"	Pip (Python Package Manager)

Then install the required dependencies:
```bash

pip install requests pandas openpyxl

```

EXAMPLE
=====================================================
    AUTOMATED DATA EXTRACTOR b
 CONFIGURATION TOOL
=====================================================

Detected existing configuration file: config.json
Would you like to use it? (Y/n): y

Starting extraction process...
Processing: https://example.com
Processing: https://jsonplaceholder.typicode.com/users/1
Data exported to data_output_20251023_104113.xlsx

SUMMARY: 2 URLs processed | 1 successful | Process completed!

Notes
	b
"	Invalid or non-JSON URLs will be skipped automatically.
	b
"	Exported files are timestamped for version control.
	b
"	If you wish to reset saved settings, simply delete config.json.

b8;

Optional: Create a Standalone Executable

You can package the tool into an .exe or .app using PyInstaller:

```
pip install pyinstaller
pyinstaller --onefile main.py

```

The built file will appear under dist/.

b8;

License

This project is released under the MIT License.
You may freely modify, distribute, or use it for commercial purposes.
