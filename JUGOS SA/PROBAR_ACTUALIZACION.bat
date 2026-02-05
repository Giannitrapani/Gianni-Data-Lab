@echo off
REM ===================================================================
REM PRUEBA DE ACTUALIZACION - JUGOS S.A.
REM ===================================================================
REM Este script prueba que los cambios en Access se reflejen
REM ===================================================================

title Prueba de Actualizacion
color 0E
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   PRUEBA DE ACTUALIZACION - JUGOS S.A.
echo ==========================================================
echo.
echo   Este script te guiara para probar que los cambios
echo   en Access se reflejen correctamente en el sistema.
echo.
echo ==========================================================
echo.

pause

echo.
echo PASO 1: Deteniendo servicio de actualizacion...
taskkill /F /FI "WINDOWTITLE eq *servicio_actualizacion*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *servicio*" >nul 2>&1
echo    OK - Servicio detenido
echo.

pause

echo.
echo PASO 2: Cerrando navegadores...
taskkill /F /IM msedge.exe >nul 2>&1
taskkill /F /IM chrome.exe >nul 2>&1
echo    OK - Navegadores cerrados
echo.

echo ==========================================================
echo   AHORA ES TU TURNO
echo ==========================================================
echo.
echo   1. Abre Access: datos_fuente\VerDatosGaspar-local.accdb
echo   2. Modifica algun dato (ejemplo: cambiar un valor)
echo   3. Guarda y cierra Access
echo   4. Vuelve a esta ventana y presiona Enter
echo.
echo ==========================================================
echo.

pause

echo.
echo PASO 3: Actualizando CSV desde Access...
python ACTUALIZAR_CSV.py

if %errorlevel%==0 (
    echo    OK - CSV actualizados con datos nuevos
) else (
    echo    ERROR - No se pudieron actualizar CSV
    pause
    exit /b 1
)

echo.
echo PASO 4: Regenerando dashboards...
python actualizar_dashboard_completo.py

if %errorlevel%==0 (
    echo    OK - Dashboards regenerados
) else (
    echo    ERROR - No se pudieron regenerar dashboards
    pause
    exit /b 1
)

echo.
echo PASO 5: Abriendo navegador...
set TS=%RANDOM%%RANDOM%%RANDOM%

where msedge >nul 2>&1
if %errorlevel%==0 (
    start msedge --new-window --start-maximized --disable-http-cache "%CD%\dashboard_completo.html?v=%TS%"
) else (
    start "" "%CD%\dashboard_completo.html"
)

echo    OK - Navegador abierto
echo.
echo ==========================================================
echo   VERIFICA EN EL NAVEGADOR
echo ==========================================================
echo.
echo   Los cambios que hiciste en Access deberian verse
echo   reflejados en el dashboard.
echo.
echo   Si ves los cambios: TODO FUNCIONA CORRECTAMENTE
echo   Si NO ves los cambios: Presiona Ctrl+F5 en el navegador
echo.
echo ==========================================================
echo.

timeout /t 10 /nobreak >nul
exit
