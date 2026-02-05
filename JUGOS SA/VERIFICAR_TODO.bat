@echo off
setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo VERIFICACION COMPLETA DEL SISTEMA - JUGOS S.A.
echo ======================================================================
echo.

set "ERRORES=0"

REM Test 1: Verificar que existe el CSV CONSOLIDACION
echo [1/5] Verificando CSV CONSOLIDACION...
if exist "datos_csv\CONSOLIDACION.csv" (
    echo       OK - CSV existe
) else (
    echo       ERROR - CSV no existe
    set /a ERRORES+=1
)

REM Test 2: Verificar Python
echo [2/5] Verificando Python...
C:\Python32\python.exe --version >nul 2>&1
if %errorlevel%==0 (
    echo       OK - Python encontrado
) else (
    echo       ERROR - Python no encontrado
    set /a ERRORES+=1
)

REM Test 3: Probar lectura de CONSOLIDACION
echo [3/5] Probando lectura de CONSOLIDACION...
C:\Python32\python.exe probar_consolidacion.py >nul 2>&1
if %errorlevel%==0 (
    echo       OK - Lectura exitosa
) else (
    echo       ERROR - Fallo al leer datos
    set /a ERRORES+=1
)

REM Test 4: Generar dashboards
echo [4/5] Probando generacion de dashboards...
C:\Python32\python.exe actualizar_dashboard_completo.py >nul 2>&1
if %errorlevel%==0 (
    echo       OK - Dashboards generados
) else (
    echo       ERROR - Fallo al generar dashboards
    set /a ERRORES+=1
)

REM Test 5: Verificar HTMLs
echo [5/5] Verificando archivos HTML...
set HTML_OK=0
if exist "dashboard_completo.html" set /a HTML_OK+=1
if exist "dashboard.html" set /a HTML_OK+=1
if exist "proveedores.html" set /a HTML_OK+=1
if exist "logistica.html" set /a HTML_OK+=1

if %HTML_OK%==4 (
    echo       OK - Todos los HTML generados
) else (
    echo       ERROR - Faltan %HTML_OK%/4 archivos HTML
    set /a ERRORES+=1
)

echo.
echo ======================================================================
if %ERRORES%==0 (
    echo RESULTADO: SISTEMA FUNCIONANDO PERFECTAMENTE
    echo ======================================================================
    echo.
    echo Todo esta listo. Puedes usar el sistema con confianza.
    echo.
    echo Para iniciar: INICIAR_SISTEMA.bat
    echo.
) else (
    echo RESULTADO: %ERRORES% ERRORES ENCONTRADOS
    echo ======================================================================
    echo.
    echo Por favor ejecuta este script con salida visible:
    echo    probar_consolidacion.py
    echo.
    echo Y comparte el error para que lo arreglemos.
    echo.
)

pause
