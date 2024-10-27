@echo off
echo Downloading and installing wget...

:: Download wget
powershell -Command "Invoke-WebRequest -Uri http://eternallybored.org/misc/wget/current/wget.exe -OutFile wget.exe"

:: Create directory if it doesn't exist
if not exist "C:\Program Files\GnuWin32\bin" (
    mkdir "C:\Program Files\GnuWin32\bin"
)

:: Install wget
echo Installing wget...
move wget.exe "C:\Program Files\GnuWin32\bin"

:: Variables
set server=https://raw.githubusercontent.com/Gallogeta/MCS/main
set filename=tenor.gif

:: Download file using wget with no certificate check
echo Downloading %filename% from %server%...
"C:\Program Files\GnuWin32\bin\wget.exe" %server%/%filename% --no-check-certificate -O C:\Users\Public\%filename%

:: Confirmation message
if exist C:\Users\Public\%filename% (
    echo Download completed!
) else (
    echo Download failed.
    exit
)

:: Set variables
set source=C:\Users\Public\%filename%
set destination=C:\Users\Public

:: Loop to copy the file 5 times
for /l %%i in (1, 1, 5) do (
    copy "%source%" "%destination%\tenor_copy%%i.gif"
)

:: Open all copied files using PowerShell
powershell -Command "Start-Process 'C:\Users\Public\tenor_copy1.gif'"
powershell -Command "Start-Process 'C:\Users\Public\tenor_copy2.gif'"
powershell -Command "Start-Process 'C:\Users\Public\tenor_copy3.gif'"
powershell -Command "Start-Process 'C:\Users\Public\tenor_copy4.gif'"
powershell -Command "Start-Process 'C:\Users\Public\tenor_copy5.gif'"

:: Close Command Prompt
exit
