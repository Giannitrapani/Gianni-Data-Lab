import pyodbc
import pandas as pd
import os
import sys
import json

# ============================================================================
# ACTUALIZAR CSV DESDE ACCESS - COMPATIBLE x32 Y x64
# ============================================================================
# Lee las tablas originales de Access y las transforma al formato esperado
# ============================================================================

# Obtener ruta del script para rutas relativas
script_dir = os.path.dirname(os.path.abspath(__file__))

# Leer ruta de base de datos desde config.json
def obtener_ruta_base_datos():
    """Obtiene ruta de la base de datos desde config.json"""
    config_path = os.path.join(script_dir, "config.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        ruta_config = config.get('sistema', {}).get('ruta_base_datos', 'auto')
        if ruta_config == 'auto':
            return os.path.join(script_dir, "datos_fuente", "VerDatosGaspar-local.accdb")
        else:
            return ruta_config
    except Exception as e:
        print(f"[WARN] Error leyendo config: {e}")
        return os.path.join(script_dir, "datos_fuente", "VerDatosGaspar-local.accdb")

db_path = obtener_ruta_base_datos()

# Lista de drivers ODBC a intentar (x64 Y x32)
DRIVERS = [
    # Drivers x64 (Access Database Engine 2016)
    'Microsoft Access Driver (*.mdb, *.accdb)',
    'Driver do Microsoft Access (*.mdb, *.accdb)',
    'Controlador de Microsoft Access (*.mdb, *.accdb)',

    # Drivers x32 (viene con Office 32 bits)
    'Microsoft Access Driver (*.mdb)',
    'Driver do Microsoft Access (*.mdb)',
    'Controlador de Microsoft Access (*.mdb)',
]

conn = None
driver_usado = None

# Intentar conectar con cada driver disponible
for driver in DRIVERS:
    try:
        conn_string = f'DRIVER={{{driver}}};DBQ={db_path}'
        conn = pyodbc.connect(conn_string)
        driver_usado = driver
        break
    except:
        continue

if conn is None:
    print("ERROR: No se pudo conectar con ningun driver ODBC disponible")
    print("Drivers intentados:")
    for d in DRIVERS:
        print(f"  - {d}")
    sys.exit(1)

try:
    os.makedirs(os.path.join(script_dir, 'datos_csv'), exist_ok=True)

    exitosas = 0
    fallidas = 0
    errores = []

    # ========================================================================
    # 1. EXPORTAR TABLAS SIMPLES (sin transformacion)
    # ========================================================================
    tablas_simples = [
        'IngresosConKm',
        'LProveedor',
        'Lvariedad',
        'LTipo_Camion',
    ]

    for t in tablas_simples:
        try:
            df = pd.read_sql(f'SELECT * FROM [{t}]', conn)
            csv_path = os.path.join(script_dir, 'datos_csv', f'{t}.csv')
            df.to_csv(csv_path, index=False, encoding='utf-8')
            exitosas += 1
        except Exception as e:
            fallidas += 1
            errores.append(f"{t}: {str(e)}")

    # ========================================================================
    # 2. CARGAR TABLA DE PROVEEDORES PARA JOINS
    # ========================================================================
    try:
        df_proveedores = pd.read_sql("SELECT nro, nom FROM LProveedor", conn)
        df_proveedores.columns = ['PROVEEDOR', 'NOMBRE']
        df_proveedores['PROVEEDOR'] = df_proveedores['PROVEEDOR'].astype(float)
    except Exception as e:
        print(f"[WARN] No se pudo cargar proveedores: {e}")
        df_proveedores = pd.DataFrame(columns=['PROVEEDOR', 'NOMBRE'])

    # ========================================================================
    # 3. EXPORTAR QUERY DINAMICO -> TBL_Lbascular_formato_final.csv
    # ========================================================================
    try:
        # Leer desde QUERY DINAMICO (lee de Lbascular automaticamente)
        df_bascular = pd.read_sql("SELECT * FROM [10_qry_Lbascular_formato_final]", conn)

        # Guardar
        csv_path = os.path.join(script_dir, 'datos_csv', 'TBL_Lbascular_formato_final.csv')
        df_bascular.to_csv(csv_path, index=False, encoding='utf-8')
        exitosas += 1

    except Exception as e:
        fallidas += 1
        errores.append(f"TBL_Lbascular_formato_final: {str(e)}")

    # ========================================================================
    # 4. EXPORTAR QUERY DINAMICO -> TBL_basculae_formato_final.csv
    # ========================================================================
    try:
        # Leer desde QUERY DINAMICO (lee de Lbasculae automaticamente)
        df_basculae = pd.read_sql("SELECT * FROM [11_qry_basculae_formato_final]", conn)

        # Guardar
        csv_path = os.path.join(script_dir, 'datos_csv', 'TBL_basculae_formato_final.csv')
        df_basculae.to_csv(csv_path, index=False, encoding='utf-8')
        exitosas += 1

    except Exception as e:
        fallidas += 1
        errores.append(f"TBL_basculae_formato_final: {str(e)}")

    # ========================================================================
    # 5. CREAR CONSOLIDACION (union de Lbascular + Lbasculae)
    # ========================================================================
    try:
        # Leer ambas tablas ya procesadas
        df_bascular_csv = pd.read_csv(os.path.join(script_dir, 'datos_csv', 'TBL_Lbascular_formato_final.csv'))
        df_basculae_csv = pd.read_csv(os.path.join(script_dir, 'datos_csv', 'TBL_basculae_formato_final.csv'))

        # Agregar columna de origen
        df_bascular_csv['TABLA_ORIGEN'] = 'BASCULAR'
        df_basculae_csv['TABLA_ORIGEN'] = 'BASCULAE'

        # Unir
        df_consolidacion = pd.concat([df_bascular_csv, df_basculae_csv], ignore_index=True)

        # Ordenar por fecha
        df_consolidacion['FECHA'] = pd.to_datetime(df_consolidacion['FECHA'], errors='coerce')
        df_consolidacion = df_consolidacion.sort_values('FECHA')

        # Guardar
        csv_path = os.path.join(script_dir, 'datos_csv', 'CONSOLIDACION.csv')
        df_consolidacion.to_csv(csv_path, index=False, encoding='utf-8')
        exitosas += 1

    except Exception as e:
        fallidas += 1
        errores.append(f"CONSOLIDACION: {str(e)}")

    conn.close()

    if fallidas == 0:
        print("OK")
    else:
        print(f"PARCIAL: {exitosas} exitosas, {fallidas} fallidas")
        for error in errores:
            print(f"  - {error}")
        # No salir con error si al menos algunas tablas se exportaron
        if exitosas > 0:
            sys.exit(0)
        else:
            sys.exit(1)

except Exception as e:
    print(f"ERROR: {str(e)}")
    sys.exit(1)
