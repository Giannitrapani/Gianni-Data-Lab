@echo off
REM ===================================================================
REM DETENER SERVICIO DE ACTUALIZACION - JUGOS S.A.
REM ===================================================================

title Detener Servicio - JUGOS S.A.
color 0C
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   DETENER SERVICIO DE ACTUALIZACION
echo ==========================================================
echo.

echo Deteniendo servicios automaticos...

REM Usar script VBS para matar procesos de forma efectiva
cscript //nologo detener_servicios_forzado.vbs

REM Método adicional por si acaso
taskkill /F /IM pythonw.exe >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *servicio*" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *monitor*" >nul 2>&1

echo.
echo   OK - Todos los servicios detenidos
echo.
echo ==========================================================
echo.

timeout /t 3 /nobreak >nul
exit
