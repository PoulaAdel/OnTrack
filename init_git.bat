@echo off
REM ------------------------------------------------------------------
REM git_init.bat  – Initialize Git repo for OnScreenTimer project
REM ------------------------------------------------------------------

echo.
echo == Checking for existing Git repository ==
if not exist .git (
    echo Initializing new Git repository...
    git init
) else (
    echo Git repository already initialized.
)

echo.
echo == Configuring remote origin ==
git remote remove origin 2>nul
git remote add origin https://github.com/PoulaAdel/OnScreenTimer.git

echo.
echo == Creating & switching to 'main' branch ==
git branch -M main

echo.
echo == Staging all files ==
git add .

echo.
echo == Creating initial commit ==
git commit -m "Initial project setup"

echo.
echo == Pushing to remote 'origin' ==
git push -u origin main

echo.
echo Repository setup complete!
pause
