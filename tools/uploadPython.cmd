@echo off
chcp 65001 >nul
setlocal

REM ============ НАСТРОЙКИ ============
set "PYTHON_VERSION=3.13.0"
set "ARCH=amd64"
set "PYTHON_DIR=.\..\python"
set "ZIP_FILE=python-%PYTHON_VERSION%-embed-%ARCH%.zip"
set "GET_PIP=get-pip.py"

REM ============ ССЫЛКИ ============
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%ZIP_FILE%"
set "GET_PIP_URL=https://bootstrap.pypa.io/get-pip.py"

REM ============ 1. Скачать Python embed ============
echo [1/6] Скачивание Portable Python %PYTHON_VERSION%...
curl -L -H "User-Agent: Mozilla/5.0" -o "%ZIP_FILE%" "%PYTHON_URL%"
if errorlevel 1 (
    echo Ошибка при скачивании Python.
    pause
    exit /b 1
)

REM ============ 2. Распаковать Python ============
echo [2/6] Распаковка архива...
mkdir "%PYTHON_DIR%" >nul 2>&1
tar -xf "%ZIP_FILE%" -C "%PYTHON_DIR%"
if errorlevel 1 (
    echo Ошибка распаковки. Пробуем через PowerShell...
    powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%PYTHON_DIR%'"
    if errorlevel 1 (
        echo Не удалось распаковать архив.
        pause
        exit /b 1
    )
)

REM ============ 3. Скачать get-pip.py ============
echo [3/6] Скачивание get-pip.py...
curl -L -H "User-Agent: Mozilla/5.0" -o "%GET_PIP%" "%GET_PIP_URL%"
if errorlevel 1 (
    echo Ошибка при скачивании get-pip.py.
    pause
    exit /b 1
)

REM ============ 4. Настроить pythonXXX._pth ============
REM Извлекаем первые 3 цифры версии: 3.13.0 → 313
for /f "delims=. tokens=1,2,3" %%a in ("%PYTHON_VERSION%") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
    set "PATCH=%%c"
)
set "VERSION_NUM=%MAJOR%%MINOR%"

echo [4/6] Настройка python%VERSION_NUM%._pth...
set "PTH_FILE=%PYTHON_DIR%\python%VERSION_NUM%._pth"

if exist "%PTH_FILE%" (
    echo Найден файл: %PTH_FILE%
    REM Раскомментируем строку 'import site'
    powershell -Command "(Get-Content '%PTH_FILE%') -replace '^#(import site)', 'import site' | Set-Content '%PTH_FILE%-tmp'"
    move /Y "%PTH_FILE%-tmp" "%PTH_FILE%" >nul
    echo Готово: раскомментировано 'import site'.
) else (
    echo Файл .pth не найден — создаём новый: %PTH_FILE%
    echo import site > "%PTH_FILE%"
    echo Lib >> "%PTH_FILE%"
    echo . >> "%PTH_FILE%"
)

REM Показываем содержимое для диагностики
echo Содержимое %PTH_FILE%:
type "%PTH_FILE%"

REM ============ 5. Установить pip ============
echo [5/6] Установка pip...
call "%PYTHON_DIR%\python.exe" "%GET_PIP%"
if errorlevel 1 (
    echo Ошибка при установке pip.
    pause
    exit /b 1
)

REM ============ 6. Проверка и очистка ============
echo [6/6] Проверка установки...

REM Добавляем папку Scripts в PATH только для текущей сессии
set "PATH=%PYTHON_DIR%;%PYTHON_DIR%\Scripts;%PATH%"

"%PYTHON_DIR%\Scripts\pip.exe" --version
if errorlevel 1 (
    echo Критическая ошибка: pip не работает.
    echo Проверьте содержимое файла: %PTH_FILE%
    type "%PTH_FILE%"
    pause
    exit /b 1
)

REM ============ ОЧИСТКА ============
del "%ZIP_FILE%" >nul 2>&1
del "%GET_PIP%" >nul 2>&1
echo.
echo ✅ Portable Python с pip успешно установлен в папку: %PYTHON_DIR%
echo Запуск Python: %PYTHON_DIR%\python.exe
echo Запуск pip: %PYTHON_DIR%\Scripts\pip.exe

call installRequirements

:: Проверяем, вызван ли скрипт из другого файла
if "%~0" == "%~f0" (
    pause
)