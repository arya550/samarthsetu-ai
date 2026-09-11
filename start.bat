@echo off
REM ============================================================
REM  SamarthSetu AI - one-command start (no database, no Node)
REM  Starts FastAPI on port 8000; it serves both API and UI.
REM ============================================================
setlocal

REM Use the py launcher if python is not on PATH
set PY=python
where python >nul 2>nul || set PY=py

cd /d "%~dp0backend"

if not exist .venv (
    echo Creating virtual environment...
    %PY% -m venv .venv || (echo Failed to create venv & pause & exit /b 1)
)

echo Installing dependencies (first run only)...
.venv\Scripts\python.exe -m pip install -q -r requirements.txt || (echo pip install failed & pause & exit /b 1)

echo.
echo ========================================
echo  SamarthSetu AI is starting...
echo  UI:      http://localhost:8000/app/
echo  API:     http://localhost:8000/api/health
echo  API docs: http://localhost:8000/docs
echo ========================================
echo  Close this window to stop the server.
echo.

.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000

endlocal
