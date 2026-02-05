@echo off
setlocal enabledelayedexpansion

title JUGOS S.A. - Sistema de Dashboards
color 0A
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   SISTEMA DE DASHBOARDS - JUGOS S.A.
echo ==========================================================
echo.

REM Usar Python directamente
set PYTHON_CMD=C:\Python32\python.exe

echo [1/4] Generando dashboards...
%PYTHON_CMD% actualizar_dashboard_completo.py

if %errorlevel% neq 0 (
    echo       ERROR generando dashboards
    pause
    exit /b 1
)
echo       OK
echo.

echo [2/4] Guardando timestamp...
echo %date% %time% > ultima_actualizacion.txt
echo       OK
echo.

echo [3/4] Iniciando servicio de actualizacion (cada 1 hora)...
start "Servicio Actualizacion" /MIN %PYTHON_CMD% servicio_actualizacion.py
timeout /t 2 /nobreak >nul
echo       OK - Servicio iniciado en segundo plano
echo.

echo [4/4] Abriendo navegador...
start "" "msedge.exe" --new-window --disable-http-cache "file:///%~dp0dashboard_completo.html"
if %errorlevel% neq 0 (
    start "" "chrome.exe" --new-window --disable-http-cache "file:///%~dp0dashboard_completo.html"
)
if %errorlevel% neq 0 (
    start "" "%~dp0dashboard_completo.html"
)
echo       OK
echo.

echo.
echo ==========================================================
echo   SISTEMA INICIADO CORRECTAMENTE
echo ==========================================================
echo.
echo   Dashboard abierto en navegador
echo   Actualizacion automatica cada 1 hora
echo.
echo   Para detener: DETENER_SERVICIO.bat
echo.
echo ==========================================================
echo.
pause
