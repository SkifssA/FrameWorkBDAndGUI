@echo off
.\..\python\python.exe -m pip install -r ".\requirements.txt" --no-warn-script-location
:: Проверяем, вызван ли скрипт из другого файла
if "%~0" == "%~f0" (
    pause
)