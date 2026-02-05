# ============================================================================
# SERVICIO DE ACTUALIZACIÓN AUTOMÁTICA - JUGOS S.A.
# ============================================================================
# Este servicio actualiza automáticamente los dashboards cada hora
# ============================================================================

import subprocess
import sys
import os
import time
from datetime import datetime

print("="*70)
print("SERVICIO DE ACTUALIZACION AUTOMATICA - JUGOS S.A.")
print("="*70)
print()

# Obtener directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Intervalo de actualización (en segundos)
INTERVALO_ACTUALIZACION = 3600  # 1 hora = 3600 segundos

def actualizar_sistema():
    """Ejecuta la actualización completa del sistema"""
    print()
    print("="*70)
    print(f"INICIANDO ACTUALIZACION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()

    # 0. Detectar configuración (usa auto_config.json si existe)
    python_cmd = sys.executable
    modo = "ACCESS"

    try:
        import json
        if os.path.exists('auto_config.json'):
            with open('auto_config.json', 'r') as f:
                config = json.load(f)
                python_cmd = config.get('python_exe', sys.executable)
                modo = "CSV" if not config.get('compatible', True) else "ACCESS"
    except:
        pass

    # 1. Exportar CONSOLIDACION desde Access (VBA)
    if modo == "ACCESS":
        print("[1/3] Exportando query CONSOLIDACION desde Access (VBA)...")
        try:
            resultado = subprocess.run(
                ["EXPORTAR_CONSOLIDACION.bat"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=script_dir,
                shell=True
            )

            if resultado.returncode == 0:
                print("   OK - CONSOLIDACION exportado")
            else:
                print("   ADVERTENCIA - Fallo al exportar CONSOLIDACION (usando datos existentes)")
        except Exception as e:
            print(f"   ADVERTENCIA: {str(e)} (usando datos existentes)")
    else:
        print("[1/3] Modo CSV - Omitiendo exportación CONSOLIDACION")

    # 2. Actualizar otros CSV desde Access (solo si modo ACCESS)
    if modo == "ACCESS":
        print()
        print("[2/3] Actualizando otras tablas desde Access...")
        try:
            resultado = subprocess.run(
                [python_cmd, "ACTUALIZAR_CSV.py"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=script_dir
            )

            if resultado.returncode == 0:
                print("   OK - Otras tablas actualizadas")
            else:
                print("   INFO - Usando datos CSV existentes")
        except Exception as e:
            print(f"   ERROR: {str(e)}")
    else:
        print()
        print("[2/3] Modo CSV - Omitiendo actualización desde Access")
        print("   INFO - Usando CSV existentes")

    # 3. Regenerar dashboards
    print()
    print("[3/3] Regenerando dashboards...")
    try:
        resultado = subprocess.run(
            [python_cmd, "actualizar_dashboard_completo.py"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=script_dir
        )

        if resultado.returncode == 0:
            print("   OK - Dashboards actualizados")
        else:
            print("   ERROR - Fallo al actualizar dashboards")
            print(resultado.stderr)
    except Exception as e:
        print(f"   ERROR: {str(e)}")

    print()
    print("="*70)
    print(f"ACTUALIZACION COMPLETADA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Proxima actualizacion: {datetime.fromtimestamp(time.time() + INTERVALO_ACTUALIZACION).strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

# Realizar primera actualización al iniciar
actualizar_sistema()

# Bucle infinito de actualización
print()
print("Servicio iniciado. Actualizando cada 1 hora...")
print("Presiona Ctrl+C para detener el servicio")
print()

try:
    while True:
        # Esperar 1 hora
        time.sleep(INTERVALO_ACTUALIZACION)

        # Actualizar sistema
        actualizar_sistema()

except KeyboardInterrupt:
    print()
    print("="*70)
    print("SERVICIO DETENIDO POR EL USUARIO")
    print("="*70)
    sys.exit(0)
