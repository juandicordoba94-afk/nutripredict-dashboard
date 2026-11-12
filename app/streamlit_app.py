import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

st.set_page_config(
    page_title="NUTRIPREDICT Colombia 2030",
    layout="wide",
)

st.title("NUTRIPREDICT Colombia 2030")
st.caption(
    "Primera prueba: archivos, códigos territoriales y mapas."
)


@st.cache_data
def leer_json(ruta):
    with open(ruta, encoding="utf-8-sig") as archivo:
        return json.load(archivo)


archivos = {
    "resultados": DATA / "resultados_nutripredict.json",
    "departamentos": DATA / "col_departamentos_inset_nacional.geojson",
    "municipios": DATA / "col_municipios_inset_nacional.geojson",
}

faltantes = [
    str(ruta.relative_to(ROOT))
    for ruta in archivos.values()
    if not ruta.exists()
]

if faltantes:
    st.error("Faltan estos archivos:")
    st.write(faltantes)
    st.stop()

resultados = leer_json(archivos["resultados"])
geo_dep = leer_json(archivos["departamentos"])
geo_mun = leer_json(archivos["municipios"])

if not isinstance(resultados, list):
    st.error(
        "El JSON de resultados no es una lista de municipios. "
        "Debemos revisar su estructura antes de continuar."
    )
    st.stop()

df = pd.DataFrame(resultados)

requeridas = {
    "DIVIPOLA",
    "DPTO",
    "MUNICIPIO",
    "CASOS_REALES",
    "CASOS_PRED",
    "PROY_2030",
    "IPR",
}

faltan_columnas = requeridas - set(df.columns)

if faltan_columnas:
    st.error(f"Faltan columnas: {sorted(faltan_columnas)}")
    st.write("Columnas disponibles:", df.columns.tolist())
    st.stop()

df["DIVIPOLA"] = (
    df["DIVIPOLA"]
    .astype("string")
    .str.strip()
    .str.replace(r"\.0$", "", regex=True)
    .str.zfill(5)
)

if not df["DIVIPOLA"].str.fullmatch(r"\d{5}", na=False).all():
    st.error("Hay códigos DIVIPOLA vacíos o inválidos.")
    st.stop()

if df["DIVIPOLA"].duplicated().any():
    st.error(
        "El JSON tiene más de una fila por municipio. "
        "Revisemos su estructura antes de agregar resultados."
    )
    st.stop()

# El código de departamento son los primeros dos dígitos del DIVIPOLA.
df["CODDPTO"] = df["DIVIPOLA"].str[:2]

columnas_numericas = [
    "CASOS_REALES",
    "CASOS_PRED",
    "PROY_2030",
    "PROY_2030_BAJO",
    "PROY_2030_ALTO",
    "PROY_2030_P10",
    "PROY_2030_P90",
    "ESPERADOS_SIGUIENTE_ANIO",
    "TASA_100K",
    "RURAL",
    "INDIGENA",
    "IPR",
]

for columna in columnas_numericas:
    if columna in df.columns:
        df[columna] = pd.to_numeric(df[columna], errors="coerce")

for geo, campo, longitud in [
    (geo_dep, "divipola_dep", 2),
    (geo_mun, "divipola_mun", 5),
]:
    if geo.get("type") != "FeatureCollection":
        st.error("Uno de los mapas no es un GeoJSON FeatureCollection.")
        st.stop()

    for elemento in geo["features"]:
        propiedades = elemento.get("properties", {})

        if propiedades.get(campo) is None:
            st.error(f"El GeoJSON no contiene el campo esperado: {campo}")
            st.stop()

        propiedades[campo] = str(propiedades[campo]).strip().zfill(longitud)

codigos_geo = {
    elemento["properties"]["divipola_mun"]
    for elemento in geo_mun["features"]
}

sin_geometria = sorted(set(df["DIVIPOLA"]) - codigos_geo)

st.subheader("Comprobación de datos")
st.write("Municipios en los resultados:", len(df))
st.write("Municipios sin geometría:", len(sin_geometria))

if sin_geometria:
    st.warning("Estos códigos requieren revisión:")
    st.write(sin_geometria)

with st.expander("Ver columnas y primeras filas"):
    st.write(df.columns.tolist())
    st.dataframe(df.head(), hide_index=True)

st.sidebar.header("Filtros")

nivel = st.sidebar.radio(
    "Nivel territorial",
    ["Departamentos", "Municipios"],
    horizontal=True,
)

departamento = st.sidebar.selectbox(
    "Departamento",
    ["Todos"] + sorted(df["DPTO"].dropna().unique().tolist()),
)

df_vista = df.copy()

if departamento != "Todos":
    df_vista = df_vista[df_vista["DPTO"] == departamento]

if nivel == "Departamentos":
    mapa = (
        df_vista
        .groupby(["CODDPTO", "DPTO"], as_index=False)["PROY_2030"]
        .sum(min_count=1)
    )

    fig = px.choropleth(
        mapa,
        geojson=geo_dep,
        locations="CODDPTO",
        featureidkey="properties.divipola_dep",
        color="PROY_2030",
        hover_name="DPTO",
        hover_data=["PROY_2030"],
        color_continuous_scale="YlOrRd",
        title="Escenario central 2030: total por departamento",
    )

else:
    fig = px.choropleth(
        df_vista,
        geojson=geo_mun,
        locations="DIVIPOLA",
        featureidkey="properties.divipola_mun",
        color="IPR",
        hover_name="MUNICIPIO",
        hover_data=["DPTO", "PROY_2030", "CASOS_PRED", "RANGO", "CONFIABILIDAD"],
        color_continuous_scale="YlOrRd",
        range_color=(0, 100),
        title="Índice de priorización municipal",
    )

fig.update_geos(
    fitbounds="locations",
    visible=False,
    projection_type="mercator",
)

fig.update_layout(
    height=550,
    margin=dict(l=0, r=0, t=50, b=0),
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Cartografía: Marco Geoestadístico Nacional 2025, DANE. "
    "Simplificación: github.com/ytolosa/mapas-colombia, CC BY 4.0. "
    "San Andrés y Providencia se muestran desplazados y ampliados."
)

st.info(
    "El IPR es una prioridad relativa municipal, no un diagnóstico. "
    "Las cifras corresponden a notificaciones, no a incidencia real."
)
