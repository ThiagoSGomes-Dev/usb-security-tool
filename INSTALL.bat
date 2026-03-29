@echo off
title USB Security Tool - Install

set "USB=%~dp0"
set "DRIVE=%~d0"
set "LOCK=%USB%.installed"

echo.
echo  ====================================================
echo   USB SECURITY TOOL  ^|  INSTALL
echo  ====================================================
echo.

REM Already installed check
if exist "%LOCK%" (
    echo  INFO: This drive was already set up.
    echo.
    echo  [1] Reinstall
    echo  [2] Skip and open terminal
    echo  [0] Exit
    echo.
    set /p "CHOICE=  > "
    if "%CHOICE%"=="1" goto START
    if "%CHOICE%"=="2" goto OPEN_TERMINAL
    if "%CHOICE%"=="0" exit /b 0
    echo  Invalid option.
    pause
    exit /b 1
)

:START

REM 1. Check USB drive
echo  [1/4] Checking drive type...

for /f "tokens=2 delims==" %%i in ('wmic logicaldisk where "DeviceID='%DRIVE%'" get DriveType /value 2^>nul') do set "DTYPE=%%i"

if "%DTYPE%"=="2" (
    echo  OK - USB removable drive detected: %DRIVE%
) else (
    echo.
    echo  ERROR: must be run from a USB drive.
    echo  Drive %DRIVE% type is %DTYPE% - expected 2 ^(removable^).
    echo  Copy all files to your USB drive and run again.
    echo.
    pause
    exit /b 1
)

echo.

REM 2. Check portable Python
echo  [2/4] Checking portable Python...

if not exist "%USB%python\python.exe" (
    echo.
    echo  ERROR: python\ folder not found.
    echo  Download Windows embeddable package 64-bit:
    echo  https://www.python.org/downloads/windows/
    echo  Extract into the python\ folder on this drive.
    echo.
    pause
    exit /b 1
)

echo  OK - python\python.exe found.
echo.

REM 3. Install dependencies
echo  [3/4] Installing dependencies...
echo.

if exist "%USB%Lib\site-packages\cryptography" (
    echo  INFO: cryptography already installed. Skipping.
) else (
    call "%USB%SETUP.bat"
    if %errorlevel% neq 0 (
        echo.
        echo  ERROR: setup failed.
        pause
        exit /b 1
    )
)

echo.

REM 4. Hide system files
echo  [4/4] Hiding system files...

attrib +h +s "%USB%python"
attrib +h +s "%USB%Lib"
attrib +h +s "%USB%pendrive_cripto.py"
attrib +h +s "%USB%SETUP.bat"
attrib +h +s "%USB%usb.bat"
attrib +h +s "%USB%cmd_usb.bat"
attrib +h +s "%USB%HIDE.bat"
attrib +h +s "%USB%SHOW.bat"
attrib +h +s "%USB%LEIA-ME.txt"
attrib +h +s "%USB%INSTALL.bat"

echo  OK - all files hidden.

REM Create lock file
echo installed > "%LOCK%"
attrib +h +s "%LOCK%"

echo.
echo  ====================================================
echo   Done! Opening secure terminal...
echo  ====================================================
echo.

timeout /t 2 /nobreak >nul

:OPEN_TERMINAL
cmd /k "set PATH=%PATH%;%USB% && echo. && echo  USB drive ready. Type: usb --help && echo."
