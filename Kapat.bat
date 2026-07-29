@echo off
chcp 65001 > nul
title Saribay AI Studio Shutdown

echo ==================================================================
echo   SARIBAY AI YOUTUBE AUTOMATION STUDIO - KAPATILIYOR...
echo ==================================================================
echo.

echo [1/2] Backend Sunucusu Sonlandiriliyor (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a > nul 2>&1
)

echo [2/2] Frontend Sunucusu Sonlandiriliyor (Port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173 ^| findstr LISTENING') do (
    taskkill /F /PID %%a > nul 2>&1
)

echo.
echo ==================================================================
echo   TUM SERVISLER VE SUNUCULAR BASARIYLA KAPATILDI!
echo ==================================================================
echo.
