@echo off
REM ===================================================================
REM DIAGNOSTICO COMPLETO - JUGOS S.A.
REM ===================================================================

title Diagnostico - JUGOS S.A.
color 0B
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   DIAGNOSTICO DEL SISTEMA
echo ==========================================================
echo.
echo   Este diagnostico verifica:
echo   - Version de Python instalada
echo   - Drivers ODBC disponibles
echo   - Compatibilidad Python vs ODBC
echo   - Conexion a Access
echo.
echo   Y ofrece soluciones si hay problemas
echo.
echo ==========================================================
echo.

pause

set PYTHON_CMD=C:\Python32\python.exe
if not exist "%PYTHON_CMD%" set PYTHON_CMD=python

%PYTHON_CMD% diagnostico_completo.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo ejecutar el diagnostico
    echo.
    echo Verifica que Python este instalado
    pause
)
