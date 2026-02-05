@echo off
echo ========================================
echo PRUEBA DEL SISTEMA - JUGOS S.A.
echo ========================================
echo.

cd /d "%~dp0"

echo Directorio actual:
echo    %CD%
echo.

echo Probando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)
echo.

echo Probando conexion a Access...
python -c "import pyodbc; print('pyodbc OK')"
if %errorlevel% neq 0 (
    echo ERROR: pyodbc no disponible
    pause
    exit /b 1
)
echo.

echo Actualizando CSV...
python ACTUALIZAR_CSV.py
echo.

echo Generando dashboards...
python actualizar_dashboard_completo.py
echo.

echo ========================================
echo PRUEBA COMPLETADA
echo ========================================
echo.
echo Presiona una tecla para abrir el dashboard...
pause

start "" "%CD%\dashboard_completo.html"
