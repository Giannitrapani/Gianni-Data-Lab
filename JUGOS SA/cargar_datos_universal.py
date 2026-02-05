"""
Sistema INTELIGENTE que detecta automáticamente:
- Python 32-bit o 64-bit
- ODBC disponible
- Fallback a CSV si no puede leer Access

¡FUNCIONA SIEMPRE, SIN CONFIGURACIÓN!
"""

import pandas as pd
import platform
import os
import json
import sys
import struct

def detectar_arquitectura():
    """Detecta si Python es 32 o 64 bits"""
    bits = struct.calcsize("P") * 8
    return bits

def obtener_ruta_base_datos():
    """Obtiene ruta de la base de datos desde config.json"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        ruta_config = config.get('sistema', {}).get('ruta_base_datos', 'auto')

        if ruta_config == 'auto':
            ruta_bd = os.path.join(script_dir, "datos_fuente", "VerDatosGaspar-local.accdb")
        else:
            ruta_bd = ruta_config

        return ruta_bd
    except Exception as e:
        print(f"[WARN] Error leyendo config: {e}")
        return os.path.join(script_dir, "datos_fuente", "VerDatosGaspar-local.accdb")

def intentar_conectar_access():
    """
    Intenta conectar a Access.
    Devuelve (exito, mensaje, driver_usado)
    """
    try:
        import pyodbc
    except ImportError:
        return False, "pyodbc no instalado", None

    ARCHIVO_ACCESS = obtener_ruta_base_datos()

    if not os.path.exists(ARCHIVO_ACCESS):
        return False, f"Archivo no existe: {ARCHIVO_ACCESS}", None

    # Detectar drivers disponibles
    drivers_disponibles = pyodbc.drivers()

    # Buscar drivers de Access (prioridad a .accdb)
    drivers_access = [
        "Microsoft Access Driver (*.mdb, *.accdb)",  # Ideal
        "Microsoft Access Driver (*.mdb)",           # Solo .mdb
        "Driver do Microsoft Access (*.mdb)",        # Portugués
        "Microsoft Access-Treiber (*.mdb)",          # Alemán
    ]

    driver_usar = None
    for driver in drivers_access:
        if driver in drivers_disponibles:
            driver_usar = driver
            break

    if not driver_usar:
        return False, "No hay driver ODBC de Access instalado", None

    # Intentar conectar
    try:
        connection_string = f"DRIVER={{{driver_usar}}};DBQ={ARCHIVO_ACCESS};"
        conn = pyodbc.connect(connection_string)
        conn.close()
        return True, "Conexión exitosa", driver_usar
    except Exception as e:
        return False, f"Error al conectar: {str(e)}", driver_usar

def cargar_tabla(nombre_tabla):
    """
    FUNCIÓN UNIVERSAL - Intenta múltiples métodos automáticamente:
    1. Leer desde Access con ODBC
    2. Leer desde CSV (fallback)
    """

    print(f"[INFO] Cargando tabla: {nombre_tabla}")
    print(f"[INFO] Python {detectar_arquitectura()}-bit")

    # MÉTODO 1: Intentar leer desde Access
    exito_access, mensaje, driver = intentar_conectar_access()

    if exito_access:
        try:
            import pyodbc
            ARCHIVO_ACCESS = obtener_ruta_base_datos()
            connection_string = f"DRIVER={{{driver}}};DBQ={ARCHIVO_ACCESS};"
            conn = pyodbc.connect(connection_string)

            # Leer tabla
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM [{nombre_tabla}]')
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            df = pd.DataFrame.from_records(rows, columns=columns)
            conn.close()

            # Convertir Decimal a float
            for col in df.columns:
                if df[col].dtype == 'object':
                    try:
                        import decimal
                        if len(df) > 0 and isinstance(df[col].iloc[0], decimal.Decimal):
                            df[col] = df[col].astype(float)
                    except:
                        pass

            print(f"[OK] Cargados {len(df):,} registros desde Access usando driver: {driver}")
            return df

        except Exception as e:
            print(f"[WARN] Error leyendo Access: {e}")
            print(f"[INFO] Intentando leer desde CSV...")
    else:
        print(f"[WARN] No se pudo conectar a Access: {mensaje}")
        print(f"[INFO] Intentando leer desde CSV...")

    # MÉTODO 2: Leer desde CSV (fallback)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_csv = os.path.join(script_dir, "datos_csv", f"{nombre_tabla}.csv")

    if not os.path.exists(archivo_csv):
        raise FileNotFoundError(
            f"\n\n"
            f"════════════════════════════════════════════════════════\n"
            f"ERROR: No se pudo cargar la tabla '{nombre_tabla}'\n"
            f"════════════════════════════════════════════════════════\n"
            f"\n"
            f"No se encontró:\n"
            f"  - Base de datos Access con driver ODBC compatible\n"
            f"  - Archivo CSV: {archivo_csv}\n"
            f"\n"
            f"SOLUCIÓN:\n"
            f"  1. Ejecuta: EXPORTAR_CSV.bat (para crear archivos CSV)\n"
            f"  2. O instala driver Access 32-bit para leer .accdb\n"
            f"\n"
            f"════════════════════════════════════════════════════════\n"
        )

    df = pd.read_csv(archivo_csv)

    # Convertir columnas de fecha
    columnas_fecha = ['FECHA', 'FVO', 'Fecha']
    for col in columnas_fecha:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Convertir columnas numéricas
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass

    print(f"[OK] Cargados {len(df):,} registros desde CSV")
    return df


def cargar_movimientos_bins():
    """Carga movimientos de bins"""
    print("Cargando movimientos de bins...")

    # IMPORTANTE: Usar QUERIES DINAMICOS en lugar de tablas estáticas
    # Los queries leen de Lbascular/Lbasculae y se actualizan automáticamente
    df1 = cargar_tabla('10_qry_Lbascular_formato_final')
    df1['TABLA_ORIGEN'] = 'BASCULAR'

    df2 = cargar_tabla('11_qry_basculae_formato_final')
    df2['TABLA_ORIGEN'] = 'BASCULAE'

    df = pd.concat([df1, df2], ignore_index=True)
    df['MOVIMIENTO'] = df['MOVIMIENTO'].str.upper()

    if df['FECHA'].dtype == 'object':
        df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')

    fechas_invalidas = df['FECHA'].isna().sum()
    if fechas_invalidas > 0:
        print(f"   ADVERTENCIA: {fechas_invalidas} fechas inválidas, eliminando...")
        df = df.dropna(subset=['FECHA'])

    df = df.sort_values('FECHA').reset_index(drop=True)

    print(f"   Total: {len(df):,} movimientos")
    print(f"   Rango: {df['FECHA'].min()} a {df['FECHA'].max()}")

    return df


def cargar_ingresos_logistica():
    """Carga datos de logística"""
    print("Cargando datos de logística...")

    df = cargar_tabla('IngresosConKm')
    df_prov = cargar_tabla('LProveedor')

    if df['Fecha'].dtype == 'object':
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    fechas_invalidas = df['Fecha'].isna().sum()
    if fechas_invalidas > 0:
        print(f"   ADVERTENCIA: {fechas_invalidas} fechas inválidas, eliminando...")
        df = df.dropna(subset=['Fecha'])

    df['FechaDia'] = df['Fecha'].dt.date
    df = df[df['pro'].notna()].copy()

    df['pro'] = df['pro'].astype(int)
    df_prov['nro'] = df_prov['nro'].astype(int)
    df = df.merge(df_prov[['nro', 'nom']], left_on='pro', right_on='nro', how='left')
    df = df.rename(columns={'nom': 'NombreProveedor'})
    df = df.drop(columns=['nro'])

    print(f"   Ingresos: {len(df):,} registros")
    print(f"   Proveedores: {len(df_prov):,}")

    return df, df_prov


if __name__ == "__main__":
    """Test de funcionalidad"""
    print("\n" + "="*60)
    print("TEST DEL SISTEMA INTELIGENTE")
    print("="*60 + "\n")

    print(f"Python: {sys.version}")
    print(f"Arquitectura: {detectar_arquitectura()}-bit")
    print(f"Sistema: {platform.system()}")
    print()

    exito, mensaje, driver = intentar_conectar_access()
    print(f"Conexion Access: {'OK' if exito else 'FALLO'}")
    print(f"Mensaje: {mensaje}")
    if driver:
        print(f"Driver: {driver}")
    print()

    # Intentar cargar una tabla pequeña
    try:
        print("Probando carga de datos...")
        df = cargar_tabla('LProveedor')
        print(f"Exito: {len(df)} registros cargados")
    except Exception as e:
        print(f"Error: {e}")
