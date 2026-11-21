@echo off
chcp 65001 >nul
title CleanTV & tvOS Launcher Tiếng Việt - Cài đặt tự động
echo ================================================================
echo    CleanTV & tvOS Launcher Tiếng Việt - Bộ cài đặt 1-Chạm
echo    1. Dọn dẹp quảng cáo, bloatware rác trên Android TV
echo    2. Cài đặt tvOS Launcher Tiếng Việt làm giao diện mặc định
echo ================================================================
echo.

set /p TV_IP="Nhập địa chỉ IP của TV/Máy chiếu (ví dụ: 192.168.1.50): "
if "%TV_IP%"=="" (
    echo [!] Chưa nhập IP. Vui lòng chạy lại!
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0cleantv-setup.ps1" -TvHost "%TV_IP%"
pause
