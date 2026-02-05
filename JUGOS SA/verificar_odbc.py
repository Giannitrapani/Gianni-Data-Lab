# ============================================================================
# VERIFICADOR DE DRIVERS ODBC - JUGOS S.A.
# ============================================================================
# Este script muestra todos los drivers ODBC instalados en el sistema
# ============================================================================

import pyodbc
import sys

print("="*70)
print("VERIFICADOR DE DRIVERS ODBC - JUGOS S.A.")
print("="*70)
print()

print("Drivers ODBC instalados en este sistema:")
print("-"*70)

drivers = pyodbc.drivers()

if not drivers:
    print("   [!] NO se encontraron drivers ODBC instalados")
    print()
    print("SOLUCIÓN:")
    print("   Instala: Microsoft Access Database Engine 2016 Redistributable")
    print("   Enlace: https://www.microsoft.com/en-us/download/details.aspx?id=54920")
    print()
else:
    for i, driver in enumerate(drivers, 1):
        print(f"   [{i}] {driver}")

        # Marcar si es driver de Access
        if "access" in driver.lower():
            print("       ^^ DRIVER DE ACCESS ENCONTRADO ^^")

print()
print("-"*70)

# Verificar compatibilidad con Access
print()
print("Verificando compatibilidad con Access:")
print("-"*70)

access_drivers = [d for d in drivers if "access" in d.lower()]

if access_drivers:
    print(f"   OK - {len(access_drivers)} driver(s) de Access disponible(s)")
    for driver in access_drivers:
        print(f"      - {driver}")
else:
    print("   [!] NO se encontró driver de Access")
    print()
    print("   El sistema NO podrá leer archivos .accdb")
    print("   Instala el driver desde el enlace mencionado arriba")

print()
print("="*70)
print()

# Información del sistema
import platform
print(f"Sistema operativo: {platform.system()} {platform.release()}")
print(f"Arquitectura: {platform.architecture()[0]}")
print(f"Python versión: {sys.version.split()[0]}")
print(f"pyodbc versión: {pyodbc.version}")
print()

print("="*70)
input("Presiona Enter para cerrar...")
