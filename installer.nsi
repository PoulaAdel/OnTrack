; Installer script for WorkflowTimer
OutFile "dist\WorkflowTimer_Installer.exe"
InstallDir "$PROGRAMFILES\WorkflowTimer"
RequestExecutionLevel user

Page directory
Page instfiles

Section "Main"
  SetOutPath "$INSTDIR"
  File "dist\WorkflowTimer.exe"

  ; Start menu shortcut
  CreateDirectory "$SMPROGRAMS\WorkflowTimer"
  CreateShortcut "$SMPROGRAMS\WorkflowTimer\WorkflowTimer.lnk" "$INSTDIR\WorkflowTimer.exe"

  ; Desktop shortcut
  CreateShortcut "$DESKTOP\WorkflowTimer.lnk" "$INSTDIR\WorkflowTimer.exe"
SectionEnd
