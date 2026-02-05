@echo off
REM ===================================================================
REM VERIFICAR DRIVERS ODBC - JUGOS S.A.
REM ===================================================================

title Verificar ODBC - JUGOS S.A.
color 0B
cd /d "%~dp0"

set PYTHON_CMD=C:\Python32\python.exe
if not exist "%PYTHON_CMD%" set PYTHON_CMD=python

%PYTHON_CMD% verificar_odbc.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo ejecutar el verificador
    pause
)
