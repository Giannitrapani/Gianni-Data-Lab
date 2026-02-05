@echo off
setlocal enabledelayedexpansion
title INSTALADOR DE REQUISITOS - JUGOS S.A.
color 0B
cd /d "%~dp0"

echo.
echo ==========================================================
echo   INSTALADOR DE REQUISITOS - JUGOS S.A.
echo ==========================================================
echo.
echo   Este script instalara todo lo necesario:
echo.
echo   1. Python 3.12 (64-bit)
echo   2. Librerias Python (pandas, pyodbc, plotly)
echo   3. Node.js (para Claude Code)
echo   4. Claude Code
echo.
echo   IMPORTANTE: Ejecutar como ADMINISTRADOR si es posible
echo.
echo ==========================================================
echo.
pause

cls
echo.
echo ==========================================================
echo   PASO 1: VERIFICANDO PYTHON
echo ==========================================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python ya esta instalado:
    python --version
    echo.
    set PYTHON_INSTALADO=1
) else (
    echo [X] Python NO esta instalado
    echo.
    set PYTHON_INSTALADO=0
)

if %PYTHON_INSTALADO%==0 (
    echo Intentando instalar Python con winget...
    echo.

    REM Intentar con winget primero (Windows 10/11)
    winget --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo [INFO] Usando winget para instalar Python...
        winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements

        if !errorlevel! equ 0 (
            echo [OK] Python instalado correctamente
            echo.
            echo IMPORTANTE: Cierra esta ventana y vuelve a ejecutar
            echo el script para continuar con la instalacion.
            echo.
            pause
            exit /b 0
        ) else (
            echo [WARN] winget fallo, intentando descarga manual...
        )
    ) else (
        echo [INFO] winget no disponible, intentando descarga manual...
    )

    REM Descarga manual con PowerShell
    echo.
    echo Descargando Python 3.12 desde python.org...
    echo Esto puede tardar unos minutos...
    echo.

    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile '%TEMP%\python_installer.exe'"

    if exist "%TEMP%\python_installer.exe" (
        echo [OK] Descarga completada
        echo.
        echo Instalando Python silenciosamente...
        echo (Esto puede tardar 2-3 minutos)
        echo.

        "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

        if !errorlevel! equ 0 (
            echo [OK] Python instalado correctamente
            del "%TEMP%\python_installer.exe" >nul 2>&1
            echo.
            echo IMPORTANTE: Cierra esta ventana y vuelve a ejecutar
            echo el script para continuar con la instalacion.
            echo.
            pause
            exit /b 0
        ) else (
            echo [ERROR] Fallo la instalacion de Python
            echo.
            echo Por favor, instala Python manualmente desde:
            echo https://www.python.org/downloads/
            echo.
            echo Asegurate de marcar "Add Python to PATH"
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo [ERROR] No se pudo descargar Python
        echo.
        echo Por favor, instala Python manualmente desde:
        echo https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ==========================================================
echo   PASO 2: INSTALANDO LIBRERIAS DE PYTHON
echo ==========================================================
echo.

echo Actualizando pip...
python -m pip install --upgrade pip --quiet

echo.
echo Instalando pandas...
pip install pandas --quiet
if %errorlevel% equ 0 (
    echo [OK] pandas instalado
) else (
    echo [ERROR] Fallo instalacion de pandas
)

echo.
echo Instalando pyodbc...
pip install pyodbc --quiet
if %errorlevel% equ 0 (
    echo [OK] pyodbc instalado
) else (
    echo [ERROR] Fallo instalacion de pyodbc
)

echo.
echo Instalando plotly...
pip install plotly --quiet
if %errorlevel% equ 0 (
    echo [OK] plotly instalado
) else (
    echo [ERROR] Fallo instalacion de plotly
)

echo.
echo ==========================================================
echo   PASO 3: VERIFICANDO NODE.JS
echo ==========================================================
echo.

REM Verificar si Node.js esta instalado
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Node.js ya esta instalado:
    node --version
    echo.
    set NODE_INSTALADO=1
) else (
    echo [X] Node.js NO esta instalado
    echo.
    set NODE_INSTALADO=0
)

if %NODE_INSTALADO%==0 (
    echo Intentando instalar Node.js...
    echo.

    REM Intentar con winget primero
    winget --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo [INFO] Usando winget para instalar Node.js...
        winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements

        if !errorlevel! equ 0 (
            echo [OK] Node.js instalado correctamente
            echo.
            echo IMPORTANTE: Cierra esta ventana y vuelve a ejecutar
            echo el script para continuar con la instalacion.
            echo.
            pause
            exit /b 0
        ) else (
            echo [WARN] winget fallo, intentando descarga manual...
        )
    ) else (
        echo [INFO] winget no disponible, intentando descarga manual...
    )

    REM Descarga manual
    echo.
    echo Descargando Node.js LTS desde nodejs.org...
    echo Esto puede tardar unos minutos...
    echo.

    powershell -Command "Invoke-WebRequest -Uri 'https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi' -OutFile '%TEMP%\node_installer.msi'"

    if exist "%TEMP%\node_installer.msi" (
        echo [OK] Descarga completada
        echo.
        echo Instalando Node.js silenciosamente...
        echo (Esto puede tardar 1-2 minutos)
        echo.

        msiexec /i "%TEMP%\node_installer.msi" /quiet /norestart

        if !errorlevel! equ 0 (
            echo [OK] Node.js instalado correctamente
            del "%TEMP%\node_installer.msi" >nul 2>&1
            echo.
            echo IMPORTANTE: Cierra esta ventana y vuelve a ejecutar
            echo el script para continuar con Claude Code.
            echo.
            pause
            exit /b 0
        ) else (
            echo [ERROR] Fallo la instalacion de Node.js
            echo.
            echo Por favor, instala Node.js manualmente desde:
            echo https://nodejs.org/
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo [ERROR] No se pudo descargar Node.js
        echo.
        echo Por favor, instala Node.js manualmente desde:
        echo https://nodejs.org/
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ==========================================================
echo   PASO 4: INSTALANDO CLAUDE CODE
echo ==========================================================
echo.

REM Verificar si Claude Code ya esta instalado
call npm list -g @anthropic-ai/claude-code >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Claude Code ya esta instalado
    echo.
) else (
    echo Instalando Claude Code...
    echo (Esto puede tardar 1-2 minutos)
    echo.

    call npm install -g @anthropic-ai/claude-code

    if !errorlevel! equ 0 (
        echo.
        echo [OK] Claude Code instalado correctamente
    ) else (
        echo.
        echo [WARN] Hubo un problema instalando Claude Code
        echo Intenta manualmente: npm install -g @anthropic-ai/claude-code
    )
)

echo.
echo ==========================================================
echo   VERIFICACION FINAL
echo ==========================================================
echo.

echo Verificando instalaciones...
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python:
    python --version
) else (
    echo [X] Python: NO INSTALADO
)

pip show pandas >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pandas: instalado
) else (
    echo [X] pandas: NO INSTALADO
)

pip show pyodbc >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pyodbc: instalado
) else (
    echo [X] pyodbc: NO INSTALADO
)

pip show plotly >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] plotly: instalado
) else (
    echo [X] plotly: NO INSTALADO
)

node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Node.js:
    node --version
) else (
    echo [X] Node.js: NO INSTALADO
)

call npm list -g @anthropic-ai/claude-code >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Claude Code: instalado
) else (
    echo [X] Claude Code: NO INSTALADO
)

echo.
echo ==========================================================
echo   INSTALACION COMPLETADA
echo ==========================================================
echo.
echo   Ahora puedes:
echo.
echo   1. Ejecutar ELEGIR_BASE_DATOS.bat para elegir la base
echo   2. Ejecutar INICIAR_SISTEMA.bat para ver el dashboard
echo   3. Escribir "claude" en CMD para usar Claude Code
echo.
echo ==========================================================
echo.
pause
