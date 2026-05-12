@echo off
REM Vocabulary Test System - Server Launcher

echo ==========================================
echo   Vocabulary Test System - Server
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.6+
    pause
    exit /b 1
)

echo [1/3] Python version:
python --version
echo.

REM Check dependencies
echo [2/3] Checking dependencies...
if exist requirements.txt (
    pip install -r requirements.txt -q
    if errorlevel 1 (
        echo [WARN] Dependency install may have issues, continuing...
    ) else (
        echo [OK] Dependencies ready
    )
) else (
    echo [WARN] requirements.txt not found
)
echo.

REM Check word bank
echo [3/3] Checking word bank...
if exist "data\word_bank\word_bank.json" (
    echo [OK] Word bank found
) else (
    echo [WARN] Word bank not found: data\word_bank\word_bank.json
    echo        Test function may not work properly
)
echo.

REM Start HTTP server
echo Starting HTTP server...
echo.
echo Access URLs:
echo   Main page: http://localhost:8080
echo   Test page: http://localhost:8080/frontend/pages/index.html
echo   Tools page: http://localhost:8080/frontend/pages/tools.html
echo.
echo Press Ctrl+C to stop server
echo ==========================================
echo.

cd /d "%~dp0"

REM Open browser
echo Opening browser...
timeout /t 1 /nobreak >nul
start "" "http://localhost:8080"

REM Start HTTP server
python -m http.server 8080

pause
