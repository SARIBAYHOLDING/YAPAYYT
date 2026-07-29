@echo off
chcp 65001 > nul
title Sarıbay AI YouTube Automation Studio Launcher

echo ==================================================================
echo   🚀 SARIBAY AI YOUTUBE AUTOMATION STUDIO - BAŞLATILIYOR...
echo   Geliştirici: Selahattin Sarıbay (Sarıbay Yazılım)
echo ==================================================================
echo.

cd /d "%~dp0"

echo [1/2] Backend Sunucusu Başlatılıyor (Port 8000)...
start "Sarıbay Backend API" cmd /k ".\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak > nul

echo [2/2] Frontend Web Stüdyosu Başlatılıyor (Port 5173)...
cd frontend
start "Sarıbay Frontend UI" cmd /k "npm.cmd run dev"

echo.
echo ==================================================================
echo   ✅ TÜM SUNUCULAR BAŞARIYLA BAŞLATILDI!
echo   - Web Panel Adresi: http://localhost:5173/
echo   - Backend API:       http://127.0.0.1:8000
echo ==================================================================
echo.

timeout /t 2 /nobreak > nul
start http://localhost:5173/

pause
