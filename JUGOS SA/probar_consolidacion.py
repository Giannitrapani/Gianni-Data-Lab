# ============================================================================
# PROBAR QUERY CONSOLIDACION - Test de integración
# ============================================================================

import pandas as pd
from cargar_datos_universal import cargar_movimientos_bins
from datetime import datetime

print("="*70)
print("PRUEBA DEL QUERY CONSOLIDACION")
print("="*70)
print()

print(f"Fecha de prueba: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print()

# ============================================================================
# PASO 1: Intentar cargar movimientos usando la función mejorada
# ============================================================================

print("PASO 1: Cargando movimientos de bins...")
print("-" * 70)

try:
    df = cargar_movimientos_bins()
    print()
    print("[OK] Datos cargados exitosamente")
    print()

    # ============================================================================
    # PASO 2: Verificar estructura de datos
    # ============================================================================

    print("PASO 2: Verificando estructura de datos...")
    print("-" * 70)

    columnas_necesarias = [
        'FECHA',
        'CANTIDAD',
        'MOVIMIENTO',
        'TABLA_ORIGEN',
        'PROVEEDOR',
        'NOMBRE',
        'FVO'
    ]

    print(f"Columnas presentes en DataFrame: {len(df.columns)}")
    for col in df.columns:
        print(f"   - {col}")
    print()

    print("Verificando columnas necesarias:")
    todas_presentes = True
    for col in columnas_necesarias:
        if col in df.columns:
            print(f"   [OK] {col}")
        else:
            print(f"   [FALTA] {col}")
            todas_presentes = False
    print()

    if not todas_presentes:
        print("[ERROR] Faltan columnas necesarias")
        print()
        exit(1)

    # ============================================================================
    # PASO 3: Estadísticas de datos
    # ============================================================================

    print("PASO 3: Estadísticas de datos...")
    print("-" * 70)

    print(f"Total de registros: {len(df):,}")
    print(f"Rango de fechas: {df['FECHA'].min()} a {df['FECHA'].max()}")
    print()

    print("Distribución por MOVIMIENTO:")
    for mov, count in df['MOVIMIENTO'].value_counts().items():
        print(f"   {mov}: {count:,} ({count/len(df)*100:.1f}%)")
    print()

    print("Distribución por TABLA_ORIGEN:")
    for origen, count in df['TABLA_ORIGEN'].value_counts().items():
        print(f"   {origen}: {count:,} ({count/len(df)*100:.1f}%)")
    print()

    print("Proveedores únicos: {:,}".format(df['PROVEEDOR'].nunique()))
    print(f"Total cantidad de bins: {df['CANTIDAD'].sum():,.0f}")
    print()

    # ============================================================================
    # PASO 4: Verificar datos de ejemplo
    # ============================================================================

    print("PASO 4: Primeros 10 registros...")
    print("-" * 70)
    print(df.head(10)[['FECHA', 'PROVEEDOR', 'NOMBRE', 'CANTIDAD', 'MOVIMIENTO', 'TABLA_ORIGEN']].to_string(index=False))
    print()

    # ============================================================================
    # PASO 5: Verificar que se está usando CONSOLIDACION
    # ============================================================================

    print("PASO 5: Verificando método de carga...")
    print("-" * 70)

    import os
    csv_consolidacion = os.path.join(os.path.dirname(__file__), 'datos_csv', 'CONSOLIDACION.csv')

    if os.path.exists(csv_consolidacion):
        print(f"[OK] CSV CONSOLIDACION encontrado: {csv_consolidacion}")
        print()
        print("   Si viste el mensaje '[OPTIMIZADO]' arriba, significa que")
        print("   el sistema está usando el query CONSOLIDACION (1 sola lectura)")
        print()
    else:
        print(f"[ADVERTENCIA] CSV CONSOLIDACION NO encontrado")
        print(f"   Ruta esperada: {csv_consolidacion}")
        print()
        print("   El sistema está usando el método fallback (2 tablas separadas)")
        print()
        print("   Para optimizar:")
        print("   1. Abre Access")
        print("   2. Exporta query CONSOLIDACION a CSV")
        print("   3. Guarda en: datos_csv/CONSOLIDACION.csv")
        print()

    # ============================================================================
    # CONCLUSIÓN
    # ============================================================================

    print("="*70)
    print("CONCLUSIÓN")
    print("="*70)
    print()

    if todas_presentes:
        print("[EXCELENTE] El sistema funciona correctamente")
        print()
        print("Columnas: OK")
        print("Datos: OK")
        print(f"Registros: {len(df):,}")
        print()

        if os.path.exists(csv_consolidacion):
            print("Optimización: ACTIVADA (usando query CONSOLIDACION)")
            print()
            print("Beneficios:")
            print("   - 1 sola lectura en lugar de 2")
            print("   - Más rápido")
            print("   - Menos carga en disco/red")
        else:
            print("Optimización: PENDIENTE (usando método fallback)")
            print()
            print("Para activar optimización:")
            print("   Exporta query CONSOLIDACION desde Access a CSV")
    else:
        print("[ERROR] El sistema no funciona correctamente")

    print()
    print("="*70)

except Exception as e:
    print()
    print("[ERROR] Fallo al cargar datos")
    print(f"   {str(e)}")
    print()
    import traceback
    traceback.print_exc()
    exit(1)
