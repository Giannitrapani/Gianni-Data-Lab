' ============================================================================
' DETENER SERVICIOS FORZADO - JUGOS S.A.
' ============================================================================
' Este script mata todos los procesos Python relacionados con el sistema
' ============================================================================

Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")

' Matar procesos python.exe relacionados con servicio_actualizacion
Set colProcesses = objWMIService.ExecQuery _
    ("SELECT * FROM Win32_Process WHERE Name = 'python.exe' AND CommandLine LIKE '%servicio_actualizacion%'")
For Each objProcess in colProcesses
    objProcess.Terminate()
Next

' Matar procesos python.exe relacionados con monitor_cierre
Set colProcesses = objWMIService.ExecQuery _
    ("SELECT * FROM Win32_Process WHERE Name = 'python.exe' AND CommandLine LIKE '%monitor_cierre%'")
For Each objProcess in colProcesses
    objProcess.Terminate()
Next

' Matar procesos pythonw.exe (todos)
Set colProcesses = objWMIService.ExecQuery _
    ("SELECT * FROM Win32_Process WHERE Name = 'pythonw.exe'")
For Each objProcess in colProcesses
    objProcess.Terminate()
Next

WScript.Echo "Servicios detenidos correctamente"
