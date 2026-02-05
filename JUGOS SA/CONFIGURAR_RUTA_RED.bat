@echo off
REM ===================================================================
REM CONFIGURAR RUTA DE RED PARA ACCESS - JUGOS S.A.
REM ===================================================================
REM Usa este archivo cuando despliegues en la empresa para configurar
REM la ruta de red donde está el archivo Access
REM ===================================================================

title Configurar Ruta de Red - JUGOS S.A.
color 0E
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   CONFIGURAR RUTA DE RED PARA ACCESS
echo ==========================================================
echo.
echo   Usa este asistente cuando copies el sistema a la empresa
echo   y necesites que lea el Access desde una ruta de red
echo.
echo ==========================================================
echo.
echo.

echo OPCIONES:
echo.
echo   [1] Usar ruta AUTO (busca Access en carpeta local)
echo   [2] Configurar ruta de RED personalizada
echo   [3] Cancelar
echo.

set /p opcion="Selecciona una opcion (1-3): "

if "%opcion%"=="1" goto AUTO
if "%opcion%"=="2" goto RED
if "%opcion%"=="3" goto CANCELAR

echo.
echo Opcion invalida. Intenta de nuevo.
timeout /t 2 /nobreak >nul
goto START

:AUTO
cls
echo.
echo ==========================================================
echo   CONFIGURANDO MODO AUTO
echo ==========================================================
echo.
echo   El sistema buscara el Access en:
echo   [Carpeta del sistema]\datos_fuente\VerDatosGaspar-local.accdb
echo.
echo ==========================================================
echo.

REM Actualizar config.json
powershell -Command "(Get-Content config.json) -replace '\"ruta_base_datos\": \".*\"', '\"ruta_base_datos\": \"auto\"' | Set-Content config.json"

echo   OK - Configuracion actualizada a modo AUTO
echo.
echo   Asegurate de que el archivo Access este en:
echo   datos_fuente\VerDatosGaspar-local.accdb
echo.
timeout /t 5 /nobreak >nul
goto FIN

:RED
cls
echo.
echo ==========================================================
echo   CONFIGURAR RUTA DE RED
echo ==========================================================
echo.
echo   Ejemplos de rutas validas:
echo.
echo   - Ruta de red UNC:
echo     \\SERVIDOR\carpeta\VerDatosGaspar-local.accdb
echo.
echo   - Unidad de red mapeada:
echo     Z:\JUGOS\datos_fuente\VerDatosGaspar-local.accdb
echo.
echo   - Ruta local:
echo     C:\JUGOS\datos_fuente\VerDatosGaspar-local.accdb
echo.
echo ==========================================================
echo.

set /p ruta_red="Ingresa la ruta completa del Access: "

if "%ruta_red%"=="" (
    echo.
    echo ERROR: No ingresaste ninguna ruta
    timeout /t 2 /nobreak >nul
    goto RED
)

echo.
echo Verificando si la ruta existe...

if exist "%ruta_red%" (
    echo   OK - Archivo encontrado
) else (
    echo   ADVERTENCIA: No se pudo verificar el archivo
    echo   Asegurate de que la ruta sea correcta
)

echo.
echo Actualizando configuracion...

REM Escapar backslashes para JSON
set "ruta_escapada=%ruta_red:\=\\%"

REM Actualizar config.json
powershell -Command "(Get-Content config.json) -replace '\"ruta_base_datos\": \".*\"', '\"ruta_base_datos\": \"%ruta_escapada%\"' | Set-Content config.json"

echo   OK - Configuracion actualizada
echo.
echo   Ruta configurada:
echo   %ruta_red%
echo.
timeout /t 5 /nobreak >nul
goto FIN

:CANCELAR
cls
echo.
echo   Configuracion cancelada
echo.
timeout /t 2 /nobreak >nul
goto FIN

:FIN
cls
echo.
echo ==========================================================
echo   CONFIGURACION COMPLETADA
echo ==========================================================
echo.
echo   Puedes iniciar el sistema con:
echo   INICIAR_SISTEMA.bat
echo.
echo ==========================================================
echo.

timeout /t 3 /nobreak >nul
exit
