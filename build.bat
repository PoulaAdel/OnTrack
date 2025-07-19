@echo off
REM Install dependencies
pip install -r requirements.txt

REM Clean old builds
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist WorkflowTimer.spec del /q WorkflowTimer.spec

REM Bundle with PyInstaller
pyinstaller --name WorkflowTimer --onefile --windowed timer_app.py

echo.
echo Build complete. Executable is in dist\WorkflowTimer.exe
pause
