# ============================================================================
# SCRIPT MAESTRO - ACTUALIZAR DASHBOARD COMPLETO - JUGOS S.A.
# ============================================================================

import subprocess
import sys
import os

print("="*70)
print("ACTUALIZACION COMPLETA DEL DASHBOARD - JUGOS S.A.")
print("="*70)
print()

# Obtener directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))

scripts = [
    ("generar_dashboard.py", "Dashboard de Stock Global", "dashboard.html"),
    ("generar_pagina_proveedores.py", "Pagina de Proveedores", "proveedores.html"),
    ("generar_analisis_logistico.py", "Analisis Logistico", "logistica.html")
]

exitosos = 0
errores = 0

for script, nombre, html_file in scripts:
    print(f"Ejecutando: {nombre}...")
    print("-"*70)

    try:
        script_path = os.path.join(script_dir, script)
        html_path = os.path.join(script_dir, html_file)

        # Guardar timestamp del HTML antes
        html_mtime_antes = os.path.getmtime(html_path) if os.path.exists(html_path) else 0

        # Ejecutar script
        subprocess.run(
            [sys.executable, script_path],
            cwd=script_dir,
            timeout=300
        )

        # Verificar si el HTML se actualizo
        html_mtime_despues = os.path.getmtime(html_path) if os.path.exists(html_path) else 0

        if html_mtime_despues > html_mtime_antes:
            print(f"   OK {nombre} actualizado correctamente")
            exitosos += 1
        else:
            print(f"   ERROR en {nombre}")
            errores += 1

    except Exception as e:
        print(f"   ERROR: {str(e)}")
        errores += 1

    print()

print("="*70)
print("RESUMEN DE ACTUALIZACION")
print("="*70)
print()
print(f"   Exitosos: {exitosos}/{len(scripts)}")
print(f"   Errores:  {errores}/{len(scripts)}")
print()

if errores == 0:
    print("OK Dashboard completo actualizado exitosamente!")

    from datetime import datetime
    with open(os.path.join(script_dir, "ultima_actualizacion.txt"), "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print()
    print("Para ver el dashboard:")
    print("   Abre: dashboard_completo.html")
else:
    print("ADVERTENCIA: Algunos componentes no se actualizaron correctamente")
    print()

print("="*70)
