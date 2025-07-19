@echo off
setlocal

echo.
echo === Installing/Updating Dependencies ===
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller

echo.
echo === Cleaning Previous Builds ===
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist WorkflowTimer.spec del /q WorkflowTimer.spec

echo.
echo === Building Standalone Executable ===
pyinstaller --noconfirm --onefile --windowed ^
    --name WorkflowTimer ^
    --distpath dist ^
    --workpath build ^
    --specpath build ^
    timer_app.py

if %errorlevel% neq 0 (
  echo PyInstaller build failed!
  pause
  exit /b %errorlevel%
)

echo.
echo === Creating Windows Installer ===
if not exist build mkdir build
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi

if %errorlevel% neq 0 (
  echo NSIS installer build failed!
  pause
  exit /b %errorlevel%
)

echo.
echo === Build Complete ===
echo Executable: dist\WorkflowTimer.exe
echo Installer: build\WorkflowTimer_Installer.exe
pause
