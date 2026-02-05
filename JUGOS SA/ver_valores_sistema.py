# ============================================================================
# VER VALORES ACTUALES DEL SISTEMA
# ============================================================================

from cargar_datos_universal import cargar_movimientos_bins
import pandas as pd

print("="*70)
print("DATOS ACTUALMENTE CARGADOS EN EL SISTEMA")
print("="*70)
print()

# Cargar datos
df = cargar_movimientos_bins()

print(f"Total de registros: {len(df):,}")
print()

print("Rango de fechas:")
print(f"  Desde: {df['FECHA'].min()}")
print(f"  Hasta: {df['FECHA'].max()}")
print()

print(f"Total cantidad de bins: {df['CANTIDAD'].sum():,.0f}")
print()

print("Distribucion por MOVIMIENTO:")
mov = df['MOVIMIENTO'].value_counts()
for m, c in mov.items():
    print(f"  {m}: {c:,} ({c/len(df)*100:.1f}%)")
print()

print("Distribucion por TABLA_ORIGEN:")
orig = df['TABLA_ORIGEN'].value_counts()
total_orig = orig.sum()
for o, c in orig.items():
    print(f"  {o}: {c:,} ({c/total_orig*100:.1f}%)")
print()

print(f"Proveedores unicos: {df['PROVEEDOR'].nunique()}")
print()

print("Primeros 5 registros (ejemplo):")
print(df[['FECHA', 'PROVEEDOR', 'NOMBRE', 'CANTIDAD', 'MOVIMIENTO']].head(5).to_string(index=False))
print()

print("="*70)
print("COMPARA ESTOS VALORES CON LOS QUE TIENES ANOTADOS")
print("="*70)
print()
