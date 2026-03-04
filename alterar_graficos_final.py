"""
Altera bdata en temp_*.html usando UN MISMO FACTOR para TODAS las series
de un mismo archivo. Así las proporciones entre series se mantienen
y la forma visual queda idéntica.
"""

import os
import re
import random
import base64
import struct

BASE = r"C:\Users\giann\Documents\GitHub\Gianni-Data-Lab\JUGOS SA"
random.seed(999)


def factor_por_archivo():
    """Factor entre 0.93 y 1.07, nunca entre 0.99 y 1.01."""
    f = random.uniform(0.93, 1.07)
    while 0.99 <= f <= 1.01:
        f = random.uniform(0.93, 1.07)
    return f


def procesar_archivo(filename):
    filepath = os.path.join(BASE, filename)
    with open(filepath, "r", encoding="utf-8") as fh:
        content = fh.read()

    # UN SOLO FACTOR para TODO el archivo
    fact = factor_por_archivo()
    count = 0

    def replace_bdata(match):
        nonlocal count
        bdata_raw = match.group(1)
        bdata_clean = bdata_raw.replace("\\u002f", "/").replace("\\u002F", "/")
        bdata_clean = bdata_clean.replace("\\u002b", "+").replace("\\u002B", "+")
        bdata_clean = bdata_clean.replace("\\u003d", "=").replace("\\u003D", "=")
        try:
            raw = base64.b64decode(bdata_clean)
            n_floats = len(raw) // 8
            if n_floats == 0:
                return match.group(0)
            if len(raw) % 8 != 0:
                raw = raw[:n_floats * 8]
            values = list(struct.unpack(f'<{n_floats}d', raw))

            new_values = tuple(v * fact if v != 0.0 else 0.0 for v in values)

            new_raw = struct.pack(f'<{n_floats}d', *new_values)
            new_bdata = base64.b64encode(new_raw).decode('ascii')
            count += 1
            return f'"bdata":"{new_bdata}"'
        except Exception as e:
            print(f"    ERROR: {e}")
            return match.group(0)

    content = re.sub(r'"bdata":"([^"]+)"', replace_bdata, content)

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(content)

    print(f"  {filename}: {count} series, factor unico = {fact:.4f}")


def main():
    html_files = sorted(fn for fn in os.listdir(BASE)
                        if fn.startswith("temp_") and fn.endswith(".html"))
    for fname in html_files:
        procesar_archivo(fname)
    print("\nCOMPLETADO")


if __name__ == "__main__":
    main()
