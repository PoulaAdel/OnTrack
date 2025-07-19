; installer.nsi – NSIS script for WorkflowTimer
; Assumes you run this from your repo root,
; and that dist\WorkflowTimer.exe exists.

; Output installer into build\
OutFile "build\WorkflowTimer_Installer.exe"

; Default install directory
InstallDir "$PROGRAMFILES\WorkflowTimer"

; Request normal user privileges
RequestExecutionLevel user

; Pages
Page directory         ; choose install folder
Page instfiles         ; show install progress
UninstPage instfiles   ; show uninstall progress

; --- Install Section ---
Section "Install"
  
  ; Fail if EXE is missing
  IfFileExists "dist\WorkflowTimer.exe" +2
    Abort "ERROR: dist\WorkflowTimer.exe not found. Run build.bat first."

  ; Copy the EXE
  SetOutPath "$INSTDIR"
  File "dist\WorkflowTimer.exe"

  ; Write the uninstaller into the same folder
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Start Menu shortcut
  CreateDirectory "$SMPROGRAMS\WorkflowTimer"
  CreateShortcut "$SMPROGRAMS\WorkflowTimer\WorkflowTimer.lnk" "$INSTDIR\WorkflowTimer.exe"

  ; Desktop shortcut
  CreateShortcut "$DESKTOP\WorkflowTimer.lnk" "$INSTDIR\WorkflowTimer.exe"

SectionEnd

; --- Uninstall Section ---
Section "Uninstall"
  ; Remove installed files
  Delete "$INSTDIR\WorkflowTimer.exe"
  Delete "$INSTDIR\Uninstall.exe"

  ; Remove shortcuts
  Delete "$DESKTOP\WorkflowTimer.lnk"
  Delete "$SMPROGRAMS\WorkflowTimer\WorkflowTimer.lnk"

  ; Remove directories
  RMDir "$SMPROGRAMS\WorkflowTimer"
  RMDir "$INSTDIR"
SectionEnd
