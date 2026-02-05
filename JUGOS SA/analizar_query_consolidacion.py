# ============================================================================
# ANALIZADOR DE QUERY CONSOLIDACION - Access Database
# ============================================================================
# Este script analiza el query CONSOLIDACION en Access para ver si puede
# reemplazar las 2 tablas separadas (TBL_Lbascular y TBL_basculae)

import pyodbc
import pandas as pd
from datetime import datetime

print("="*70)
print("ANALIZADOR DE QUERY CONSOLIDACION")
print("="*70)
print()

# Ruta de la base de datos
DB_PATH = r"C:\Users\giann\Desktop\JUGOS-CLAUDE\datos_fuente\VerDatosGaspar-local.accdb"

# Conectar a Access
print("Conectando a Access...")

# Intentar diferentes drivers ODBC
drivers = [
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};',
    r'DRIVER={Microsoft Access Driver (*.mdb)};',
]

conn_str = None
for driver in drivers:
    try:
        test_str = driver + f'DBQ={DB_PATH};'
        test_conn = pyodbc.connect(test_str, timeout=5)
        test_conn.close()
        conn_str = test_str
        print(f"   OK Driver encontrado: {driver.split('{')[1].split('}')[0]}")
        break
    except:
        continue

if not conn_str:
    print("   ERROR: No se encontro driver ODBC compatible")
    print("   Drivers intentados:")
    for d in drivers:
        print(f"      - {d.split('{')[1].split('}')[0]}")
    exit(1)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("   OK Conexion establecida")
    print()

    # ========================================================================
    # PASO 1: Listar todos los queries disponibles
    # ========================================================================
    print("PASO 1: Listando todos los queries disponibles...")
    print("-" * 70)

    queries_info = []
    for table_info in cursor.tables(tableType='VIEW'):
        queries_info.append(table_info.table_name)

    if queries_info:
        print(f"   Se encontraron {len(queries_info)} queries:")
        for i, qname in enumerate(queries_info, 1):
            print(f"   {i}. {qname}")
    else:
        print("   No se encontraron queries")
    print()

    # ========================================================================
    # PASO 2: Verificar si existe el query CONSOLIDACION
    # ========================================================================
    print("PASO 2: Verificando query CONSOLIDACION...")
    print("-" * 70)

    consolidacion_existe = 'CONSOLIDACION' in [q.upper() for q in queries_info]

    if consolidacion_existe:
        print("   ✓ Query CONSOLIDACION encontrado")
    else:
        print("   ✗ Query CONSOLIDACION NO encontrado")
        print("   Queries disponibles (case-insensitive):")
        for q in queries_info:
            if 'CONSOL' in q.upper():
                print(f"      - {q}")
    print()

    # ========================================================================
    # PASO 3: Analizar estructura del query CONSOLIDACION
    # ========================================================================
    if consolidacion_existe:
        print("PASO 3: Analizando estructura del query CONSOLIDACION...")
        print("-" * 70)

        # Buscar el nombre exacto (puede tener diferente capitalización)
        query_name = None
        for q in queries_info:
            if q.upper() == 'CONSOLIDACION':
                query_name = q
                break

        # Obtener columnas
        print(f"   Columnas del query '{query_name}':")
        columns = []
        for column in cursor.columns(table=query_name):
            col_name = column.column_name
            col_type = column.type_name
            columns.append((col_name, col_type))
            print(f"      - {col_name} ({col_type})")

        print()
        print(f"   Total columnas: {len(columns)}")
        print()

        # ====================================================================
        # PASO 4: Ejecutar query y ver primeros registros
        # ====================================================================
        print("PASO 4: Ejecutando query y mostrando datos de ejemplo...")
        print("-" * 70)

        query = f"SELECT * FROM [{query_name}] ORDER BY FECHA"
        df = pd.read_sql(query, conn)

        print(f"   Total de registros: {len(df):,}")
        print()

        # Mostrar info del DataFrame
        print("   Información del DataFrame:")
        print(f"      - Columnas: {list(df.columns)}")
        print(f"      - Tipos de datos:")
        for col in df.columns:
            print(f"        {col}: {df[col].dtype}")
        print()

        # Estadísticas básicas
        print("   Estadísticas básicas:")
        if 'FECHA' in df.columns:
            print(f"      - Fecha mínima: {df['FECHA'].min()}")
            print(f"      - Fecha máxima: {df['FECHA'].max()}")
        if 'CANTIDAD' in df.columns:
            print(f"      - Total cantidad: {df['CANTIDAD'].sum():,.0f}")
            print(f"      - Cantidad promedio: {df['CANTIDAD'].mean():.2f}")
        if 'MOVIMIENTO' in df.columns:
            print(f"      - Tipos de movimiento:")
            movimientos = df['MOVIMIENTO'].value_counts()
            for mov, count in movimientos.items():
                print(f"        {mov}: {count:,} registros ({count/len(df)*100:.1f}%)")
        if 'TABLA_ORIGEN' in df.columns:
            print(f"      - Origen de datos:")
            origenes = df['TABLA_ORIGEN'].value_counts()
            for origen, count in origenes.items():
                print(f"        {origen}: {count:,} registros ({count/len(df)*100:.1f}%)")
        print()

        # Primeros 10 registros
        print("   Primeros 10 registros:")
        print(df.head(10).to_string(index=False))
        print()

        # Últimos 10 registros
        print("   Últimos 10 registros:")
        print(df.tail(10).to_string(index=False))
        print()

        # ====================================================================
        # PASO 5: Comparar con las tablas originales
        # ====================================================================
        print("PASO 5: Comparando con tablas originales...")
        print("-" * 70)

        # Contar registros en tablas originales
        query_bascular = "SELECT COUNT(*) as total FROM TBL_Lbascular_formato_final"
        query_basculae = "SELECT COUNT(*) as total FROM TBL_basculae_formato_final"

        count_bascular = pd.read_sql(query_bascular, conn)['total'].iloc[0]
        count_basculae = pd.read_sql(query_basculae, conn)['total'].iloc[0]
        count_consolidado = len(df)

        print(f"   TBL_Lbascular_formato_final: {count_bascular:,} registros")
        print(f"   TBL_basculae_formato_final: {count_basculae:,} registros")
        print(f"   CONSOLIDACION (query): {count_consolidado:,} registros")
        print()

        suma_tablas = count_bascular + count_basculae
        diferencia = count_consolidado - suma_tablas

        if diferencia == 0:
            print(f"   ✓ PERFECTO: Query consolidado tiene EXACTAMENTE la suma de ambas tablas")
            print(f"     ({count_bascular:,} + {count_basculae:,} = {count_consolidado:,})")
        elif abs(diferencia) < 10:
            print(f"   ⚠ ADVERTENCIA: Diferencia menor detectada: {diferencia:+,} registros")
            print(f"     Suma de tablas: {suma_tablas:,}")
            print(f"     Query consolidado: {count_consolidado:,}")
        else:
            print(f"   ✗ ERROR: Diferencia significativa: {diferencia:+,} registros")
            print(f"     Suma de tablas: {suma_tablas:,}")
            print(f"     Query consolidado: {count_consolidado:,}")
        print()

        # ====================================================================
        # PASO 6: Verificar columnas necesarias para Stock y Proveedores
        # ====================================================================
        print("PASO 6: Verificando columnas necesarias...")
        print("-" * 70)

        columnas_necesarias = [
            'FECHA',
            'CANTIDAD',
            'MOVIMIENTO',
            'TABLA_ORIGEN',
            'PROVEEDOR',
            'NOMBRE',
            'FVO'  # Para bins llenos en planta
        ]

        columnas_faltantes = []
        columnas_presentes = []

        for col_necesaria in columnas_necesarias:
            if col_necesaria in df.columns:
                columnas_presentes.append(col_necesaria)
                print(f"   ✓ {col_necesaria}: Presente")
            else:
                columnas_faltantes.append(col_necesaria)
                print(f"   ✗ {col_necesaria}: FALTANTE")

        print()

        if len(columnas_faltantes) == 0:
            print("   ✓✓✓ EXCELENTE: Todas las columnas necesarias están presentes")
            print()
            print("="*70)
            print("CONCLUSIÓN: El query CONSOLIDACION es COMPATIBLE")
            print("="*70)
            print()
            print("Beneficios de usar el query CONSOLIDACION:")
            print("   1. ✓ Una sola lectura a Access (más rápido)")
            print("   2. ✓ Datos ya ordenados por fecha")
            print("   3. ✓ Menos carga en disco/red")
            print("   4. ✓ Más eficiente para actualizaciones automáticas")
            print("   5. ✓ Consistencia garantizada entre dashboards")
            print()
            print("Siguiente paso:")
            print("   → Modificar cargar_datos_universal.py para usar CONSOLIDACION")
            print("   → Simplificar la función cargar_movimientos_bins()")
            print()
        else:
            print(f"   ✗ FALTAN {len(columnas_faltantes)} columnas necesarias:")
            for col in columnas_faltantes:
                print(f"      - {col}")
            print()
            print("   → Necesitas agregar estas columnas al query CONSOLIDACION")

    else:
        print("   No se puede analizar - query no encontrado")

    # Cerrar conexión
    conn.close()
    print()
    print("Análisis completado.")
    print("="*70)

except Exception as e:
    print(f"✗ ERROR: {str(e)}")
    print()
    import traceback
    traceback.print_exc()
