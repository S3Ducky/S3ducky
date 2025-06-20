@echo off
echo S3Ducky - Build Script
echo =======================

echo Installing dependencies...
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo Building executable...
pyinstaller --onefile --windowed --name=S3Ducky --icon=asset/logo.png --add-data=asset;asset main.py

echo.
echo Build complete! Check the dist folder for S3Ducky.exe
pause
