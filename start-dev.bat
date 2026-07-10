@echo off
REM Seller Toolkit — local dev server
REM Access: http://127.0.0.1:8888  or  http://sisuu.com.test  (requires Laragon Apache)
cd /d "%~dp0"
echo Starting Seller Toolkit on http://127.0.0.1:8888 ...
echo Also available at http://sisuu.com.test (if Laragon Apache is running)
venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8888
