@echo off
title Verificar Valores Clave - JUGOS S.A.
cd /d "%~dp0"

cls
echo.
echo ==========================================================
echo   VERIFICAR VALORES CLAVE DEL SISTEMA
echo ==========================================================
echo.
echo Este script verifica los 2 valores principales:
echo.
echo   1. LOGISTICA: Cantidad de kg de fruta procesada
echo      (esperado: 180.693.798 kg)
echo.
echo   2. STOCK GLOBAL: Bins Vacios Disponibles
echo      (esperado: 22.971 bins)
echo.
pause

C:\Python32\python.exe verificar_valores_clave.py

echo.
echo.
pause
