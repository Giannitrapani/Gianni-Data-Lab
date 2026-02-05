# Analizar query CONSOLIDACION usando el sistema existente
import pandas as pd
from cargar_datos_universal import cargar_tabla
import pyodbc
import os

print("="*70)
print("ANALISIS DEL QUERY CONSOLIDACION")
print("="*70)
print()

# Usar la misma conexión que el sistema actual
from cargar_datos_universal import intentar_conectar_access, obtener_ruta_base_datos

# Probar conexión
exito, mensaje, driver = intentar_conectar_access()

if not exito:
    print(f"ERROR: No se pudo conectar a Access: {mensaje}")
    exit(1)

print(f"Conectado exitosamente usando driver: {driver}")
print()

ARCHIVO_ACCESS = obtener_ruta_base_datos()
connection_string = f"DRIVER={{{driver}}};DBQ={ARCHIVO_ACCESS};"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Listar todas las tablas y queries
print("Listando objetos en la base de datos...")
print("-" * 70)

tablas = []
queries = []

for table_info in cursor.tables():
    nombre = table_info.table_name
    tipo = table_info.table_type

    if tipo == 'TABLE':
        tablas.append(nombre)
    elif tipo == 'VIEW':
        queries.append(nombre)

print(f"Tablas encontradas: {len(tablas)}")
for t in sorted(tablas):
    print(f"   - {t}")
print()

print(f"Queries encontrados: {len(queries)}")
for q in sorted(queries):
    print(f"   - {q}")
print()

# Buscar CONSOLIDACION
consolidacion_encontrado = False
nombre_query = None

for q in queries:
    if 'CONSOLIDACION' in q.upper() or 'CONSOLIDA' in q.upper():
        nombre_query = q
        consolidacion_encontrado = True
        print(f">>> Query encontrado: '{q}'")
        break

if not consolidacion_encontrado:
    print("ERROR: No se encontro query CONSOLIDACION")
    print()
    print("Queries disponibles que contienen 'CONSOL':")
    for q in queries:
        if 'CONSOL' in q.upper():
            print(f"   - {q}")
    conn.close()
    exit(1)

print()
print("="*70)
print(f"ANALIZANDO QUERY: {nombre_query}")
print("="*70)
print()

# Obtener estructura del query
print("Columnas del query:")
print("-" * 70)
cursor.execute(f"SELECT TOP 1 * FROM [{nombre_query}]")
columnas = [col[0] for col in cursor.description]
for i, col in enumerate(columnas, 1):
    print(f"   {i}. {col}")
print()

# Contar registros
print("Contando registros...")
cursor.execute(f"SELECT COUNT(*) FROM [{nombre_query}]")
count_consolidado = cursor.fetchone()[0]
print(f"   Query CONSOLIDACION: {count_consolidado:,} registros")
print()

# Contar registros en tablas originales
cursor.execute("SELECT COUNT(*) FROM TBL_Lbascular_formato_final")
count_bascular = cursor.fetchone()[0]
print(f"   TBL_Lbascular_formato_final: {count_bascular:,} registros")

cursor.execute("SELECT COUNT(*) FROM TBL_basculae_formato_final")
count_basculae = cursor.fetchone()[0]
print(f"   TBL_basculae_formato_final: {count_basculae:,} registros")
print()

suma_tablas = count_bascular + count_basculae
diferencia = count_consolidado - suma_tablas

print(f"   Suma de ambas tablas: {suma_tablas:,}")
print(f"   Query consolidado: {count_consolidado:,}")
print(f"   Diferencia: {diferencia:+,}")
print()

if diferencia == 0:
    print("   [OK] Coincidencia PERFECTA")
else:
    print(f"   [ADVERTENCIA] Hay {abs(diferencia)} registros de diferencia")
print()

# Leer datos de ejemplo
print("Cargando datos del query CONSOLIDACION...")
df = pd.read_sql(f"SELECT * FROM [{nombre_query}] ORDER BY FECHA", conn)
print(f"   OK - {len(df):,} registros cargados")
print()

# Estadisticas
print("Estadisticas del query:")
print("-" * 70)
if 'FECHA' in df.columns:
    print(f"   Fecha minima: {df['FECHA'].min()}")
    print(f"   Fecha maxima: {df['FECHA'].max()}")
if 'CANTIDAD' in df.columns:
    print(f"   Total cantidad: {df['CANTIDAD'].sum():,.0f}")
    print(f"   Promedio cantidad: {df['CANTIDAD'].mean():.2f}")
if 'MOVIMIENTO' in df.columns:
    print(f"   Movimientos:")
    for mov, count in df['MOVIMIENTO'].value_counts().items():
        print(f"      {mov}: {count:,} ({count/len(df)*100:.1f}%)")
if 'TABLA_ORIGEN' in df.columns:
    print(f"   Origen de datos:")
    for origen, count in df['TABLA_ORIGEN'].value_counts().items():
        print(f"      {origen}: {count:,} ({count/len(df)*100:.1f}%)")
print()

# Verificar columnas necesarias
print("Verificando columnas necesarias para Stock y Proveedores:")
print("-" * 70)

columnas_necesarias = {
    'FECHA': 'Fecha del movimiento',
    'CANTIDAD': 'Cantidad de bins',
    'MOVIMIENTO': 'Tipo de movimiento (ENTRADA/SALIDA)',
    'TABLA_ORIGEN': 'Origen (BASCULAR/BASCULAE)',
    'PROVEEDOR': 'Codigo de proveedor',
    'NOMBRE': 'Nombre del proveedor',
    'FVO': 'Fecha de volcado (para bins llenos)'
}

todas_presentes = True
for col, descripcion in columnas_necesarias.items():
    if col in df.columns:
        print(f"   [OK] {col}: {descripcion}")
    else:
        print(f"   [FALTA] {col}: {descripcion}")
        todas_presentes = False
print()

# Primeros registros
print("Primeros 5 registros:")
print("-" * 70)
print(df.head(5).to_string(index=False))
print()

# Ultimos registros
print("Ultimos 5 registros:")
print("-" * 70)
print(df.tail(5).to_string(index=False))
print()

conn.close()

# Conclusion
print("="*70)
print("CONCLUSION")
print("="*70)
print()

if todas_presentes and diferencia == 0:
    print("[EXCELENTE] El query CONSOLIDACION es PERFECTO para reemplazar las 2 tablas")
    print()
    print("Beneficios:")
    print("   1. Una sola lectura a Access (mas rapido)")
    print("   2. Datos ya ordenados por fecha")
    print("   3. Menos carga en disco/red")
    print("   4. Consistencia garantizada")
    print()
    print("Siguiente paso:")
    print("   -> Modificar cargar_datos_universal.py")
    print("   -> Cambiar cargar_movimientos_bins() para usar CONSOLIDACION")
    print()
elif todas_presentes:
    print("[ADVERTENCIA] El query funciona pero tiene diferencia en cantidad de registros")
    print(f"   Diferencia: {diferencia:+,} registros")
    print()
    print("   Recomendacion: Revisar el query CONSOLIDACION en Access")
    print()
else:
    print("[ERROR] Faltan columnas necesarias en el query CONSOLIDACION")
    print()
    print("   Debes agregar estas columnas al query en Access")
    print()

print("="*70)
