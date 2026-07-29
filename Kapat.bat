@echo off
chcp 65001 > nul
title Sarıbay AI Studio Shutdown

echo ==================================================================
echo   🛑 SARIBAY AI YOUTUBE AUTOMATION STUDIO - KAPATILIYOR...
echo ==================================================================
echo.

echo [1/2] Backend Sunucusu Sonlandırılıyor (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /f /pid %%a > nul 2>&1
)

echo [2/2] Frontend Sunucusu Sonlandırılıyor (Port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173 ^| findstr LISTENING') do (
    taskkill /f /pid %%a > nul 2>&1
)

echo.
echo ==================================================================
echo   ✅ TÜM SERVİSLER VE SUNUCULAR BAŞARIYLA KAPATILDI!
echo ==================================================================
echo.

timeout /t 3
