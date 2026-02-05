' ============================================================================
' LANZADOR INVISIBLE - JUGOS S.A.
' ============================================================================
' Este script VBS lanza procesos Python completamente invisibles
' ============================================================================

Set objArgs = WScript.Arguments
If objArgs.Count = 0 Then
    WScript.Quit
End If

strCommand = ""
For i = 0 To objArgs.Count - 1
    strCommand = strCommand & " " & objArgs(i)
Next

Set objShell = CreateObject("WScript.Shell")
objShell.Run strCommand, 0, False
Set objShell = Nothing
