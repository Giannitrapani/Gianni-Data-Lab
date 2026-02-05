@echo off
title Crear Instalador - JUGOS S.A.
color 0E
cd /d "%~dp0"

echo.
echo ========================================
echo   CREAR INSTALADOR - JUGOS S.A.
echo ========================================
echo.

REM Buscar Inno Setup en ubicaciones comunes
set "ISCC="

if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"
)

if "%ISCC%"=="" (
    echo ERROR: Inno Setup no encontrado.
    echo.
    echo Por favor instale Inno Setup 6 desde:
    echo https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

echo Inno Setup encontrado: %ISCC%
echo.
echo Compilando instalador...
echo Esto puede tardar varios minutos...
echo.

"%ISCC%" "instalador_setup.iss"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Fallo la compilacion.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALADOR CREADO EXITOSAMENTE
echo ========================================
echo.
echo Archivo generado en:
echo   instalador_output\JUGOS_Dashboard_Instalador_v3.1.exe
echo.
echo Copie este archivo a la otra PC y ejecutelo.
echo.

pause
