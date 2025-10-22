@echo off
.\..\python\python.exe -X utf8 ".\..\main modul.py" createSours
:: Проверяем, вызван ли скрипт из другого файла
if "%~0" == "%~f0" (
    pause
)