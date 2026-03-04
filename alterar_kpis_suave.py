"""
Altera KPIs y datos de proveedores con variación suave:
- ±10% máximo
- Siempre redondeado a número entero
- Conserva formato de miles con punto
"""

import os
import re
import json
import random

BASE = r"C:\Users\giann\Documents\GitHub\Gianni-Data-Lab\JUGOS SA"
random.seed(321)


def factor():
    """Factor entre 0.90 y 1.10, nunca entre 0.98 y 1.02."""
    f = random.uniform(0.90, 1.10)
    while 0.98 <= f <= 1.02:
        f = random.uniform(0.90, 1.10)
    return f


def format_miles(n):
    """180693798 -> 180.693.798"""
    s = str(abs(int(n)))
    groups = []
    while s:
        groups.append(s[-3:])
        s = s[:-3]
    result = ".".join(reversed(groups))
    if n < 0:
        result = "-" + result
    return result


def alterar_valor_entero(valor_original):
    """Aplica ±10% y redondea a entero."""
    return int(round(valor_original * factor()))


# ---- dashboard.html ----
def alterar_dashboard():
    filepath = os.path.join(BASE, "dashboard.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    cambios = [
        # (valor_original_texto, valor_numerico, es_formato_miles)
        ("22.971", 22971, True),
        ("-33.1", -33.1, False),   # este es decimal, lo dejamos como -XX
        ("452", 452, False),
        ("542", 542, False),
        ("8.000", 8000, True),
        ("5.000", 5000, True),
    ]

    for texto_orig, val_num, es_miles in cambios:
        nuevo = alterar_valor_entero(val_num)
        if es_miles:
            texto_nuevo = format_miles(nuevo)
        else:
            texto_nuevo = str(nuevo)
        content = content.replace(texto_orig, texto_nuevo, 1)
        print(f"  dashboard: {texto_orig} -> {texto_nuevo}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


# ---- logistica.html ----
def alterar_logistica():
    filepath = os.path.join(BASE, "logistica.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 180.693.798 kg
    nuevo_kg = alterar_valor_entero(180693798)
    texto_kg = format_miles(nuevo_kg)
    content = content.replace("180.693.798", texto_kg, 1)
    print(f"  logistica: 180.693.798 -> {texto_kg}")

    # 390.242 bins
    nuevo_bins = alterar_valor_entero(390242)
    texto_bins = format_miles(nuevo_bins)
    content = content.replace("390.242", texto_bins, 1)
    print(f"  logistica: 390.242 -> {texto_bins}")

    # 463,0 promedio -> entero
    nuevo_prom = alterar_valor_entero(463)
    content = content.replace("463,0", f"{nuevo_prom},0", 1)
    print(f"  logistica: 463,0 -> {nuevo_prom},0")

    # 14.704 ingresos
    nuevo_ing = alterar_valor_entero(14704)
    texto_ing = format_miles(nuevo_ing)
    content = content.replace("14.704", texto_ing, 1)
    print(f"  logistica: 14.704 -> {texto_ing}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


# ---- proveedores.html ----
def alterar_proveedores():
    filepath = os.path.join(BASE, "proveedores.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    m = re.search(r'(const proveedores\s*=\s*)(\[.*?\]);', content, re.DOTALL)
    if not m:
        print("  ERROR: No se encontró array de proveedores")
        return

    data = json.loads(m.group(2))
    print(f"  proveedores: {len(data)} encontrados")

    for prov in data:
        f_sal = factor()
        if prov["salidas"] > 0:
            prov["salidas"] = max(1, int(round(prov["salidas"] * f_sal)))
        if prov["entradas"] > 0:
            prov["entradas"] = max(0, int(round(prov["entradas"] * factor())))

        prov["deuda"] = max(0, prov["salidas"] - prov["entradas"])

        if prov["salidas"] > 0:
            prov["deuda_pct"] = round(prov["deuda"] / prov["salidas"] * 100, 1)
            prov["ratio_dev"] = round(prov["entradas"] / prov["salidas"] * 100, 1)
        else:
            prov["deuda_pct"] = 0.0
            prov["ratio_dev"] = 0.0

        if prov["dias_sin_dev"] not in (999, 0):
            prov["dias_sin_dev"] = max(1, int(round(prov["dias_sin_dev"] * factor())))

        if prov["ritmo_devolucion"] > 0:
            prov["ritmo_devolucion"] = round(prov["ritmo_devolucion"] * factor(), 1)

        if prov["dias_para_saldar"] not in (9999, 0):
            prov["dias_para_saldar"] = max(1, int(round(prov["dias_para_saldar"] * factor())))

        if "razon" in prov and "%" in prov["razon"]:
            prov["razon"] = re.sub(r'\d+\.\d+%', f'{prov["deuda_pct"]}%', prov["razon"])

    new_json = json.dumps(data, ensure_ascii=False)
    content = content[:m.start(2)] + new_json + content[m.end(2):]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  proveedores: {len(data)} alterados")


def main():
    print("=" * 50)
    print("  ALTERACION SUAVE DE KPIs (±10%, enteros)")
    print("=" * 50)
    print()
    print("[1/3] dashboard.html...")
    alterar_dashboard()
    print()
    print("[2/3] logistica.html...")
    alterar_logistica()
    print()
    print("[3/3] proveedores.html...")
    alterar_proveedores()
    print()
    print("COMPLETADO")


if __name__ == "__main__":
    main()
