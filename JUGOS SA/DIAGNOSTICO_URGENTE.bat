@echo off
echo.
echo ======================================================================
echo DIAGNOSTICO DE EMERGENCIA - ENCONTRANDO EL ERROR
echo ======================================================================
echo.

echo Ejecutando INICIAR_SISTEMA.bat con salida visible...
echo.
echo ======================================================================
echo.

REM Ejecutar con pausas para ver errores
call INICIAR_SISTEMA.bat

echo.
echo ======================================================================
echo FIN DEL DIAGNOSTICO
echo ======================================================================
echo.
echo Si viste algun error arriba, ese es el problema.
echo.
pause
