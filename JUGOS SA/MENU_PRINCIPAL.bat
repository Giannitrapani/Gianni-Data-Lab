@echo off
REM ===================================================================
REM MENU PRINCIPAL - JUGOS S.A.
REM ===================================================================

title Sistema JUGOS S.A. - Menu Principal
color 0B
cd /d "%~dp0"

:MENU
cls
echo.
echo ==========================================================
echo   SISTEMA DE DASHBOARDS - JUGOS S.A.
echo   MENU PRINCIPAL
echo ==========================================================
echo.
echo   [1] Iniciar Sistema (Dashboard)
echo   [2] Detener Servicio de Actualizacion
echo.
echo   [3] Ejecutar Diagnostico
echo   [4] Verificar Drivers ODBC
echo.
echo   [5] Configurar Ruta de Red
echo   [6] Configurar Python Portable
echo.
echo   [7] Leer Instrucciones
echo   [8] Guia Sin Permisos Admin
echo.
echo   [0] Salir
echo.
echo ==========================================================
echo.

set /p opcion="Selecciona una opcion (0-8): "

if "%opcion%"=="1" goto INICIAR
if "%opcion%"=="2" goto DETENER
if "%opcion%"=="3" goto DIAGNOSTICO
if "%opcion%"=="4" goto ODBC
if "%opcion%"=="5" goto RUTA_RED
if "%opcion%"=="6" goto PYTHON_PORTABLE
if "%opcion%"=="7" goto INSTRUCCIONES
if "%opcion%"=="8" goto GUIA_SIN_ADMIN
if "%opcion%"=="0" goto SALIR

echo.
echo Opcion invalida. Intenta de nuevo.
timeout /t 2 /nobreak >nul
goto MENU

:INICIAR
cls
echo.
echo ==========================================================
echo   INICIANDO SISTEMA...
echo ==========================================================
echo.
call INICIAR_SISTEMA.bat
goto MENU

:DETENER
cls
echo.
echo ==========================================================
echo   DETENIENDO SERVICIO...
echo ==========================================================
echo.
call DETENER_SERVICIO.bat
echo.
pause
goto MENU

:DIAGNOSTICO
cls
echo.
echo ==========================================================
echo   EJECUTANDO DIAGNOSTICO...
echo ==========================================================
echo.
call DIAGNOSTICO.bat
goto MENU

:ODBC
cls
echo.
echo ==========================================================
echo   VERIFICANDO DRIVERS ODBC...
echo ==========================================================
echo.
call VERIFICAR_ODBC.bat
goto MENU

:RUTA_RED
cls
echo.
echo ==========================================================
echo   CONFIGURAR RUTA DE RED...
echo ==========================================================
echo.
call CONFIGURAR_RUTA_RED.bat
goto MENU

:PYTHON_PORTABLE
cls
echo.
echo ==========================================================
echo   CONFIGURAR PYTHON PORTABLE...
echo ==========================================================
echo.
call CONFIGURAR_PYTHON_PORTABLE.bat
goto MENU

:INSTRUCCIONES
cls
echo.
echo ==========================================================
echo   ABRIENDO INSTRUCCIONES...
echo ==========================================================
echo.
start notepad INSTRUCCIONES.txt
timeout /t 1 /nobreak >nul
goto MENU

:GUIA_SIN_ADMIN
cls
echo.
echo ==========================================================
echo   ABRIENDO GUIA SIN ADMIN...
echo ==========================================================
echo.
start notepad GUIA_SIN_ADMIN.txt
timeout /t 1 /nobreak >nul
goto MENU

:SALIR
cls
echo.
echo ==========================================================
echo   HASTA LUEGO
echo ==========================================================
echo.
timeout /t 2 /nobreak >nul
exit
