; ============================================================================
; INSTALADOR JUGOS S.A. - Dashboard System
; Creado con Inno Setup
; ============================================================================

#define MyAppName "JUGOS S.A. Dashboard"
#define MyAppVersion "3.1"
#define MyAppPublisher "JUGOS S.A."
#define MyAppURL "https://jugos-sa.com"
#define MyAppExeName "INICIAR_SISTEMA.bat"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName=C:\JUGOS-DASHBOARD
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=.\instalador_output
OutputBaseFilename=JUGOS_Dashboard_Instalador_v3.1
; SetupIconFile requiere .ico - descomentear si se tiene icono
; SetupIconFile=.\icono.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableProgramGroupPage=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Messages]
spanish.WelcomeLabel1=Bienvenido al instalador de {#MyAppName}
spanish.WelcomeLabel2=Este asistente instalara {#MyAppName} version {#MyAppVersion} en su computadora.%n%nSe instalara:%n- Python 3.12.7%n- Driver ODBC de Access%n- Librerias necesarias%n- Sistema de Dashboards%n%nSe recomienda cerrar todas las aplicaciones antes de continuar.
spanish.FinishedHeadingLabel=Instalacion completada
spanish.FinishedLabel=El sistema {#MyAppName} ha sido instalado correctamente.%n%nPuede iniciar el sistema usando el acceso directo en el escritorio.

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el Escritorio"; GroupDescription: "Accesos directos:"

[Files]
; Instaladores
Source: "instaladores\python-3.12.7-amd64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "instaladores\accessdatabaseengine_X64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

; Script de instalacion de librerias
Source: "instalar_librerias.bat"; DestDir: "{tmp}"; Flags: deleteafterinstall

; Archivos principales
Source: "INICIAR_SISTEMA.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "ELEGIR_BASE_DATOS.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "INSTALAR_REQUISITOS.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "VERIFICAR_INSTALACION.bat"; DestDir: "{app}"; Flags: ignoreversion

; Scripts Python principales
Source: "ACTUALIZAR_CSV.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "actualizar_dashboard_completo.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "cargar_datos_universal.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "generar_dashboard.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "generar_pagina_proveedores.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "generar_analisis_logistico.py"; DestDir: "{app}"; Flags: ignoreversion

; HTML y recursos
Source: "dashboard_completo.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "dashboard.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "proveedores.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "logistica.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "favicon.png"; DestDir: "{app}"; Flags: ignoreversion

; Configuracion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "CLAUDE.md"; DestDir: "{app}"; Flags: ignoreversion

; Carpeta datos_csv
Source: "datos_csv\*"; DestDir: "{app}\datos_csv"; Flags: ignoreversion recursesubdirs createallsubdirs

; Carpeta datos_fuente (base de datos)
Source: "datos_fuente\VerDatosGaspar-local.accdb"; DestDir: "{app}\datos_fuente"; Flags: ignoreversion

; Carpeta instaladores (por si se necesitan despues)
Source: "instaladores\*"; DestDir: "{app}\instaladores"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\Elegir Base de Datos"; Filename: "{app}\ELEGIR_BASE_DATOS.bat"; WorkingDir: "{app}"
Name: "{group}\Verificar Instalacion"; Filename: "{app}\VERIFICAR_INSTALACION.bat"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
; Instalar Python silenciosamente
Filename: "{tmp}\python-3.12.7-amd64.exe"; Parameters: "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0"; StatusMsg: "Instalando Python 3.12.7..."; Flags: waituntilterminated

; Instalar Driver ODBC
Filename: "{tmp}\accessdatabaseengine_X64.exe"; Parameters: "/quiet"; StatusMsg: "Instalando Driver ODBC de Access..."; Flags: waituntilterminated skipifdoesntexist

; Instalar librerias pip
Filename: "{tmp}\instalar_librerias.bat"; StatusMsg: "Instalando librerias Python (pandas, pyodbc, plotly)..."; Flags: waituntilterminated runhidden

; Opcion para iniciar el sistema al finalizar
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar {#MyAppName} ahora"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent shellexec

[Code]
// Verificar si Python ya esta instalado
function IsPythonInstalled: Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec('python', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
end;

// Verificar si el driver ODBC ya esta instalado
function IsODBCInstalled: Boolean;
var
  Names: TArrayOfString;
  I: Integer;
begin
  Result := False;
  if RegGetSubkeyNames(HKEY_LOCAL_MACHINE, 'SOFTWARE\ODBC\ODBCINST.INI', Names) then
  begin
    for I := 0 to GetArrayLength(Names) - 1 do
    begin
      if Pos('Microsoft Access Driver', Names[I]) > 0 then
      begin
        Result := True;
        Exit;
      end;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Crear archivo de marca de instalacion exitosa
    SaveStringToFile(ExpandConstant('{app}\instalacion_completa.txt'),
      'Instalacion completada: ' + GetDateTimeString('yyyy-mm-dd hh:nn:ss', '-', ':'), False);
  end;
end;
