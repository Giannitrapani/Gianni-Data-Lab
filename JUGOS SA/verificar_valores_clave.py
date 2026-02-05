# ============================================================================
# VERIFICAR VALORES CLAVE DEL SISTEMA
# ============================================================================

print("="*70)
print("VERIFICACION DE VALORES CLAVE")
print("="*70)
print()

# ============================================================================
# VALOR 1: LOGISTICA - Cantidad de kg de fruta procesada
# ============================================================================

print("[1/2] LOGISTICA - Cantidad de kg de fruta procesada")
print("-" * 70)

try:
    from cargar_datos_universal import cargar_ingresos_logistica
    import pandas as pd

    df_logistica, df_prov = cargar_ingresos_logistica()

    total_kg_logistica = df_logistica['kgs'].sum()

    print(f"   Fuente: IngresosConKm")
    print(f"   Total registros: {len(df_logistica):,}")
    print(f"   Rango fechas: {df_logistica['Fecha'].min()} a {df_logistica['Fecha'].max()}")
    print()
    print(f"   >>> VALOR ACTUAL: {total_kg_logistica:,.0f} kg <<<")
    print()

    valor_esperado_logistica = 180693798
    diferencia_logistica = abs(total_kg_logistica - valor_esperado_logistica)

    if abs(total_kg_logistica - valor_esperado_logistica) < 1000:
        print(f"   ✓ CORRECTO - Coincide con valor esperado ({valor_esperado_logistica:,})")
    else:
        print(f"   ✗ DIFERENCIA - Valor esperado: {valor_esperado_logistica:,}")
        print(f"                  Diferencia: {diferencia_logistica:,} kg")

except Exception as e:
    print(f"   ERROR: {str(e)}")

print()

# ============================================================================
# VALOR 2: STOCK GLOBAL - Bins Vacíos Disponibles
# ============================================================================

print("[2/2] STOCK GLOBAL - Bins Vacíos Disponibles")
print("-" * 70)

try:
    from cargar_datos_universal import cargar_movimientos_bins
    import pandas as pd

    movimientos = cargar_movimientos_bins()

    print(f"   Fuente: CONSOLIDACION (Lbascular + Lbasculae)")
    print(f"   Total registros: {len(movimientos):,}")
    print(f"   Rango fechas: {movimientos['FECHA'].min()} a {movimientos['FECHA'].max()}")
    print()

    # Calcular bins vacíos disponibles (última fecha)
    TOTAL_BINS = 30000

    # Crear columna de fecha sin hora
    movimientos['FECHA_DIA'] = pd.to_datetime(movimientos['FECHA']).dt.date
    movimientos['FECHA_DIA'] = pd.to_datetime(movimientos['FECHA_DIA'])

    # Obtener última fecha
    fecha_max = movimientos['FECHA_DIA'].max()

    # Calcular salidas y entradas acumuladas hasta última fecha
    salidas_vacios_acum = movimientos[
        (movimientos['TABLA_ORIGEN'] == 'BASCULAE') &
        (movimientos['MOVIMIENTO'] == 'SALIDA') &
        (movimientos['FECHA_DIA'] <= fecha_max)
    ]['CANTIDAD'].sum()

    entradas_desde_campo_acum = movimientos[
        (movimientos['MOVIMIENTO'] == 'ENTRADA') &
        (movimientos['FECHA_DIA'] <= fecha_max)
    ]['CANTIDAD'].sum()

    bins_en_campos = salidas_vacios_acum - entradas_desde_campo_acum

    # Bins llenos en planta
    bins_llenos = movimientos[
        (movimientos['TABLA_ORIGEN'] == 'BASCULAR') &
        (movimientos['MOVIMIENTO'] == 'ENTRADA') &
        (movimientos['FECHA_DIA'] <= fecha_max)
    ]['CANTIDAD'].sum()

    bins_vacios_disponibles = TOTAL_BINS - bins_en_campos - bins_llenos

    print(f"   Cálculo:")
    print(f"      Total bins sistema: {TOTAL_BINS:,}")
    print(f"      Bins en campos: {bins_en_campos:,.0f}")
    print(f"      Bins llenos planta: {bins_llenos:,.0f}")
    print()
    print(f"   >>> VALOR ACTUAL: {bins_vacios_disponibles:,.0f} bins <<<")
    print()

    valor_esperado_bins = 22971
    diferencia_bins = abs(bins_vacios_disponibles - valor_esperado_bins)

    if abs(bins_vacios_disponibles - valor_esperado_bins) < 100:
        print(f"   ✓ CORRECTO - Coincide con valor esperado ({valor_esperado_bins:,})")
    else:
        print(f"   ✗ DIFERENCIA - Valor esperado: {valor_esperado_bins:,}")
        print(f"                  Diferencia: {diferencia_bins:,.0f} bins")

except Exception as e:
    print(f"   ERROR: {str(e)}")

print()
print("="*70)
print("RESUMEN")
print("="*70)
print()
print("Si los valores coinciden con tu papel: ✓ TODO FUNCIONA")
print("Si los valores NO coinciden: Necesitas elegir otra base de datos")
print()
print("="*70)
