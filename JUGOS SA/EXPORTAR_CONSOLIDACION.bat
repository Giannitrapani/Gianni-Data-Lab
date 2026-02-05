@echo off
REM ============================================================================
REM EXPORTAR CONSOLIDACION DESDE ACCESS - VERSION MANUAL
REM ============================================================================
REM Este script te guia para exportar CONSOLIDACION manualmente

setlocal

set "CSV_PATH=%~dp0datos_csv\CONSOLIDACION.csv"

REM Verificar si ya existe el CSV
if exist "%CSV_PATH%" (
    echo CONSOLIDACION.csv ya existe - saltando exportacion
    exit /b 0
)

echo.
echo ======================================================================
echo EXPORTAR CONSOLIDACION DESDE ACCESS
echo ======================================================================
echo.
echo Este CSV no existe aun. Necesitas exportarlo manualmente:
echo.
echo 1. Abre Access: datos_fuente\VerDatosGaspar-local.accdb
echo 2. Presiona Alt + F8
echo 3. Ejecuta: Macro_ExportarConsolidacion
echo 4. Cierra Access
echo.
echo Mientras tanto, el sistema usara las tablas separadas (modo fallback).
echo.

endlocal
exit /b 0
