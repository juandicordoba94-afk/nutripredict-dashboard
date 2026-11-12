import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def leer_json(ruta):
    with ruta.open(encoding="utf-8-sig") as archivo:
        return json.load(archivo)


def normalizar_codigo(valor, longitud):
    """Convierte códigos numéricos o de texto a DIVIPOLA con ceros iniciales."""
    if valor is None:
        return None

    codigo = str(valor).strip()
    if codigo.endswith(".0"):
        codigo = codigo[:-2]
    if not codigo:
        return None
    return codigo.zfill(longitud)


resultados = leer_json(DATA / "resultados_nutripredict.json")
df = pd.DataFrame(resultados)

if "DIVIPOLA" not in df.columns:
    raise KeyError("El JSON de resultados no contiene la columna DIVIPOLA.")

df["DIVIPOLA"] = df["DIVIPOLA"].map(lambda codigo: normalizar_codigo(codigo, 5))
codigos_resultados = set(df["DIVIPOLA"].dropna())
codigos_dpto_resultados = {codigo[:2] for codigo in codigos_resultados}

geo_mun = leer_json(DATA / "col_municipios_inset_nacional.geojson")
geo_dep = leer_json(DATA / "col_departamentos_inset_nacional.geojson")

codigos_geo_mun = {
    normalizar_codigo(feature.get("properties", {}).get("divipola_mun"), 5)
    for feature in geo_mun.get("features", [])
}
codigos_geo_mun.discard(None)

codigos_geo_dep = {
    normalizar_codigo(feature.get("properties", {}).get("divipola_dep"), 2)
    for feature in geo_dep.get("features", [])
}
codigos_geo_dep.discard(None)


def imprimir_lista(titulo, codigos, columnas, datos):
    print(f"\n{titulo}: {len(codigos)}")
    if not codigos:
        print("  Ninguno")
        return

    if datos is not None:
        filas = datos[datos[columnas[0]].isin(codigos)]
        disponibles = [columna for columna in columnas if columna in filas.columns]
        print(filas[disponibles].sort_values(columnas[0]).to_string(index=False))
    else:
        print("  " + ", ".join(sorted(codigos)))


print("=== Comparación de códigos DIVIPOLA ===")
print(f"Municipios en resultados: {len(codigos_resultados)} códigos únicos")
print(f"Municipios en GeoJSON:    {len(codigos_geo_mun)} códigos únicos")
print(f"Departamentos en resultados: {len(codigos_dpto_resultados)} códigos únicos")
print(f"Departamentos en GeoJSON:    {len(codigos_geo_dep)} códigos únicos")

imprimir_lista(
    "Municipios con resultados pero sin geometría",
    codigos_resultados - codigos_geo_mun,
    ["DIVIPOLA", "DPTO", "MUNICIPIO"],
    df,
)
imprimir_lista(
    "Municipios con geometría pero sin resultados",
    codigos_geo_mun - codigos_resultados,
    ["DIVIPOLA"],
    None,
)
imprimir_lista(
    "Departamentos con resultados pero sin geometría",
    codigos_dpto_resultados - codigos_geo_dep,
    ["CODDPTO"],
    pd.DataFrame({"CODDPTO": sorted(codigos_dpto_resultados)}),
)
imprimir_lista(
    "Departamentos con geometría pero sin resultados",
    codigos_geo_dep - codigos_dpto_resultados,
    ["CODDPTO"],
    None,
)

duplicados = df[df["DIVIPOLA"].duplicated(keep=False)].sort_values("DIVIPOLA")
print(f"\nFilas duplicadas en resultados: {len(duplicados)}")
if not duplicados.empty:
    columnas = [columna for columna in ["DIVIPOLA", "DPTO", "MUNICIPIO"] if columna in df.columns]
    print(duplicados[columnas].to_string(index=False))



with open("data/resultados_nutripredict.json", encoding="utf-8-sig") as f:
    datos = json.load(f)

df = pd.DataFrame(datos)

columnas = ["DIVIPOLA", "MUNICIPIO", "TASA_100K", "RURAL", "INDIGENA"]

print(df[columnas].head(15))
print()
print("Valores no nulos:")
print(df[columnas].notna().sum())
print()
print("Tipos de datos:")
print(df[columnas].dtypes)