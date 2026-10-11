@echo off
chcp 65001 >nul

:: Указываем путь к твоему локальному Python
set PYTHON_PATH=.\python\python.exe

:: Проверяем, существует ли файл
if not exist "%PYTHON_PATH%" (
    echo [ERROR] Файл %PYTHON_PATH% не найден!
    echo Проверь, лежит ли python.exe в папке .\python\
    pause
    exit /b 1
)

:: Меню выбора
echo ========================================
echo   Sourcerer Generator - Dev Tools
echo ========================================
echo.
echo [1] Запустить тесты
echo [2] Проверить код (ruff)
echo [3] Отформатировать код (black + ruff)
echo [4] Проверить типы (mypy)
echo [5] Все проверки сразу
echo [6] Установить dev-зависимости
echo [0] Выход
echo.

set /p choice="Выберите действие: "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto lint
if "%choice%"=="3" goto format
if "%choice%"=="4" goto typecheck
if "%choice%"=="5" goto check_all
if "%choice%"=="6" goto install
if "%choice%"=="0" exit /b 0

echo Неверный выбор
pause
exit /b 1

:test
echo.
echo === Запуск тестов ===
"%PYTHON_PATH%" -m pytest --cov=module --cov-report=term-missing -v
pause
exit /b 0

:lint
echo.
echo === Проверка кода (Ruff) ===
"%PYTHON_PATH%" -m ruff check .
pause
exit /b 0

:format
echo.
echo === Форматирование кода ===
"%PYTHON_PATH%" -m ruff format .
"%PYTHON_PATH%" -m black .
echo Готово!
pause
exit /b 0

:typecheck
echo.
echo === Проверка типов (Mypy) ===
"%PYTHON_PATH%" -m mypy .
pause
exit /b 0

:check_all
echo.
echo === Полная проверка ===
echo [1/4] Ruff...
"%PYTHON_PATH%" -m ruff check .
echo [2/4] Black...
"%PYTHON_PATH%" -m black --check .
echo [3/4] Mypy...
"%PYTHON_PATH%" -m mypy .
echo [4/4] Tests...
"%PYTHON_PATH%" -m pytest --cov=module -v
pause
exit /b 0

:install
echo.
echo === Установка зависимостей ===
"%PYTHON_PATH%" -m pip install -e ".[dev]"
"%PYTHON_PATH%" -m pip install pre-commit
"%PYTHON_PATH%" -m pre_commit install
echo Готово!
pause
exit /b 0