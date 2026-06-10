@echo off
REM Build a Windows executable for Rhyme Generator
python -m pip install -r requirements.txt
python -m pip install pyinstaller
pyinstaller --windowed --onefile --name Rhymegenerator --add-data "images;images" --add-data "languages.json;." --add-data "loadwords.txt;." --add-data "settings.json;." main.py
echo.
echo Build complete.
echo If you used onefile, the executable is dist\Rhymegenerator.exe
echo If you used onedir, the folder is dist\Rhymegenerator
echo.
pause
