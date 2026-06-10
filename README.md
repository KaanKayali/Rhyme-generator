# Rhyme Generator

Rhyme Generator is a small Python desktop app for finding rhyming words from custom text or PDF word lists.
It uses `tkinter` for the user interface and `PyPDF2` to extract words from PDFs.

> **Note:** The rhyme matching logic is designed for German word endings. The English option only changes the user interface language.

## What it does
- Finds rhyming words from a user-provided list
- Supports plain text and PDF files
- Offers multiple rhyme modes
- Saves settings and your word list automatically
- Includes a light/dark interface toggle

## Requirements
- Windows
- Python 3.9 or newer
- `tkinter` (included with standard Python on Windows)
- `PyPDF2`

## Setup
1. Open PowerShell in the project folder.
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run from source
```powershell
python main.py
```

## Build a Windows executable
You can build the app with PyInstaller. The executable name will be `Rhymegenerator.exe`.

Install PyInstaller if you do not already have it:
```powershell
python -m pip install pyinstaller
```

Then run one of these commands:

- One-folder build (`dist\Rhymegenerator\Rhymegenerator.exe`):
  ```powershell
  pyinstaller --windowed --onedir --name Rhymegenerator --add-data "images;images" --add-data "languages.json;." --add-data "loadwords.txt;." --add-data "settings.json;." main.py
  ```

- Single-file build (`dist\Rhymegenerator.exe`):
  ```powershell
  pyinstaller --windowed --onefile --name Rhymegenerator --add-data "images;images" --add-data "languages.json;." --add-data "loadwords.txt;." --add-data "settings.json;." main.py
  ```

> If the app is built as a single file, user settings and word data are stored automatically in `%APPDATA%\Rhymegenerator`.

## Build helper
A helper script is included:
- `build_windows.bat`

Run it from the project root to install requirements and build the executable.

## Files and folders
- `main.py` — application source code
- `images/` — icon assets for light/dark toggle
- `languages.json` — UI text for German/English
- `loadwords.txt` — default word list data
- `settings.json` — default settings
- `requirements.txt` — runtime dependency list

## Usage
1. Start the app by running `python main.py` or by launching `dist\Rhymegenerator.exe`.
2. Type a word or phrase into the text field.
3. Select a rhyme mode.
4. Add a `.txt` or `.pdf` word list using `Add a list (txt/PDF)`.
5. Optionally enable `Perfect rhyme` or `Additional words`.

### Add words
Click `Add a list (txt/PDF)` and select one or more text or PDF files. The app extracts plain words automatically, so the file does not need a special format.

### Additional words
When `Additional words` is enabled, the app may combine multiple words to produce rhyme candidates instead of only showing single-word results.

### Rhyme modes
- **Classic rhyme**: matches words with identical endings.
- **Vowel rhyme**: matches words with the same vowel sequence.
- **Vowel rhyme + consonant ending**: matches words with the same vowel sequence and the same ending sound.

Classic rhyme is usually best for poems. For rap-style results, the looser vowel rhyme mode often produces more usable matches.

### Perfect rhyme
When `Perfect rhyme` is turned off, the app treats `e` and `i` as equivalent, and `u` and `o` as equivalent. This lets the app return broader rhyme matches.

## Troubleshooting
- If the app cannot open `images/sun.png`, rebuild using the exact PyInstaller command above with `--add-data`.
- If PDF extraction fails, make sure the PDF contains selectable text.
- If you see no rhymes, add more words to `loadwords.txt` or import a larger word list.

## License
This project is proprietary. Unauthorized copying, modification, or distribution is strictly prohibited.
