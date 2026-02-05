@echo off
REM Script para instalar librerias Python necesarias
REM Se ejecuta durante la instalacion

REM Esperar a que Python termine de instalarse
timeout /t 5 /nobreak >nul

REM Actualizar pip
python -m pip install --upgrade pip --quiet

REM Instalar librerias necesarias
python -m pip install pandas pyodbc plotly --quiet

exit /b 0
