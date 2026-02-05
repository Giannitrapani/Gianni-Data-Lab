@echo off
REM ===================================================================
REM CONFIGURAR PYTHON PORTABLE - JUGOS S.A.
REM ===================================================================
REM Asistente para configurar WinPython portable en el sistema
REM ===================================================================

title Configurar Python Portable - JUGOS S.A.
color 0E
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   CONFIGURAR PYTHON PORTABLE
echo ==========================================================
echo.
echo   Este asistente te ayudara a configurar WinPython
echo   portable para que funcione con el sistema.
echo.
echo   REQUISITO:
echo   Ya debes haber descargado y extraido WinPython
echo   en la carpeta del proyecto.
echo.
echo ==========================================================
echo.

pause

cls
echo.
echo ==========================================================
echo   BUSCANDO INSTALACIONES DE PYTHON
echo ==========================================================
echo.

REM Buscar carpetas de WinPython
set FOUND=0

for /d %%i in (WPy*) do (
    set FOUND=1
    echo   Encontrado: %%i
)

if %FOUND%==0 (
    echo   [!] No se encontraron carpetas WPy* en este directorio
    echo.
    echo   Asegurate de haber extraido WinPython aqui primero.
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================================
echo.

set /p carpeta_python="Ingresa el nombre de la carpeta de Python (ej: WPy32-39100): "

if "%carpeta_python%"=="" (
    echo.
    echo ERROR: No ingresaste ninguna carpeta
    pause
    exit /b 1
)

if not exist "%carpeta_python%" (
    echo.
    echo ERROR: La carpeta "%carpeta_python%" no existe
    pause
    exit /b 1
)

REM Buscar python.exe dentro de la carpeta
set PYTHON_EXE=
if exist "%carpeta_python%\python.exe" set PYTHON_EXE=%carpeta_python%\python.exe
if exist "%carpeta_python%\python-*" (
    for /d %%i in ("%carpeta_python%\python-*") do (
        if exist "%%i\python.exe" set PYTHON_EXE=%%i\python.exe
    )
)

if "%PYTHON_EXE%"=="" (
    echo.
    echo ERROR: No se encontro python.exe en "%carpeta_python%"
    echo.
    echo Verifica que la estructura sea correcta:
    echo    %carpeta_python%\python.exe
    echo o
    echo    %carpeta_python%\python-X.X.X\python.exe
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================================
echo   VERIFICANDO PYTHON
echo ==========================================================
echo.

"%PYTHON_EXE%" --version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo ejecutar Python
    pause
    exit /b 1
)

echo.
echo   OK - Python funciona correctamente
echo.

echo ==========================================================
echo   INSTALANDO LIBRERIAS NECESARIAS
echo ==========================================================
echo.

echo Instalando pandas...
"%PYTHON_EXE%" -m pip install pandas --quiet
echo   OK

echo Instalando pyodbc...
"%PYTHON_EXE%" -m pip install pyodbc --quiet
echo   OK

echo Instalando plotly...
"%PYTHON_EXE%" -m pip install plotly --quiet
echo   OK

echo.
echo   Todas las librerias instaladas correctamente
echo.

echo ==========================================================
echo   ACTUALIZANDO INICIAR_SISTEMA.bat
echo ==========================================================
echo.

REM Crear backup
copy INICIAR_SISTEMA.bat INICIAR_SISTEMA.bat.backup >nul 2>&1

REM Reemplazar la línea de Python
powershell -Command "(Get-Content INICIAR_SISTEMA.bat) -replace 'set PYTHON_CMD=C:\\Python32\\python.exe', 'set PYTHON_CMD=%%~dp0%PYTHON_EXE%' | Set-Content INICIAR_SISTEMA.bat.tmp"
move /y INICIAR_SISTEMA.bat.tmp INICIAR_SISTEMA.bat >nul 2>&1

echo   OK - INICIAR_SISTEMA.bat actualizado
echo   (Backup guardado como: INICIAR_SISTEMA.bat.backup)
echo.

echo ==========================================================
echo   CONFIGURACION COMPLETADA
echo ==========================================================
echo.
echo   Python configurado: %PYTHON_EXE%
echo.
echo   Ahora puedes ejecutar:
echo      INICIAR_SISTEMA.bat
echo.
echo   Para verificar que todo funciona:
echo      DIAGNOSTICO.bat
echo.
echo ==========================================================
echo.

pause
