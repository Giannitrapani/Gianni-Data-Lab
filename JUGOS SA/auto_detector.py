# ============================================================================
# AUTO-DETECTOR INTELIGENTE V4 - JUGOS S.A.
# ============================================================================
# NUEVO: Prueba REAL de conexión con Access
# No asume nada - PRUEBA cada Python contra el archivo .accdb real
# ============================================================================

import sys
import os
import struct
import subprocess
import json

# ============================================================================
# FUNCIONES DE DETECCIÓN
# ============================================================================

def detectar_python_bits():
    """Detecta si este Python es 32 o 64 bits"""
    return struct.calcsize("P") * 8

def buscar_pythons_instalados():
    """Busca todas las instalaciones de Python disponibles"""
    pythons = []
    rutas_vistas = set()

    # Python actual (el que ejecuta este script)
    ruta_actual = sys.executable
    pythons.append({
        'ruta': ruta_actual,
        'version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'bits': detectar_python_bits(),
        'tipo': 'sistema (actual)'
    })
    rutas_vistas.add(ruta_actual.lower())

    # Buscar Python en PATH
    try:
        result = subprocess.run(['where', 'python'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            for ruta in result.stdout.strip().split('\n'):
                ruta = ruta.strip()
                if ruta and ruta.lower() not in rutas_vistas:
                    try:
                        # Obtener bits de este Python
                        cmd = f'"{ruta}" -c "import struct; print(struct.calcsize(\'P\') * 8)"'
                        bits_result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=5)
                        if bits_result.returncode == 0:
                            bits = int(bits_result.stdout.strip())
                            pythons.append({
                                'ruta': ruta,
                                'version': 'desconocida',
                                'bits': bits,
                                'tipo': 'sistema (PATH)'
                            })
                            rutas_vistas.add(ruta.lower())
                    except:
                        pass
    except:
        pass

    # Buscar en ubicaciones comunes
    ubicaciones_comunes = [
        r'C:\Python27\python.exe',
        r'C:\Python32\python.exe',
        r'C:\Python36\python.exe',
        r'C:\Python37\python.exe',
        r'C:\Python38\python.exe',
        r'C:\Python39\python.exe',
        r'C:\Python310\python.exe',
        r'C:\Python311\python.exe',
        r'C:\Python312\python.exe',
    ]

    for ruta in ubicaciones_comunes:
        if os.path.exists(ruta) and ruta.lower() not in rutas_vistas:
            try:
                cmd = f'"{ruta}" -c "import struct; print(struct.calcsize(\'P\') * 8)"'
                bits_result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=5)
                if bits_result.returncode == 0:
                    bits = int(bits_result.stdout.strip())
                    pythons.append({
                        'ruta': ruta,
                        'version': 'desconocida',
                        'bits': bits,
                        'tipo': 'sistema (ubicación común)'
                    })
                    rutas_vistas.add(ruta.lower())
            except:
                pass

    # Buscar WinPython portable en la carpeta actual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        for item in os.listdir(script_dir):
            item_path = os.path.join(script_dir, item)
            if os.path.isdir(item_path) and ('WPy' in item or 'python' in item.lower()):
                # Buscar python.exe dentro
                python_exe = None

                # Buscar en raíz
                if os.path.exists(os.path.join(item_path, 'python.exe')):
                    python_exe = os.path.join(item_path, 'python.exe')
                else:
                    # Buscar en subdirectorios python-*
                    try:
                        for subdir in os.listdir(item_path):
                            if subdir.startswith('python-') or subdir.lower() == 'python':
                                candidate = os.path.join(item_path, subdir, 'python.exe')
                                if os.path.exists(candidate):
                                    python_exe = candidate
                                    break
                    except:
                        pass

                if python_exe and python_exe.lower() not in rutas_vistas:
                    try:
                        cmd = f'"{python_exe}" -c "import struct; print(struct.calcsize(\'P\') * 8)"'
                        bits_result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=5)
                        if bits_result.returncode == 0:
                            bits = int(bits_result.stdout.strip())
                            pythons.append({
                                'ruta': python_exe,
                                'version': 'portable',
                                'bits': bits,
                                'tipo': f'portable ({item})'
                            })
                            rutas_vistas.add(python_exe.lower())
                    except:
                        pass
    except:
        pass

    return pythons

def probar_conexion_access(python_exe, db_path):
    """
    Prueba REAL: intenta conectar con Access usando este Python
    Retorna True si puede conectarse, False si no
    """
    # Crear script de prueba en archivo temporal para evitar problemas con escapes
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_temp = os.path.join(script_dir, '_test_connection.py')

    script_content = f"""import sys
import pyodbc

drivers = [
    'Microsoft Access Driver (*.mdb, *.accdb)',
    'Driver do Microsoft Access (*.mdb, *.accdb)',
    'Controlador de Microsoft Access (*.mdb, *.accdb)',
    'Microsoft Access Driver (*.mdb)',
]

db_path = r'{db_path}'

for driver in drivers:
    try:
        conn_string = 'DRIVER={{' + driver + '}};DBQ=' + db_path
        conn = pyodbc.connect(conn_string, timeout=3)
        conn.close()
        print("OK")
        sys.exit(0)
    except Exception as e:
        continue

print("FAIL")
sys.exit(1)
"""

    try:
        # Escribir script temporal
        with open(script_temp, 'w') as f:
            f.write(script_content)

        # Ejecutar script
        result = subprocess.run(
            [python_exe, script_temp],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=script_dir
        )

        # Limpiar archivo temporal
        try:
            os.remove(script_temp)
        except:
            pass

        output = result.stdout.strip()

        if output == "OK":
            return True, "Puede conectar con Access"
        elif "ModuleNotFoundError" in result.stderr or "No module named 'pyodbc'" in result.stderr:
            return False, "No tiene pyodbc instalado"
        else:
            return False, "No puede conectar (driver incompatible)"

    except subprocess.TimeoutExpired:
        try:
            os.remove(script_temp)
        except:
            pass
        return False, "Timeout al probar conexión"
    except Exception as e:
        try:
            os.remove(script_temp)
        except:
            pass
        return False, f"Error: {str(e)}"

def encontrar_mejor_python(pythons, db_path):
    """
    Prueba cada Python para ver cuál puede conectarse realmente con Access
    """
    resultados = []

    for python in pythons:
        puede_conectar, mensaje = probar_conexion_access(python['ruta'], db_path)

        resultado = {
            'python': python,
            'puede_conectar': puede_conectar,
            'mensaje': mensaje
        }
        resultados.append(resultado)

        # Si encontramos uno que funciona, ese es el bueno
        if puede_conectar:
            return resultado, resultados

    # Ninguno pudo conectar
    return None, resultados

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("AUTO-DETECTOR INTELIGENTE V4 - JUGOS S.A.")
    print("="*70)
    print()

    # Ubicar archivo Access
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'datos_fuente', 'VerDatosGaspar-local.accdb')

    if not os.path.exists(db_path):
        print(f"ERROR: No se encuentra el archivo Access")
        print(f"Ruta esperada: {db_path}")
        print()
        sys.exit(1)

    print(f"Archivo Access: {os.path.basename(db_path)}")
    print()

    # Buscar Pythons
    print("[1/2] Buscando instalaciones de Python...")
    pythons = buscar_pythons_instalados()

    print(f"   Encontrados: {len(pythons)} instalación(es)")
    for i, py in enumerate(pythons, 1):
        print(f"   [{i}] Python {py['bits']} bits - {py['tipo']}")
        print(f"       {py['ruta']}")

    print()

    # Probar cada Python
    print("[2/2] Probando conexión REAL con Access...")
    print()

    mejor, resultados = encontrar_mejor_python(pythons, db_path)

    # Mostrar resultados de cada prueba
    for i, res in enumerate(resultados, 1):
        py = res['python']
        simbolo = "[OK]" if res['puede_conectar'] else "[X]"
        print(f"   [{i}] Python {py['bits']} bits {simbolo}")
        print(f"       {res['mensaje']}")

    print()
    print("="*70)

    if mejor:
        py = mejor['python']
        print("RESULTADO: Sistema puede leer Access directamente")
        print("="*70)
        print()
        print(f"Python seleccionado:")
        print(f"   Ruta: {py['ruta']}")
        print(f"   Bits: {py['bits']}")
        print(f"   Tipo: {py['tipo']}")
        print()

        # Guardar configuración
        config = {
            'python_exe': py['ruta'],
            'python_bits': py['bits'],
            'python_tipo': py['tipo'],
            'compatible': True,
            'mensaje': f"Python {py['bits']} bits puede leer Access"
        }

        config_path = os.path.join(script_dir, 'auto_config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"Configuración guardada: auto_config.json")
        print("="*70)
        sys.exit(0)
    else:
        print("RESULTADO: Ningún Python puede leer Access")
        print("="*70)
        print()
        print("CAUSAS POSIBLES:")
        print("  1. No tienes driver ODBC para .accdb instalado")
        print("  2. Python y ODBC son de arquitecturas incompatibles")
        print("  3. pyodbc no está instalado en ningún Python")
        print()
        print("SOLUCIONES:")
        print("  A. Instala Python 64 bits (si tienes Office 64)")
        print("  B. Instala Python 32 bits (si tienes Office 32)")
        print("  C. Descarga WinPython portable y colócalo en esta carpeta")
        print("  D. Usa modo CSV (exporta tablas manualmente)")
        print()

        # Usar primer Python para modo CSV
        if pythons:
            config = {
                'python_exe': pythons[0]['ruta'],
                'python_bits': pythons[0]['bits'],
                'compatible': False,
                'mensaje': 'Modo CSV - No puede leer Access',
                'modo': 'csv'
            }

            config_path = os.path.join(script_dir, 'auto_config.json')
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)

            print("Sistema configurado en MODO CSV")
            print("Exporta las tablas manualmente a: datos_csv\\")

        print("="*70)
        sys.exit(1)
