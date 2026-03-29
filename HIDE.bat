@echo off
chcp 65001 > nul 2>&1
title USB Security Tool - Hide Files

set "DIR=%~dp0"

echo.
echo  Hiding system files...
echo.

attrib +h +s "%DIR%python"
attrib +h +s "%DIR%Lib"
attrib +h +s "%DIR%pendrive_cripto.py"
attrib +h +s "%DIR%SETUP.bat"
attrib +h +s "%DIR%usb.bat"
attrib +h +s "%DIR%LEIA-ME.txt"
attrib +h +s "%DIR%HIDE.bat"

echo  Done! All files are now hidden.
echo.
echo  To show files again, run SHOW.bat
echo  or: attrib -h -s "E:\filename"
echo.
pause
