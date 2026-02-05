@echo off
title Ver Valores Actuales - JUGOS S.A.
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   VALORES ACTUALES DEL SISTEMA
echo ==========================================================
echo.
echo Este script muestra los valores que el sistema esta
echo usando actualmente. Comparalos con tu papel.
echo.
pause

C:\Python32\python.exe ver_valores_sistema.py

echo.
echo.
pause
