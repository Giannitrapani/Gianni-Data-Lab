# Test directo para leer CONSOLIDACION.csv
import pandas as pd
import os

print("="*70)
print("TEST LECTURA DIRECTA DE CONSOLIDACION.CSV")
print("="*70)
print()

archivo_csv = r"C:\Users\giann\Desktop\JUGOS-CLAUDE\datos_csv\CONSOLIDACION.csv"

print(f"Archivo: {archivo_csv}")
print(f"Existe: {os.path.exists(archivo_csv)}")
print()

if os.path.exists(archivo_csv):
    # Ver primeras líneas del archivo
    print("Primeras 3 líneas del archivo:")
    print("-" * 70)
    with open(archivo_csv, 'r', encoding='utf-8') as f:
        for i in range(3):
            print(f"  {i+1}: {f.readline().strip()}")
    print()

    # Intentar leer con detección automática
    print("Intentando leer con detección automática...")
    try:
        df = pd.read_csv(archivo_csv, sep=None, engine='python')
        print(f"[OK] Leído con detección automática")
        print(f"     Registros: {len(df):,}")
        print(f"     Columnas: {list(df.columns)}")
        print()
    except Exception as e:
        print(f"[ERROR] Detección automática falló: {e}")
        print()

    # Intentar con punto y coma
    print("Intentando leer con punto y coma (;)...")
    try:
        df = pd.read_csv(archivo_csv, sep=';')
        print(f"[OK] Leído con punto y coma")
        print(f"     Registros: {len(df):,}")
        print(f"     Columnas: {list(df.columns)}")
        print()

        print("Primeros 5 registros:")
        print(df.head(5).to_string(index=False))
        print()

    except Exception as e:
        print(f"[ERROR] Punto y coma falló: {e}")
        print()

    # Intentar con coma
    print("Intentando leer con coma (,)...")
    try:
        df = pd.read_csv(archivo_csv, sep=',')
        print(f"[OK] Leído con coma")
        print(f"     Registros: {len(df):,}")
        print(f"     Columnas: {list(df.columns)}")
        print()
    except Exception as e:
        print(f"[ERROR] Coma falló: {e}")
        print()

else:
    print("[ERROR] Archivo no existe")

print("="*70)
