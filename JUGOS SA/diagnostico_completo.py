# ============================================================================
# DIAGNÓSTICO COMPLETO - JUGOS S.A.
# ============================================================================
# Detecta compatibilidad Python vs ODBC y ofrece soluciones
# ============================================================================

import sys
import struct
import os

print("="*70)
print("DIAGNOSTICO COMPLETO - JUGOS S.A.")
print("="*70)
print()

# ============================================================================
# 1. INFORMACIÓN DEL SISTEMA
# ============================================================================
print("[1] INFORMACIÓN DEL SISTEMA")
print("-"*70)

import platform
print(f"   Sistema Operativo: {platform.system()} {platform.release()}")
print(f"   Arquitectura OS: {platform.architecture()[0]}")
print(f"   Python Version: {sys.version.split()[0]}")

# Detectar si Python es x32 o x64
bits_python = struct.calcsize("P") * 8
print(f"   Python Arquitectura: {bits_python} bits")

if bits_python == 64:
    print("   >> Python es 64 bits (x64)")
elif bits_python == 32:
    print("   >> Python es 32 bits (x86/x32)")

print()

# ============================================================================
# 2. VERIFICAR PYODBC
# ============================================================================
print("[2] VERIFICAR PYODBC")
print("-"*70)

try:
    import pyodbc
    print(f"   OK - pyodbc instalado (version {pyodbc.version})")
    pyodbc_disponible = True
except ImportError:
    print("   [!] pyodbc NO esta instalado")
    print()
    print("   SOLUCION: Ejecuta en CMD (como usuario normal):")
    print("      pip install pyodbc")
    print()
    pyodbc_disponible = False

print()

# ============================================================================
# 3. DRIVERS ODBC INSTALADOS
# ============================================================================
print("[3] DRIVERS ODBC INSTALADOS")
print("-"*70)

if pyodbc_disponible:
    drivers = pyodbc.drivers()

    if not drivers:
        print("   [!] NO se encontraron drivers ODBC")
        print()
        print("   CAUSA PROBABLE:")
        print("      - Office no esta instalado")
        print("      - Access no esta instalado")
        print()
    else:
        print(f"   Total de drivers: {len(drivers)}")
        print()

        # Buscar drivers de Access
        drivers_access_x64 = []
        drivers_access_x32 = []

        for driver in drivers:
            if "access" in driver.lower():
                if "*.accdb" in driver.lower() or ".accdb" in driver.lower():
                    drivers_access_x64.append(driver)
                    print(f"   [x64] {driver}")
                elif "*.mdb" in driver.lower():
                    drivers_access_x32.append(driver)
                    print(f"   [x32] {driver}")
                else:
                    print(f"   [???] {driver}")

        if not drivers_access_x64 and not drivers_access_x32:
            print()
            print("   [!] NO se encontro driver de Access")
            print()
            print("   Si Access abre archivos .accdb en esta PC:")
            print("      - El driver SI existe pero Python no lo ve")
            print("      - Probablemente hay incompatibilidad x32/x64")

print()

# ============================================================================
# 4. ANÁLISIS DE COMPATIBILIDAD
# ============================================================================
print("[4] ANALISIS DE COMPATIBILIDAD")
print("-"*70)

if pyodbc_disponible:
    compatible = False
    mensaje_compatibilidad = ""

    if bits_python == 64:
        if drivers_access_x64:
            compatible = True
            mensaje_compatibilidad = "OK - Python x64 con Driver ODBC x64"
        elif drivers_access_x32:
            compatible = False
            mensaje_compatibilidad = "INCOMPATIBLE - Python x64 NO puede usar Driver ODBC x32"
        else:
            compatible = False
            mensaje_compatibilidad = "NO se encontro driver de Access compatible"
    elif bits_python == 32:
        if drivers_access_x32:
            compatible = True
            mensaje_compatibilidad = "OK - Python x32 con Driver ODBC x32"
        elif drivers_access_x64:
            compatible = False
            mensaje_compatibilidad = "INCOMPATIBLE - Python x32 NO puede usar Driver ODBC x64"
        else:
            compatible = False
            mensaje_compatibilidad = "NO se encontro driver de Access compatible"

    if compatible:
        print(f"   ✓✓✓ {mensaje_compatibilidad}")
        print()
        print("   >> El sistema FUNCIONARA correctamente")
    else:
        print(f"   [X] {mensaje_compatibilidad}")
        print()
        print("   >> El sistema NO puede leer Access directamente")

print()

# ============================================================================
# 5. PROBAR CONEXIÓN A ACCESS
# ============================================================================
print("[5] PROBAR CONEXION A ACCESS")
print("-"*70)

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'datos_fuente', 'VerDatosGaspar-local.accdb')

if not os.path.exists(db_path):
    print(f"   [!] Archivo Access NO encontrado en:")
    print(f"       {db_path}")
    print()
else:
    print(f"   OK - Archivo Access encontrado")
    print(f"       {db_path}")
    print()

    if pyodbc_disponible:
        print("   Intentando conectar...")

        conectado = False
        driver_usado = None

        drivers_a_intentar = [
            'Microsoft Access Driver (*.mdb, *.accdb)',
            'Microsoft Access Driver (*.mdb)',
            'Driver do Microsoft Access (*.mdb, *.accdb)',
            'Driver do Microsoft Access (*.mdb)',
        ]

        for driver in drivers_a_intentar:
            try:
                conn_string = f'DRIVER={{{driver}}};DBQ={db_path}'
                conn = pyodbc.connect(conn_string, timeout=5)
                conectado = True
                driver_usado = driver
                conn.close()
                break
            except Exception as e:
                continue

        if conectado:
            print(f"   ✓✓✓ CONEXION EXITOSA")
            print(f"       Driver usado: {driver_usado}")
            print()
            print("   >> El sistema puede leer Access directamente")
        else:
            print(f"   [X] NO se pudo conectar a Access")
            print()
            print("   CAUSA PROBABLE:")
            print("      - Incompatibilidad Python x64 vs ODBC x32")
            print("      - Access esta bloqueado por otro usuario")
            print("      - Permisos insuficientes en la red")

print()

# ============================================================================
# 6. RECOMENDACIONES
# ============================================================================
print("[6] RECOMENDACIONES")
print("="*70)

if pyodbc_disponible and 'conectado' in locals() and conectado:
    print()
    print("   ✓✓✓ TODO ESTA CONFIGURADO CORRECTAMENTE")
    print()
    print("   Puedes ejecutar: INICIAR_SISTEMA.bat")
    print()
else:
    print()
    print("   SOLUCION 1 (RECOMENDADA - Sin permisos admin):")
    print("   ------------------------------------------------")
    print("   Usa Python Portable 32 bits:")
    print()
    print("   1. Descarga WinPython 32 bits desde:")
    print("      https://winpython.github.io/")
    print()
    print("   2. Extrae en la carpeta del proyecto")
    print()
    print("   3. Instala pyodbc, pandas, plotly en ese Python")
    print()
    print("   4. Modifica INICIAR_SISTEMA.bat para usar ese Python")
    print()
    print()
    print("   SOLUCION 2 (Requiere administrador):")
    print("   --------------------------------------")
    print("   Pide al administrador que instale:")
    if bits_python == 64:
        print("   - AccessDatabaseEngine_X64.exe")
        print("     (Driver ODBC x64 para coincidir con Python x64)")
    else:
        print("   - Office 32 bits (ya incluye driver ODBC x32)")
    print()
    print()
    print("   SOLUCION 3 (Modo manual):")
    print("   --------------------------")
    print("   El sistema puede funcionar SIN leer Access:")
    print()
    print("   1. Exporta manualmente las tablas a CSV desde Access")
    print("   2. Colocalos en la carpeta: datos_csv\\")
    print("   3. El sistema usara esos CSV automaticamente")
    print()

print()
print("="*70)
input("Presiona Enter para cerrar...")
