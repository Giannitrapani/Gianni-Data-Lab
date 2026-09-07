"""
Anonimiza las identidades de proveedores en los datos de Jugos S.A.

REEMPLAZA al script perdido que hacia esto sobre el HTML. La diferencia es
que este trabaja sobre los DATOS, no sobre la pagina: enmascarar solo el HTML
dejaba los nombres reales a la vista en los CSV del repositorio.

Que anonimiza
-------------
1. NOMBRE en las tablas de bascula (y en CONSOLIDACION)
2. nom en LProveedor  (el padron completo, ~1.900 nombres)
3. Origen en IngresosConKm, donde los nombres vienen embebidos y truncados
   ("GLP.CIPOLLETI BOSCHI HNOS. SA"). Este es el que se escapa si uno solo
   piensa en la columna NOMBRE.

Que NO cambia
-------------
Los codigos de proveedor, las cantidades, las fechas y los kilos quedan
intactos: el analisis sigue siendo valido, solo cambian las etiquetas.

El mapa real -> ficticio se guarda FUERA del repositorio. Sin ese archivo el
reemplazo no se puede revertir, y por eso mismo no debe publicarse.
"""

import os
import json
import random
import unicodedata
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "datos_csv")
# Fuera del repositorio a proposito.
MAPA = r"D:\DOCUMENTOS\GITHUB\jugos-datos\mapa_nombres.json"

SEMILLA = 20260906  # fijo: reejecutar da siempre el mismo resultado

APELLIDOS = [
    "AGUIRRE", "BENITEZ", "CABRERA", "DOMINGUEZ", "ESQUIVEL", "FIGUEROA",
    "GALVAN", "HEREDIA", "IBARRA", "JUAREZ", "LEDESMA", "MALDONADO",
    "NAVARRETE", "OLIVERA", "PERALTA", "QUIROGA", "ROLDAN", "SALGADO",
    "TEJEDA", "URQUIZA", "VALDEZ", "ZALAZAR", "ARANDA", "BUSTOS",
    "CARRIZO", "DELGADO", "ESCOBAR", "FRIAS", "GAUNA", "HUERTA",
    "LAGOS", "MERCADO", "NIEVA", "ORTEGA", "PAREDES", "RIVAROLA",
    "SORIA", "TOLEDO", "VERON", "ZAPATA",
]
NOMBRES = [
    "ALBERTO", "BEATRIZ", "CARLOS", "DANIELA", "EDUARDO", "FLORENCIA",
    "GUSTAVO", "HORACIO", "IGNACIO", "JULIETA", "LEANDRO", "MARIANA",
    "NICOLAS", "OSVALDO", "PATRICIA", "RAMIRO", "SILVINA", "TOMAS",
    "VALERIA", "WALTER", "ADRIAN", "CECILIA", "DIEGO", "ESTELA",
    "FERNANDO", "GRACIELA", "HECTOR", "IRENE", "JAVIER", "LUCIA",
]
EMPRESA_A = [
    "AGROPECUARIA", "FRUTICOLA", "CHACRAS", "ESTABLECIMIENTO", "FINCA",
    "PRODUCTORES", "COSECHA", "VALLE", "ANDINA", "PATAGONICA",
    "RIO NEGRO", "ALTO VALLE", "LA SERRANA", "EL ALAMO", "LOS SAUCES",
    "SANTA RITA", "SAN JORGE", "DON PEDRO", "LA ESPERANZA", "EL MIRADOR",
]
EMPRESA_B = ["SA", "SRL", "SAS", "HNOS. SA", "Y CIA SRL", "SA", "SRL"]

MARCAS_EMPRESA = (" SA", " S.A", " SRL", " S.R", " SAS", "HNOS", " CIA",
                  "COOP", " LTDA", "SOCIEDAD")


def es_empresa(nombre):
    u = nombre.upper()
    return any(m in u for m in MARCAS_EMPRESA)


def sin_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def construir_mapa(reales):
    """Real -> ficticio, conservando si parece empresa o persona."""
    rnd = random.Random(SEMILLA)
    usados = set()
    mapa = {}

    # Un nombre inventado no puede coincidir con uno real, ni contenerlo:
    # "ZAPATA ADRIAN BEATRIZ" deja visible al proveedor real "ZAPATA ADRIAN".
    # Se indexa por primera palabra para que la comprobacion sea barata.
    prohibidos = {r.strip().upper() for r in reales}
    por_inicial = {}
    for r in prohibidos:
        if r:
            por_inicial.setdefault(r.split()[0], []).append(r)

    def choca(candidato):
        c = candidato.upper()
        if c in prohibidos:
            return True
        return any(r in c for r in por_inicial.get(c.split()[0], ()))

    for real in sorted(reales):          # orden fijo => resultado estable
        for _ in range(400):
            if es_empresa(real):
                # Tres componentes: el repertorio tiene que cubrir ~1.900
                # nombres sin repetir. Con dos partes se agotaba a las 140.
                falso = (f"{rnd.choice(EMPRESA_A)} {rnd.choice(APELLIDOS)} "
                         f"{rnd.choice(EMPRESA_B)}")
            else:
                falso = (f"{rnd.choice(APELLIDOS)} {rnd.choice(NOMBRES)} "
                         f"{rnd.choice(NOMBRES)}")
            if falso not in usados and not choca(falso):
                break
        else:
            raise RuntimeError(f"sin alternativas libres para {real!r}")
        usados.add(falso)
        # Se respeta el largo original: los datos vienen con relleno de
        # espacios y cambiarlo desalinea las tablas de ancho fijo.
        mapa[real] = falso[:len(real)].ljust(len(real)) if len(real) > len(falso) else falso
    return mapa


CHACRAS = [
    "LA ISLA", "EL ALAMO", "LOS OLMOS", "SAN MIGUEL", "LA LOMA",
    "EL SAUCE", "LAS ACACIAS", "LA RIBERA", "EL MOLINO", "SANTA ANA",
    "LOS NOGALES", "LA HUELLA", "EL PORVENIR", "LA PALMERA", "EL RETIRO",
    "LOS CEIBOS", "LA QUINTA", "EL PARAISO", "LA ARBOLEDA", "EL MIRADOR",
]


def reconstruir_origenes(ing, cod_a_falso):
    """
    Devuelve origen_real -> origen_ficticio.

    Un origen es una CHACRA, y un productor puede tener muchas. No es una
    relacion uno a uno. Por eso el origen se reconstruye entero como
    "<chacra ficticia> - <productor ficticio>" en vez de parchear el texto:
    parchear dejaba restos del nombre real, rompia el nombre de la chacra
    (que no es el proveedor) y daba un nombre distinto a cada chacra del
    mismo productor, que asi parecia varios proveedores.
    """
    # A que productor pertenece cada origen (455 de 456 tienen uno solo).
    duenio = (ing.dropna(subset=["Origen"])
                 .groupby("Origen")["pro"].first().to_dict())

    mapa_o = {}
    contador = {}
    usados = set()
    for i, origen in enumerate(sorted(duenio)):
        cod = duenio[origen]
        prov_falso = cod_a_falso.get(cod, "PRODUCTOR SA")
        n = contador.get(cod, 0) + 1
        contador[cod] = n
        largo = len(origen)   # el campo es de ancho fijo (30)

        # El texto se corta a 30 caracteres, y ahi dos chacras de productores
        # distintos pueden terminar identicas y fusionarse en los graficos.
        # Se prueban variantes hasta que el resultado truncado sea unico.
        for k in range(len(CHACRAS)):
            chacra = CHACRAS[(i + k) % len(CHACRAS)]
            nuevo = f"CH.{n:02d} {chacra} - {prov_falso}"[:largo].ljust(largo)
            if nuevo not in usados:
                break
        else:
            nuevo = f"CH.{n:02d}-{i:03d} {prov_falso}"[:largo].ljust(largo)
        usados.add(nuevo)
        mapa_o[origen] = nuevo
    return mapa_o


def main():
    print("=" * 62)
    print("ANONIMIZACION DE IDENTIDADES - JUGOS S.A.")
    print("=" * 62)

    # 1. Juntar todos los nombres reales que aparecen en cualquier archivo
    reales = set()
    for f in ["TBL_Lbascular_formato_final", "TBL_basculae_formato_final"]:
        d = pd.read_csv(os.path.join(CSV, f + ".csv"))
        reales |= {str(x) for x in d["NOMBRE"].dropna()}
    prov = pd.read_csv(os.path.join(CSV, "LProveedor.csv"))
    reales |= {str(x) for x in prov["nom"].dropna()}
    reales = {r for r in reales if r.strip()}
    print(f"\nnombres reales encontrados: {len(reales):,}")

    mapa = construir_mapa(reales)
    os.makedirs(os.path.dirname(MAPA), exist_ok=True)
    with open(MAPA, "w", encoding="utf-8") as f:
        json.dump(mapa, f, ensure_ascii=False, indent=1)
    print(f"mapa guardado FUERA del repo -> {MAPA}")

    # Del mas largo al mas corto, para que el reemplazo por fragmentos no
    # rompa un nombre largo al encontrar antes uno corto contenido en el.
    pares = sorted(((r, mapa[r]) for r in mapa),
                   key=lambda p: len(p[0]), reverse=True)

    # 2. Columnas NOMBRE
    for f in ["TBL_Lbascular_formato_final", "TBL_basculae_formato_final"]:
        ruta = os.path.join(CSV, f + ".csv")
        d = pd.read_csv(ruta)
        antes = d["NOMBRE"].nunique()
        d["NOMBRE"] = d["NOMBRE"].map(lambda x: mapa.get(str(x), x))
        d.to_csv(ruta, index=False)
        print(f"  {f:32s} {antes:>4} nombres reemplazados")

    # 3. Padron de proveedores
    ruta = os.path.join(CSV, "LProveedor.csv")
    prov = pd.read_csv(ruta)
    prov["nom"] = prov["nom"].map(lambda x: mapa.get(str(x), x))
    prov.to_csv(ruta, index=False)
    print(f"  {'LProveedor':32s} {len(prov):>4} filas del padron")

    # 4. Origen (chacras). Se reconstruye entero: ver reconstruir_origenes.
    #    El codigo de productor 'pro' NO se toca, asi que la relacion
    #    productor -> muchas chacras queda intacta.
    ruta = os.path.join(CSV, "IngresosConKm.csv")
    ing = pd.read_csv(ruta)
    cod_a_falso = {}
    for _, r in prov.iterrows():
        try:
            cod_a_falso[int(r["nro"])] = str(r["nom"]).strip()
        except (ValueError, TypeError):
            pass
    origenes = reconstruir_origenes(ing, cod_a_falso)
    ing["Origen"] = ing["Origen"].map(lambda x: origenes.get(str(x), x))
    ing.to_csv(ruta, index=False)
    print(f"  {'IngresosConKm.Origen':32s} {len(origenes):>4} chacras reconstruidas")

    # 5. CONSOLIDACION se rearma de las dos basculas ya anonimizadas
    b1 = pd.read_csv(os.path.join(CSV, "TBL_Lbascular_formato_final.csv"))
    b1["TABLA_ORIGEN"] = "BASCULAR"
    b2 = pd.read_csv(os.path.join(CSV, "TBL_basculae_formato_final.csv"))
    b2["TABLA_ORIGEN"] = "BASCULAE"
    pd.concat([b1, b2], ignore_index=True).to_csv(
        os.path.join(CSV, "CONSOLIDACION.csv"), index=False)
    print(f"  {'CONSOLIDACION':32s} rearmado")

    print("\nListo. Ahora hay que regenerar los dashboards:")
    print("   python actualizar_dashboard_completo.py")


if __name__ == "__main__":
    main()
