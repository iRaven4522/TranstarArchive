@echo off
title TranstarArchive Looping Test (for Windows)
echo %cd%
set /p confirm=This will create a loop for archiving files from transtar, delayed every few minutes, are you sure?
if %confirm% == yes goto loop
if %confirm% == no goto :eof
goto :eof

:loop
echo Starting to loop @ %date% %time%
python.exe %cd%\main.py -archive
timeout 17
goto loop
