@echo off
chcp 65001 > nul 2>&1
title USB Security Tool

set "USB=%~dp0"
set "PATH=%PATH%;%USB%"

echo.
echo  USB drive ready. Command available: usb
echo  Type "usb --help" for usage.
echo.

cmd /k
