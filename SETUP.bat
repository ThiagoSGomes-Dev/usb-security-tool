@echo off
title USB Security Tool - Dependencies

set "USB=%~dp0"
set "PYTHON=%USB%python\python.exe"
set "PIP_SCRIPT=%USB%python\get-pip.py"
set "LIBS=%USB%Lib\site-packages"

echo.
echo  [setup] activating pip...

for %%f in ("%USB%python\python*._pth") do (
    powershell -Command "(Get-Content '%%f') -replace '#import site', 'import site' | Set-Content '%%f'"
)

if not exist "%PIP_SCRIPT%" (
    echo  [setup] downloading get-pip.py...
    powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%PIP_SCRIPT%'"
    if not exist "%PIP_SCRIPT%" (
        echo  ERROR: failed to download get-pip.py. Check your connection.
        pause
        exit /b 1
    )
)

if not exist "%LIBS%" mkdir "%LIBS%"

echo  [setup] installing pip...
"%PYTHON%" "%PIP_SCRIPT%" --no-warn-script-location >nul 2>&1

echo  [setup] installing cryptography...
"%PYTHON%" -m pip install cryptography --target="%LIBS%" --no-warn-script-location

if %errorlevel%==0 (
    echo  [setup] done.
) else (
    echo  ERROR: installation failed. Check your internet connection.
    pause
    exit /b 1
)
