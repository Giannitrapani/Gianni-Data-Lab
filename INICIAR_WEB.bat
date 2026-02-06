@echo off
title Gianni Data Lab - Servidor Web
color 0B

echo.
echo ====================================================
echo    GIANNI DATA LAB - Portfolio Web Local
echo ====================================================
echo.
echo  Iniciando servidor en http://localhost:8080 ...
echo  El navegador se abrira automaticamente.
echo.
echo  Para detener: cierra esta ventana o presiona Ctrl+C
echo ====================================================
echo.

cd /d "%~dp0"

python servidor.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] No se pudo iniciar el servidor.
    echo Verifica que Python este instalado y en el PATH.
    echo.
    pause
)
