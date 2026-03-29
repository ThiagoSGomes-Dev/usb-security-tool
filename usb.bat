@echo off
chcp 65001 > nul 2>&1
title USB Security Tool

set "SCRIPT_DIR=%~dp0"
set "PYTHON=%SCRIPT_DIR%python\python.exe"
set "SCRIPT=%SCRIPT_DIR%pendrive_cripto.py"
set "LIBS=%SCRIPT_DIR%Lib\site-packages"

if not exist "%PYTHON%" (
    echo.
    echo  ERROR: portable Python not found!
    echo  make sure the "python\" folder exists.
    echo.
    pause
    exit /b
)

if not exist "%SCRIPT%" (
    echo.
    echo  ERROR: script pendrive_cripto.py not found!
    echo.
    pause
    exit /b
)

set "PYTHONPATH=%LIBS%"

REM Pass all arguments quoted to handle paths with spaces
"%PYTHON%" "%SCRIPT%" %*

pause
