@echo off
:: Batch script to run PowerShell script as administrator
set script_path=C:\Users\vboxuser\Desktop\powerskriptv1.ps1

:: Check if running as administrator
openfiles >nul 2>nul
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
 
:: Run PowerShell script as administrator
powershell -Command "Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File %script_path%' -Verb RunAs"
