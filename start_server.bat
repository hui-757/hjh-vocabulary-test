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

echo [1/4] Python version:
python --version
echo.

REM Check dependencies
echo [2/4] Checking dependencies...
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
echo [3/4] Checking word bank...
if exist "data\word_bank\word_bank.json" (
    echo [OK] Word bank found
) else (
    echo [WARN] Word bank not found: data\word_bank\word_bank.json
    echo        Test function may not work properly
)
echo.

REM Check users data
echo [4/4] Checking users data...
if exist "data\users.json" (
    echo [OK] Users data found
) else (
    echo [INFO] Users data will be created on first use
)
echo.

cd /d "%~dp0"

REM Start API server in background
echo Starting API server...
start "API Server" cmd /k "python backend/api/app.py"
echo [OK] API server started at http://localhost:5000
echo.

REM Wait a moment for API to boot up
timeout /t 2 /nobreak >nul

REM Start HTTP server in background
echo Starting HTTP server...
start "HTTP Server" cmd /c "python -m http.server 8080"
echo [OK] HTTP server started at http://localhost:8080
echo.

echo Access URLs:
echo   Main page:   http://localhost:8080
echo   API health:  http://localhost:5000/api/health
echo   Test page:   http://localhost:8080/frontend/pages/index.html
echo   Tools page:  http://localhost:8080/frontend/pages/tools.html
echo.
echo Press any key to stop all servers...
echo ==========================================

REM Open browser
timeout /t 1 /nobreak >nul
start "" "http://localhost:8080"

pause

REM Stop servers
echo.
echo Stopping servers...
taskkill /FI "WINDOWTITLE eq API Server*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq HTTP Server*" /T /F >nul 2>&1
echo [OK] Servers stopped.
pause
