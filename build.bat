@echo off
setlocal

echo.
echo === Installing/Updating Dependencies ===
py -m pip install --upgrade pip
py -m pip install -r requirements.txt pyinstaller

echo.
echo === Cleaning Previous Builds ===
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist OnTrack.spec del /q OnTrack.spec

echo.
echo === Building Standalone Executable ===
pyinstaller --noconfirm --onefile --windowed ^
    --name OnTrack ^
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
echo Executable: dist\OnTrack.exe
echo Installer: build\OnTrack_Installer.exe
pause
