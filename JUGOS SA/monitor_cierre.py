# ============================================================================
# MONITOR DE CIERRE AUTOMÁTICO - JUGOS S.A.
# ============================================================================
# Este script monitorea el navegador y detiene el servicio automáticamente
# cuando el usuario cierra el navegador
# ============================================================================

import time
import subprocess
import sys
import os

def navegador_esta_abierto():
    """Verifica si hay navegadores abiertos con el dashboard"""
    try:
        # Verificar Edge
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq msedge.exe', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            shell=True
        )
        if 'msedge.exe' in result.stdout:
            return True

        # Verificar Chrome
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq chrome.exe', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            shell=True
        )
        if 'chrome.exe' in result.stdout:
            return True

        # Verificar Firefox
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq firefox.exe', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            shell=True
        )
        if 'firefox.exe' in result.stdout:
            return True

        return False
    except:
        return False

def detener_servicio():
    """Detiene el servicio de actualización y el monitor"""
    try:
        # Obtener PID propio para no matarse a sí mismo aún
        mi_pid = os.getpid()

        # Matar todos los procesos Python relacionados con servicio_actualizacion
        subprocess.run(
            ['taskkill', '/F', '/IM', 'python.exe', '/FI', 'WINDOWTITLE eq *servicio_actualizacion*'],
            capture_output=True,
            shell=True
        )
        subprocess.run(
            ['taskkill', '/F', '/IM', 'pythonw.exe', '/FI', 'STATUS eq running'],
            capture_output=True,
            shell=True
        )

        # Pequeña pausa para asegurar que se cerraron
        time.sleep(1)

        return True
    except:
        return False

# Esperar 5 segundos para que el navegador termine de abrir
time.sleep(5)

# Monitorear cada 3 segundos
while True:
    if not navegador_esta_abierto():
        # Navegador cerrado - detener todos los servicios
        try:
            # Ejecutar script VBS para matar procesos
            script_dir = os.path.dirname(os.path.abspath(__file__))
            vbs_path = os.path.join(script_dir, 'detener_servicios_forzado.vbs')
            subprocess.run(['cscript', '//nologo', vbs_path], capture_output=True, shell=True)
        except:
            pass

        # Detener servicio con método alternativo
        detener_servicio()

        # Terminar este monitor
        sys.exit(0)

    # Esperar 3 segundos antes de verificar de nuevo
    time.sleep(3)
