@echo off
title VERIFICAR INSTALACION - JUGOS S.A.
color 0B

echo.
echo ==========================================================
echo   VERIFICACION DE INSTALACION - JUGOS S.A.
echo ==========================================================
echo.

set ERRORES=0

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python:
    python --version
) else (
    echo [X] Python: NO INSTALADO
    set /a ERRORES+=1
)
echo.

echo Verificando librerias de Python...
pip show pandas >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pandas: instalado
) else (
    echo [X] pandas: NO INSTALADO - ejecutar: pip install pandas
    set /a ERRORES+=1
)

pip show pyodbc >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pyodbc: instalado
) else (
    echo [X] pyodbc: NO INSTALADO - ejecutar: pip install pyodbc
    set /a ERRORES+=1
)

pip show plotly >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] plotly: instalado
) else (
    echo [X] plotly: NO INSTALADO - ejecutar: pip install plotly
    set /a ERRORES+=1
)
echo.

echo Verificando Driver ODBC de Access...
python -c "import pyodbc; drivers = [d for d in pyodbc.drivers() if 'Access' in d]; print('[OK] Driver encontrado:', drivers[0]) if drivers else print('[X] NO HAY DRIVER ODBC DE ACCESS')" 2>nul
if %errorlevel% neq 0 (
    echo [X] No se pudo verificar driver ODBC
    set /a ERRORES+=1
)
echo.

echo Verificando Node.js (para Claude Code)...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Node.js:
    node --version
) else (
    echo [X] Node.js: NO INSTALADO (opcional, solo para Claude Code)
)
echo.

echo Verificando Claude Code...
call npm list -g @anthropic-ai/claude-code >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Claude Code: instalado
) else (
    echo [X] Claude Code: NO INSTALADO (opcional)
)
echo.

echo ==========================================================
if %ERRORES% equ 0 (
    echo   RESULTADO: TODO CORRECTO
    echo   El sistema esta listo para funcionar.
) else (
    echo   RESULTADO: %ERRORES% ERRORES ENCONTRADOS
    echo   Ejecuta INSTALAR_REQUISITOS.bat para solucionarlos.
)
echo ==========================================================
echo.
pause
