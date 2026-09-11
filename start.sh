#!/bin/bash
# ============================================================
#  SamarthSetu AI - one-command start (no database, no Node)
#  Starts FastAPI on port 8000; it serves both API and UI.
# ============================================================
set -e
cd "$(dirname "$0")/backend"

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python

if [ ! -d .venv ]; then
    echo "Creating virtual environment..."
    "$PY" -m venv .venv
fi

echo "Installing dependencies (first run only)..."
.venv/bin/python -m pip install -q -r requirements.txt

echo ""
echo "========================================"
echo " SamarthSetu AI is starting..."
echo " UI:       http://localhost:8000/app/"
echo " API:      http://localhost:8000/api/health"
echo " API docs: http://localhost:8000/docs"
echo "========================================"
echo " Press Ctrl+C to stop the server."
echo ""

exec .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
