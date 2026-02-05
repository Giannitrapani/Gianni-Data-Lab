@echo off
REM ===================================================================
REM ELEGIR BASE DE DATOS ACCESS - JUGOS S.A.
REM ===================================================================
REM Abre explorador de Windows para seleccionar el archivo Access
REM La selección queda guardada permanentemente
REM ===================================================================

title Elegir Base de Datos - JUGOS S.A.
color 0B
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   ELEGIR BASE DE DATOS ACCESS
echo ==========================================================
echo.
echo   Se abrira un cuadro de dialogo para que selecciones
echo   el archivo Access (.accdb) que deseas usar.
echo.
echo   CASOS DE USO:
echo   -------------
echo   - Presentacion: Selecciona Access 2025 (año completo)
echo   - Produccion: Selecciona Access 2026 (red/local)
echo   - Pruebas: Selecciona cualquier Access de prueba
echo.
echo   La seleccion queda guardada hasta que vuelvas a
echo   ejecutar este archivo y elijas otra base de datos.
echo.
echo ==========================================================
echo.
pause

REM Crear script PowerShell para abrir cuadro de dialogo
echo Add-Type -AssemblyName System.Windows.Forms > "%TEMP%\seleccionar_access.ps1"
echo $OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog >> "%TEMP%\seleccionar_access.ps1"
echo $OpenFileDialog.Title = "Selecciona el archivo Access a usar" >> "%TEMP%\seleccionar_access.ps1"
echo $OpenFileDialog.Filter = "Access Database (*.accdb)|*.accdb|Access 2003 (*.mdb)|*.mdb|Todos (*.*)|*.*" >> "%TEMP%\seleccionar_access.ps1"
echo $OpenFileDialog.InitialDirectory = "%CD%\datos_fuente" >> "%TEMP%\seleccionar_access.ps1"
echo if ($OpenFileDialog.ShowDialog() -eq 'OK') { >> "%TEMP%\seleccionar_access.ps1"
echo     Write-Output $OpenFileDialog.FileName >> "%TEMP%\seleccionar_access.ps1"
echo } else { >> "%TEMP%\seleccionar_access.ps1"
echo     Write-Output "CANCELADO" >> "%TEMP%\seleccionar_access.ps1"
echo } >> "%TEMP%\seleccionar_access.ps1"

REM Ejecutar script PowerShell
for /f "delims=" %%a in ('powershell -ExecutionPolicy Bypass -File "%TEMP%\seleccionar_access.ps1"') do set RUTA_SELECCIONADA=%%a

REM Limpiar script temporal
del "%TEMP%\seleccionar_access.ps1" >nul 2>&1

REM Verificar si se cancelo
if "%RUTA_SELECCIONADA%"=="CANCELADO" (
    cls
    echo.
    echo ==========================================================
    echo   OPERACION CANCELADA
    echo ==========================================================
    echo.
    echo   No se realizo ningun cambio.
    echo   La configuracion anterior sigue activa.
    echo.
    echo ==========================================================
    echo.
    timeout /t 3 /nobreak >nul
    exit /b 0
)

REM Verificar que se selecciono algo
if "%RUTA_SELECCIONADA%"=="" (
    cls
    echo.
    echo ==========================================================
    echo   ERROR
    echo ==========================================================
    echo.
    echo   No se selecciono ningun archivo.
    echo.
    echo ==========================================================
    echo.
    timeout /t 3 /nobreak >nul
    exit /b 1
)

cls
echo.
echo ==========================================================
echo   ARCHIVO SELECCIONADO
echo ==========================================================
echo.
echo   Archivo: %RUTA_SELECCIONADA%
echo.

REM Verificar que el archivo existe
if exist "%RUTA_SELECCIONADA%" (
    echo   Estado: OK - Archivo encontrado
) else (
    echo   ADVERTENCIA: No se pudo verificar el archivo
)

echo.
echo   Guardando configuracion...

REM Escapar backslashes para JSON (reemplazar \ por \\)
set "ruta_escapada=%RUTA_SELECCIONADA:\=\\%"

REM Actualizar config.json con la ruta seleccionada
powershell -Command "(Get-Content config.json) -replace '\"ruta_base_datos\": \".*\"', '\"ruta_base_datos\": \"%ruta_escapada%\"' | Set-Content config.json"

echo   OK - Configuracion guardada
echo.
echo ==========================================================
echo.
echo   SISTEMA CONFIGURADO CORRECTAMENTE
echo.
echo   Desde ahora, cada vez que ejecutes INICIAR_SISTEMA.bat
echo   se usara el archivo que acabas de seleccionar.
echo.
echo   Para cambiar a otra base de datos, simplemente vuelve
echo   a ejecutar este archivo (ELEGIR_BASE_DATOS.bat).
echo.
echo ==========================================================
echo.
echo   Puedes iniciar el sistema ahora con:
echo   INICIAR_SISTEMA.bat
echo.
echo ==========================================================
echo.

timeout /t 8 /nobreak >nul
exit /b 0
