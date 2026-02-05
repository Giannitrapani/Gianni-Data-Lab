@echo off
title JUGOS S.A. - Dashboard (Auto-actualizacion cada 1 hora)
color 0A
cd /d "%~dp0"

echo.
echo ========================================
echo   SISTEMA DE DASHBOARDS - JUGOS S.A.
echo ========================================
echo.

echo [1/3] Actualizando datos...
python ACTUALIZAR_CSV.py
if %errorlevel% neq 0 (
    echo       Usando CSV existentes...
)
echo       OK
echo.

echo [2/3] Generando dashboards...
python actualizar_dashboard_completo.py
echo.

echo [3/3] Abriendo dashboard...
start "" "%CD%\dashboard_completo.html"
echo       OK
echo.

echo ========================================
echo   SISTEMA INICIADO - AUTO-ACTUALIZACION
echo ========================================
echo.
echo   El dashboard se actualiza cada 1 HORA automaticamente.
echo   Deja esta ventana abierta (puede minimizarla).
echo   Para detener: cierra esta ventana o presiona Ctrl+C
echo.
echo ========================================

:LOOP
echo.
echo [%date% %time%] Proxima actualizacion en 5 minutos...
echo.

REM Esperar 5 minutos (300 segundos) - Cambiar a 3600 para 1 hora
timeout /t 300 /nobreak >nul

echo.
echo ========================================
echo [%date% %time%] ACTUALIZANDO DATOS...
echo ========================================
echo.

python ACTUALIZAR_CSV.py
if %errorlevel% neq 0 (
    echo       Error al actualizar CSV, usando existentes...
)

python actualizar_dashboard_completo.py

echo.
echo [%date% %time%] Actualizacion completada.
echo El dashboard se recargara automaticamente.

goto LOOP
