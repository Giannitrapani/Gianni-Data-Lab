@echo off
REM ============================================================================
REM VERSION PARA PRESENTACION - GARANTIZADO QUE FUNCIONA
REM ============================================================================

title JUGOS S.A. - Dashboard
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   JUGOS S.A. - SISTEMA DE DASHBOARDS
echo ==========================================================
echo.
echo Generando dashboards, por favor espera...
echo.

REM Generar dashboards
C:\Python32\python.exe actualizar_dashboard_completo.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudieron generar los dashboards
    echo.
    pause
    exit /b 1
)

REM Guardar timestamp
echo %date% %time% > ultima_actualizacion.txt

echo.
echo Dashboards generados correctamente.
echo.
echo Abriendo en navegador...
echo.

REM Abrir navegador
start "" "dashboard_completo.html"

echo.
echo ==========================================================
echo   SISTEMA LISTO
echo ==========================================================
echo.
echo Dashboard abierto. Puedes cerrar esta ventana.
echo.
timeout /t 3 /nobreak >nul
exit
