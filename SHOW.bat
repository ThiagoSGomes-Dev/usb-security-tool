@echo off
chcp 65001 > nul 2>&1
title USB Security Tool - Show Files

set "DIR=%~dp0"

echo.
echo  Restoring file visibility...
echo.

attrib -h -s "%DIR%python"
attrib -h -s "%DIR%Lib"
attrib -h -s "%DIR%pendrive_cripto.py"
attrib -h -s "%DIR%SETUP.bat"
attrib -h -s "%DIR%usb.bat"
attrib -h -s "%DIR%LEIA-ME.txt"
attrib -h -s "%DIR%HIDE.bat"
attrib -h -s "%DIR%SHOW.bat"

echo  Done! All files are visible again.
echo.
pause
