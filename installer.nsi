; installer.nsi – NSIS script for OnTrack
; Assumes you run this from your repo root,
; and that dist\OnTrack.exe exists.

; Output installer into build\
OutFile "build\OnTrack_Installer.exe"

; Default install directory
InstallDir "$PROGRAMFILES\OnTrack"

; Request normal user privileges
RequestExecutionLevel admin

; Pages
Page directory         ; choose install folder
Page instfiles         ; show install progress
UninstPage instfiles   ; show uninstall progress

; --- Install Section ---
Section "Install"
  
  ; Fail if EXE is missing
  IfFileExists "dist\OnTrack.exe" +2
    Abort "ERROR: dist\OnTrack.exe not found. Run build.bat first."

  ; Copy the EXE
  SetOutPath "$INSTDIR"
  File "dist\OnTrack.exe"

  ; Write the uninstaller into the same folder
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Start Menu shortcut
  CreateDirectory "$SMPROGRAMS\OnTrack"
  CreateShortcut "$SMPROGRAMS\OnTrack\OnTrack.lnk" "$INSTDIR\OnTrack.exe"

  ; Desktop shortcut
  CreateShortcut "$DESKTOP\OnTrack.lnk" "$INSTDIR\OnTrack.exe"

SectionEnd

; --- Uninstall Section ---
Section "Uninstall"
  ; Remove installed files
  Delete "$INSTDIR\OnTrack.exe"
  Delete "$INSTDIR\Uninstall.exe"

  ; Remove shortcuts
  Delete "$DESKTOP\OnTrack.lnk"
  Delete "$SMPROGRAMS\OnTrack\OnTrack.lnk"

  ; Remove directories
  RMDir "$SMPROGRAMS\OnTrack"
  RMDir "$INSTDIR"
SectionEnd
