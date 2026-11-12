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
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    *, *::before, *::after {
        box-sizing: border-box;
    }

    [data-testid="stMainBlockContainer"] {
        width: 100%;
        max-width: 1600px;
        padding-inline: clamp(1rem, 3vw, 3rem);
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        min-width: 0;
        max-width: 100%;
    }

    @media (min-width: 769px) and (max-width: 1100px) {
        [data-testid="stMainBlockContainer"] {
            padding-inline: 1.5rem;
        }

        h1 {
            font-size: 2.1rem;
        }
    }

    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1rem 0.85rem 2rem;
        }

        h1 {
            font-size: 1.65rem;
            line-height: 1.2;
        }

        h2 {
            font-size: 1.3rem;
        }

        h3 {
            font-size: 1.1rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.2rem;
            flex-wrap: nowrap;
            justify-content: flex-start;
            overflow-x: auto;
            scrollbar-width: thin;
        }

        .stTabs [data-baseweb="tab"] {
            flex: 0 0 auto;
            min-height: 2.75rem;
            padding: 0.55rem 0.7rem;
            white-space: nowrap;
            font-size: 0.88rem;
        }

        [data-testid="stPlotlyChart"] {
            width: 100%;
            overflow: hidden;
        }

        [data-testid="stDataFrame"] {
            width: 100%;
            overflow-x: auto;
        }

        [data-testid="stWidgetLabel"] {
            font-size: 0.95rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("NUTRIPREDICT Colombia 2030")
st.caption(
    "Primera prueba: archivos, codigos territoriales y mapas."
)


@st.cache_data
def leer_json(ruta):
    with open(ruta, encoding="utf-8-sig") as archivo:
        return json.load(archivo)

@st.cache_data
def leer_parquet(ruta):
    return pd.read_parquet(ruta)


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

RUTA_PANEL_MENSUAL = DATA / "panel_mensual.parquet"

if not RUTA_PANEL_MENSUAL.exists():
    st.error(
        "No se encontró el archivo panel_mensual.parquet. "
        "Revísalo en la carpeta data/."
    )
    st.stop()

panel_mensual = leer_parquet(RUTA_PANEL_MENSUAL)

RUTA_PANEL_SEMANAL = DATA / "panel_semanal.parquet"

if not RUTA_PANEL_SEMANAL.exists():
    st.error(
        "No se encontró el archivo panel_semanal.parquet. "
        "Revísalo en la carpeta data/."
    )
    st.stop()

panel_semanal = leer_parquet(RUTA_PANEL_SEMANAL)

RUTA_EXCEL = ROOT / "outputs" / "resultados_consolidados.xlsx"

if not RUTA_EXCEL.exists():
    st.error(
        "No se encontró el archivo resultados_consolidados.xlsx. "
        "Revísalo en la carpeta outputs/."
    )
    st.stop()


@st.cache_data
def leer_excel(ruta, hoja):
    return pd.read_excel(ruta, sheet_name=hoja)


proy_nacional = leer_excel(RUTA_EXCEL, "Proy_Nacional")
proy_departamental = leer_excel(RUTA_EXCEL, "Proy_Departamental")
proy_municipal = leer_excel(RUTA_EXCEL, "Proy_Municipal")

RUTA_METRICAS = ROOT / "outputs" / "metricas_modelos.csv"
RUTA_SELECCION = ROOT / "outputs" / "seleccion_modelos.json"
RUTA_CALIDAD = ROOT / "outputs" / "calidad_datos.json"

if not RUTA_METRICAS.exists():
    st.error(
        "No se encontró el archivo metricas_modelos.csv. "
        "Revísalo en la carpeta outputs/."
    )
    st.stop()

if not RUTA_SELECCION.exists():
    st.error(
        "No se encontró el archivo seleccion_modelos.json. "
        "Revísalo en la carpeta outputs/."
    )
    st.stop()

if not RUTA_CALIDAD.exists():
    st.error(
        "No se encontró el archivo calidad_datos.json. "
        "Revísalo en la carpeta outputs/."
    )
    st.stop()


@st.cache_data
def leer_csv(ruta):
    return pd.read_csv(ruta)


metricas_modelos = leer_csv(RUTA_METRICAS)
seleccion_modelos = leer_json(RUTA_SELECCION)
calidad_datos = leer_json(RUTA_CALIDAD)

def normalizar_columnas_proyeccion(df):
    renombres = {}

    for columna in df.columns:
        clave = "".join(
            caracter
            for caracter in str(columna).casefold()
            if caracter.isalnum()
        )

        equivalencias = {
            "anio": "ANIO",
            "año": "ANIO",
            "escenario": "ESCENARIO",
            "proyeccion": "PROYECCION",
            "ic80bajo": "IC80BAJO",
            "ic80alto": "IC80ALTO",
            "coddpto": "CODDPTO",
            "coddepto": "CODDPTO",
            "codigodepartamento": "CODDPTO",
            "departamento": "DEPARTAMENTO",
            "divipolaresidencia": "DIVIPOLA",
            "departamentoresidencia": "DPTO",
            "municipioresidencia": "MUNICIPIO",
        }

        destino = equivalencias.get(clave)

        if destino and destino not in df.columns:
            renombres[columna] = destino

    return df.rename(columns=renombres)


proy_nacional = normalizar_columnas_proyeccion(proy_nacional)
proy_departamental = normalizar_columnas_proyeccion(proy_departamental)
proy_municipal = normalizar_columnas_proyeccion(proy_municipal)

# Las hojas nacional y municipal guardan los escenarios en columnas separadas.
escenarios = ["BAJO", "CENTRAL", "ALTO"]
if {"ANIO", *escenarios, "IC80BAJO", "IC80ALTO"}.issubset(
    proy_nacional.columns
):
    proy_nacional = proy_nacional.melt(
        id_vars=["ANIO", "IC80BAJO", "IC80ALTO"],
        value_vars=escenarios,
        var_name="ESCENARIO",
        value_name="PROYECCION",
    )

columnas_escenario_municipal = [
    columna
    for columna in proy_municipal.columns
    if str(columna).startswith("PROY_")
    and str(columna).endswith(tuple(f"_{escenario}" for escenario in escenarios))
]
if columnas_escenario_municipal and {
    "DIVIPOLA",
    "DPTO",
    "MUNICIPIO",
}.issubset(proy_municipal.columns):
    # Conserva los metadatos y los intervalos P10/P90 al pasar a formato largo.
    columnas_id_municipal = [
        columna
        for columna in proy_municipal.columns
        if columna not in columnas_escenario_municipal
    ]
    proy_municipal = proy_municipal.melt(
        id_vars=columnas_id_municipal,
        value_vars=columnas_escenario_municipal,
        var_name="ANIO_ESCENARIO",
        value_name="PROYECCION",
    )
    extraido = proy_municipal["ANIO_ESCENARIO"].str.extract(
        r"PROY_(\d{4})_(BAJO|CENTRAL|ALTO)"
    )
    proy_municipal["ANIO"] = pd.to_numeric(extraido[0], errors="coerce")
    proy_municipal["ESCENARIO"] = extraido[1]
    proy_municipal = proy_municipal.drop(columns="ANIO_ESCENARIO")


def tabla_escenarios(df):
    """Conserva las demás columnas y expande los escenarios a columnas."""
    columnas_id = [
        columna
        for columna in df.columns
        if columna not in {
            "ESCENARIO",
            "PROYECCION",
            "IC80BAJO",
            "IC80ALTO",
        }
    ]
    tabla = (
        df.pivot(
            index=columnas_id,
            columns="ESCENARIO",
            values="PROYECCION",
        )
        .reset_index()
    )
    tabla.columns.name = None
    columnas = columnas_id + [
        escenario for escenario in escenarios if escenario in tabla.columns
    ]
    return tabla[columnas]


formato_escenarios = {
    escenario: st.column_config.NumberColumn(escenario, format="%.0f")
    for escenario in escenarios
}

# Unifica los nombres del Parquet con los que utiliza la interfaz. Así se
# aceptan variantes con guiones bajos, espacios y diferencias de mayúsculas.
columnas_interfaz = {
    "divipolaresidencia": "DIVIPOLARESIDENCIA",
    "departamentoresidencia": "Departamentoresidencia",
    "municipioresidencia": "Municipioresidencia",
    "aniomesdt": "ANIOMESDT",
    "casosrural": "CASOSRURAL",
    "casosindigena": "CASOSINDIGENA",
}
renombres_panel = {}
for columna in panel_mensual.columns:
    clave = "".join(caracter for caracter in str(columna).casefold() if caracter.isalnum())
    destino = columnas_interfaz.get(clave)
    if destino and destino not in panel_mensual.columns:
        renombres_panel[columna] = destino

panel_mensual = panel_mensual.rename(columns=renombres_panel)

columnas_semanal = {
    "divipolaresidencia": "DIVIPOLARESIDENCIA",
    "departamentoresidencia": "Departamentoresidencia",
    "municipioresidencia": "Municipioresidencia",
    "anoepi": "ANOEPI",
    "semepi": "SEMEPI",
    "semanaini": "SEMANAINI",
    "casosrural": "CASOSRURAL",
    "casosindigena": "CASOSINDIGENA",
}

renombres_semanal = {}

for columna in panel_semanal.columns:
    clave = "".join(
        caracter
        for caracter in str(columna).casefold()
        if caracter.isalnum()
    )

    destino = columnas_semanal.get(clave)

    if destino and destino not in panel_semanal.columns:
        renombres_semanal[columna] = destino

panel_semanal = panel_semanal.rename(columns=renombres_semanal)

columnas_requeridas_panel = {
    "DIVIPOLARESIDENCIA",
    "Departamentoresidencia",
    "Municipioresidencia",
    "ANIOMESDT",
    "CASOS",
    "CASOSRURAL",
    "CASOSINDIGENA",
}

faltan_panel = columnas_requeridas_panel - set(panel_mensual.columns)

if faltan_panel:
    st.error(
        "El panel mensual no contiene estas columnas: "
        + ", ".join(sorted(faltan_panel))
    )
    st.write("Columnas disponibles:", panel_mensual.columns.tolist())
    st.stop()


columnas_requeridas_semanal = {
    "DIVIPOLARESIDENCIA",
    "Departamentoresidencia",
    "Municipioresidencia",
    "SEMANAINI",
    "CASOS",
    "CASOSRURAL",
    "CASOSINDIGENA",
}

faltan_semanal = (
    columnas_requeridas_semanal
    - set(panel_semanal.columns)
)

if faltan_semanal:
    st.error(
        "El panel semanal no contiene estas columnas: "
        + ", ".join(sorted(faltan_semanal))
    )
    st.write(
        "Columnas disponibles:",
        panel_semanal.columns.tolist(),
    )
    st.stop()

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
        "El JSON tiene mas de una fila por municipio. "
        "Revisemos su estructura antes de agregar resultados."
    )
    st.stop()

# El codigo de departamento son los primeros dos dígitos del DIVIPOLA.
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
    "RURAL",
    "INDIGENA",
    "IPR",
]

for columna in columnas_numericas:
    if columna in df.columns:
        valores = df[columna]
        if columna in {"RURAL", "INDIGENA"}:
            # El JSON guarda estos porcentajes como texto, por ejemplo "84.7%".
            valores = (
                valores.astype("string")
                .str.strip()
                .str.replace("%", "", regex=False)
            )
        df[columna] = pd.to_numeric(valores, errors="coerce")

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

st.subheader("Comprobacion de datos")
st.write("Municipios en los resultados:", len(df))
st.write("Municipios sin geometria:", len(sin_geometria))

if sin_geometria:
    st.warning("Estos codigos requieren revision:")
    st.write(sin_geometria)

with st.expander("Ver columnas y primeras filas"):
    st.write(df.columns.tolist())
    st.dataframe(df.head(), hide_index=True)

codigos_resultados = set(df["DIVIPOLA"])
codigos_geo = {
    elemento["properties"]["divipola_mun"]
    for elemento in geo_mun["features"]
}

sin_geometria = sorted(codigos_resultados - codigos_geo)
sin_resultados = sorted(codigos_geo - codigos_resultados)

st.subheader("Comprobacion de cobertura territorial")

st.write("Municipios con resultados:", len(codigos_resultados))
st.write("Municipios con geometria:", len(codigos_geo))
st.write("Con resultados pero sin geometria:", len(sin_geometria))
st.write("Con geometria pero sin resultados:", len(sin_resultados))

if sin_geometria:
    st.warning(
        "Municipios con resultados pero sin geometria en el GeoJSON:"
    )
    st.dataframe(
        df[df["DIVIPOLA"].isin(sin_geometria)][[
            "DIVIPOLA", "DPTO", "MUNICIPIO", "CASOS_REALES",
            "CASOS_PRED", "PROY_2030", "IPR", "CONFIABILIDAD"
        ]],
        hide_index=True,
    )

if sin_resultados:
    st.info(
        "Municipios con geometria pero sin resultados en el JSON: "
        + ", ".join(sin_resultados)
    )

tab_mapa, tab_priorizacion, tab_mensual, tab_semanal, tab_proyeccion, tab_modelos, tab_metodologia = st.tabs(
    ["Mapa", 
     "Priorización municipal", 
     "Evolución mensual", 
     "Evolución semanal", 
     "Proyección 2026-2030",
     "Modelos y calidad",
     "Metodología y limitaciones"]
)

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
        title="Indice de priorizacion municipal",
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

with tab_mapa:
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
    "El IPR es una prioridad relativa municipal, no un diagnostico individual. "
    "Rural e indigena corresponden a la composicion de los casos notificados, "
    "no a la composicion poblacional del municipio."
    )

with tab_priorizacion:
    st.subheader("Priorizacion municipal")

    st.caption(
        "La tabla muestra los municipios con mayor indice de Priorizacion Relativa (IPR). "
        "El IPR es una prioridad relativa entre municipios, no un diagnostico individual."
    )

    columnas_tabla = [
        "DIVIPOLA",
        "DPTO",
        "MUNICIPIO",
        "CASOS_REALES",
        "CASOS_PRED",
        "PROY_2030",
        "RURAL",
        "INDIGENA",
        "IPR",
        "RANGO",
        "CONFIABILIDAD",
    ]

    columnas_disponibles = [
        columna
        for columna in columnas_tabla
        if columna in df.columns
    ]

    if "IPR" not in columnas_disponibles:
        st.error("La columna IPR no esta disponible en el JSON.")
        st.stop()

    df_prioridad = df_vista.copy()

    df_prioridad["IPR"] = pd.to_numeric(
        df_prioridad["IPR"],
        errors="coerce",
    )

    df_prioridad = df_prioridad.sort_values(
        "IPR",
        ascending=False,
        na_position="last",
    )

    if "RANGO" in df_prioridad.columns:
        orden_rango = {
            "CRITICO": 0,
            "ALTO": 1,
            "MEDIO": 2,
            "BAJO": 3,
        }

        df_prioridad["ORDEN_RANGO"] = (
            df_prioridad["RANGO"]
            .astype("string")
            .str.strip()
            .str.upper()
            .map(orden_rango)
            .fillna(99)
        )

        df_prioridad = df_prioridad.sort_values(
            ["ORDEN_RANGO", "IPR"],
            ascending=[True, False],
            na_position="last",
        )

        df_prioridad = df_prioridad.drop(columns="ORDEN_RANGO")

    top_n = st.slider(
        "Numero de municipios a mostrar",
        min_value=10,
        max_value=50,
        value=15,
        step=5,
    )

    tabla_prioridad = df_prioridad.head(top_n)[columnas_disponibles]

    columnas_formato = {
    "CASOS_REALES": st.column_config.NumberColumn(
        "Casos reales",
        format="%.0f",
    ),
    "CASOS_PRED": st.column_config.NumberColumn(
        "Casos predichos",
        format="%.0f",
    ),
    "PROY_2030": st.column_config.NumberColumn(
        "Proyeccion 2030",
        format="%.0f",
    ),
    "RURAL": st.column_config.NumberColumn(
        "Casos rurales (%)",
        format="%.1f%%",
    ),
    "INDIGENA": st.column_config.NumberColumn(
        "Casos indigenas (%)",
        format="%.1f%%",
    ),
    "IPR": st.column_config.NumberColumn(
        "IPR",
        format="%.2f",
    ),
    }   

    st.dataframe(
        tabla_prioridad,
        hide_index=True,
        use_container_width=True,
        column_config=columnas_formato,
    )

    st.download_button(
        label="Descargar tabla de priorizacion en CSV",
        data=tabla_prioridad.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        file_name="priorizacion_municipal.csv",
        mime="text/csv",
    )

    st.info(
        "Los municipios con confiabilidad baja tienen pocos casos notificados "
        "en los ultimos dos años; sus proyecciones e indices son mas inestables."
    )

with tab_mensual:
    st.subheader("Evolución mensual por municipio")

    st.caption(
        "La línea muestra casos notificados por municipio y mes. "
        "No representa incidencia real ni riesgo individual."
    )

    departamentos_mensuales = sorted(
        panel_mensual["Departamentoresidencia"]
        .dropna()
        .unique()
        .tolist()
    )

    departamento_mensual = st.selectbox(
        "Departamento",
        departamentos_mensuales,
        key="departamento_mensual",
    )

    municipios_mensuales = (
        panel_mensual
        .loc[
            panel_mensual["Departamentoresidencia"]
            == departamento_mensual,
            "Municipioresidencia",
        ]
        .dropna()
        .unique()
        .tolist()
    )

    municipio_mensual = st.selectbox(
        "Municipio",
        sorted(municipios_mensuales),
        key="municipio_mensual",
    )

    df_mensual = panel_mensual.loc[
        (panel_mensual["Departamentoresidencia"] == departamento_mensual)
        & (panel_mensual["Municipioresidencia"] == municipio_mensual)
    ].copy()

    if df_mensual.empty:
        st.warning(
            "No hay datos mensuales para este municipio."
        )
    else:
        df_mensual["ANIOMESDT"] = pd.to_datetime(
            df_mensual["ANIOMESDT"],
            errors="coerce",
        )

        df_mensual = df_mensual.dropna(
            subset=["ANIOMESDT"]
        ).sort_values("ANIOMESDT")

        fecha_minima = df_mensual["ANIOMESDT"].min()
        fecha_maxima = df_mensual["ANIOMESDT"].max()

        rango_fechas = st.slider(
            "Rango de fechas",
            min_value=fecha_minima.to_pydatetime(),
            max_value=fecha_maxima.to_pydatetime(),
            value=(
                fecha_minima.to_pydatetime(),
                fecha_maxima.to_pydatetime(),
            ),
            format="MM/YYYY",
        )

        fecha_inicio, fecha_fin = rango_fechas

        df_mensual = df_mensual.loc[
            (df_mensual["ANIOMESDT"] >= pd.Timestamp(fecha_inicio))
            & (df_mensual["ANIOMESDT"] <= pd.Timestamp(fecha_fin))
        ]

        if df_mensual.empty:
            st.warning(
                "No hay datos en el rango de fechas seleccionado."
            )
        else:
            fig_mensual = px.line(
                df_mensual,
                x="ANIOMESDT",
                y="CASOS",
                title=(
                    f"Casos notificados por mes: "
                    f"{municipio_mensual}, {departamento_mensual}"
                ),
                labels={
                    "ANIOMESDT": "Mes",
                    "CASOS": "Casos notificados",
                },
            )

            fig_mensual.update_traces(
                mode="lines+markers",
                line=dict(width=2),
                marker=dict(size=5),
            )

            fig_mensual.update_layout(
                height=450,
                margin=dict(l=0, r=0, t=50, b=0),
                hovermode="x unified",
            )

            st.plotly_chart(
                fig_mensual,
                use_container_width=True,
            )

            with st.expander("Ver datos mensuales"):
                st.dataframe(
                    df_mensual[[
                        "ANIOMESDT",
                        "CASOS",
                        "CASOSRURAL",
                        "CASOSINDIGENA",
                    ]],
                    hide_index=True,
                    use_container_width=True,
                )

            st.download_button(
                label="Descargar datos mensuales en CSV",
                data=df_mensual.to_csv(
                    index=False,
                    encoding="utf-8-sig",
                ).encode("utf-8-sig"),
                file_name=(
                    f"evolucion_mensual_"
                    f"{municipio_mensual.replace(' ', '_')}.csv"
                ),
                mime="text/csv",
            )

with tab_semanal:
    st.subheader("Evolución semanal por municipio")
    st.caption(
        "La línea muestra casos notificados por semana epidemiológica. "
        "No representa incidencia real ni riesgo individual."
    )

    departamentos_semanales = sorted(
        panel_semanal["Departamentoresidencia"]
        .dropna()
        .unique()
        .tolist()
    )

    departamento_semanal = st.selectbox(
        "Departamento",
        departamentos_semanales,
        key="departamento_semanal",
    )

    municipios_semanales = sorted(
        panel_semanal.loc[
            panel_semanal["Departamentoresidencia"] == departamento_semanal,
            "Municipioresidencia",
        ]
        .dropna()
        .unique()
        .tolist()
    )

    municipio_semanal = st.selectbox(
        "Municipio",
        municipios_semanales,
        key="municipio_semanal",
    )

    df_semanal = panel_semanal.loc[
        (panel_semanal["Departamentoresidencia"] == departamento_semanal)
        & (panel_semanal["Municipioresidencia"] == municipio_semanal)
    ].copy()

    if df_semanal.empty:
        st.warning("No hay datos semanales para este municipio.")
    else:
        df_semanal["SEMANAINI"] = pd.to_datetime(
            df_semanal["SEMANAINI"],
            errors="coerce",
        )
        df_semanal = df_semanal.dropna(subset=["SEMANAINI"]).sort_values(
            "SEMANAINI"
        )

        if df_semanal.empty:
            st.warning("El panel no contiene fechas semanales válidas.")
        else:
            fecha_minima = df_semanal["SEMANAINI"].min()
            fecha_maxima = df_semanal["SEMANAINI"].max()

            if fecha_minima < fecha_maxima:
                rango_semanal = st.slider(
                    "Rango de fechas",
                    min_value=fecha_minima.to_pydatetime(),
                    max_value=fecha_maxima.to_pydatetime(),
                    value=(
                        fecha_minima.to_pydatetime(),
                        fecha_maxima.to_pydatetime(),
                    ),
                    format="DD/MM/YYYY",
                    key="rango_semanal",
                )
                fecha_inicio, fecha_fin = rango_semanal
                df_semanal = df_semanal.loc[
                    (df_semanal["SEMANAINI"] >= pd.Timestamp(fecha_inicio))
                    & (df_semanal["SEMANAINI"] <= pd.Timestamp(fecha_fin))
                ]

            if df_semanal.empty:
                st.warning("No hay datos en el rango de fechas seleccionado.")
            else:
                fig_semanal = px.line(
                    df_semanal,
                    x="SEMANAINI",
                    y="CASOS",
                    title=(
                        f"Casos notificados por semana: "
                        f"{municipio_semanal}, {departamento_semanal}"
                    ),
                    labels={
                        "SEMANAINI": "Semana epidemiológica (inicio)",
                        "CASOS": "Casos notificados",
                    },
                )
                fig_semanal.update_traces(
                    mode="lines+markers",
                    line=dict(width=2),
                    marker=dict(size=4),
                )
                fig_semanal.update_layout(
                    height=450,
                    margin=dict(l=0, r=0, t=50, b=0),
                    hovermode="x unified",
                )
                st.plotly_chart(fig_semanal, use_container_width=True)

                with st.expander("Ver datos semanales"):
                    st.dataframe(
                        df_semanal[[
                            "SEMANAINI",
                            "CASOS",
                            "CASOSRURAL",
                            "CASOSINDIGENA",
                        ]],
                        hide_index=True,
                        use_container_width=True,
                    )

                st.download_button(
                    label="Descargar datos semanales en CSV",
                    data=df_semanal.to_csv(
                        index=False,
                        encoding="utf-8-sig",
                    ).encode("utf-8-sig"),
                    file_name=(
                        f"evolucion_semanal_"
                        f"{municipio_semanal.replace(' ', '_')}.csv"
                    ),
                    mime="text/csv",
                )

with tab_proyeccion:
    st.subheader("Proyección 2026–2030")

    st.caption(
        "Las proyecciones corresponden a casos notificados esperados, "
        "no a incidencia real ni riesgo individual. "
        "Los escenarios reflejan supuestos de planeación, no certezas."
    )

    nivel_proyeccion = st.radio(
        "Nivel de proyección",
        ["Nacional", "Departamental", "Municipal"],
        horizontal=True,
    )

    if nivel_proyeccion == "Nacional":
        columnas_requeridas = {
            "ANIO",
            "ESCENARIO",
            "PROYECCION",
        }

        faltan = columnas_requeridas - set(proy_nacional.columns)

        if faltan:
            st.error(
                "La hoja Proy_Nacional no contiene estas columnas: "
                + ", ".join(sorted(faltan))
            )
            st.write(
                "Columnas disponibles:",
                proy_nacional.columns.tolist(),
            )
            st.stop()

        fig_proyeccion = px.line(
            proy_nacional,
            x="ANIO",
            y="PROYECCION",
            color="ESCENARIO",
            markers=True,
            title="Proyección nacional de casos notificados, 2026–2030",
            labels={
                "ANIO": "Año",
                "PROYECCION": "Casos notificados esperados",
                "ESCENARIO": "Escenario",
            },
            color_discrete_map={
                "BAJO": "#2ca02c",
                "CENTRAL": "#1f77b4",
                "ALTO": "#d62728",
            },
        )

        if {"IC80BAJO", "IC80ALTO"}.issubset(proy_nacional.columns):
            central = proy_nacional[
                proy_nacional["ESCENARIO"] == "CENTRAL"
            ].sort_values("ANIO")

            fig_proyeccion.add_scatter(
                x=central["ANIO"],
                y=central["IC80ALTO"],
                mode="lines",
                name="Intervalo 80% superior",
                line=dict(width=1, dash="dash", color="#1f77b4"),
                showlegend=True,
            )

            fig_proyeccion.add_scatter(
                x=central["ANIO"],
                y=central["IC80BAJO"],
                mode="lines",
                name="Intervalo 80% inferior",
                line=dict(width=1, dash="dash", color="#1f77b4"),
                fill="tonexty",
                fillcolor="rgba(31,119,180,0.12)",
                showlegend=True,
            )

        st.plotly_chart(
            fig_proyeccion,
            use_container_width=True,
        )

        with st.expander("Ver proyección nacional"):
            st.dataframe(
                tabla_escenarios(proy_nacional),
                hide_index=True,
                use_container_width=True,
                column_config=formato_escenarios,
            )

    elif nivel_proyeccion == "Departamental":
        columnas_requeridas = {
            "CODDPTO",
            "DEPARTAMENTO",
            "ANIO",
            "ESCENARIO",
            "PROYECCION",
        }

        faltan = columnas_requeridas - set(proy_departamental.columns)

        if faltan:
            st.error(
                "La hoja Proy_Departamental no contiene estas columnas: "
                + ", ".join(sorted(faltan))
            )
            st.write(
                "Columnas disponibles:",
                proy_departamental.columns.tolist(),
            )
            st.stop()

        departamentos_proyeccion = sorted(
            proy_departamental["DEPARTAMENTO"]
            .dropna()
            .unique()
            .tolist()
        )

        departamento_proyeccion = st.selectbox(
            "Departamento",
            departamentos_proyeccion,
            key="departamento_proyeccion",
        )

        df_departamento = proy_departamental.loc[
            proy_departamental["DEPARTAMENTO"]
            == departamento_proyeccion
        ].copy()

        if df_departamento.empty:
            st.warning(
                "No hay proyección departamental para este departamento."
            )

        else:
            fig_proyeccion = px.line(
                df_departamento,
                x="ANIO",
                y="PROYECCION",
                color="ESCENARIO",
                markers=True,
                title=(
                    f"Proyección departamental: "
                    f"{departamento_proyeccion}, 2026–2030"
                ),
                labels={
                    "ANIO": "Año",
                    "PROYECCION": "Casos notificados esperados",
                    "ESCENARIO": "Escenario",
                },
                color_discrete_map={
                    "BAJO": "#2ca02c",
                    "CENTRAL": "#1f77b4",
                    "ALTO": "#d62728",
                },
            )

            if {"IC80BAJO", "IC80ALTO"}.issubset(df_departamento.columns):
                central = df_departamento[
                    df_departamento["ESCENARIO"] == "CENTRAL"
                ].sort_values("ANIO")

                fig_proyeccion.add_scatter(
                    x=central["ANIO"],
                    y=central["IC80ALTO"],
                    mode="lines",
                    name="Intervalo 80% superior",
                    line=dict(width=1, dash="dash", color="#1f77b4"),
                    showlegend=True,
                )

                fig_proyeccion.add_scatter(
                    x=central["ANIO"],
                    y=central["IC80BAJO"],
                    mode="lines",
                    name="Intervalo 80% inferior",
                    line=dict(width=1, dash="dash", color="#1f77b4"),
                    fill="tonexty",
                    fillcolor="rgba(31,119,180,0.12)",
                    showlegend=True,
                )

            fig_proyeccion.update_layout(
                height=450,
                margin=dict(l=0, r=0, t=50, b=0),
                hovermode="x unified",
            )

            st.plotly_chart(
                fig_proyeccion,
                use_container_width=True,
            )

            with st.expander("Ver proyección departamental"):
                st.dataframe(
                    tabla_escenarios(df_departamento),
                    hide_index=True,
                    use_container_width=True,
                    column_config=formato_escenarios,
                )

    else:
        columnas_requeridas = {
            "DIVIPOLA",
            "DPTO",
            "MUNICIPIO",
            "ANIO",
            "ESCENARIO",
            "PROYECCION",
        }

        faltan = columnas_requeridas - set(proy_municipal.columns)

        if faltan:
            st.error(
                "La hoja Proy_Municipal no contiene estas columnas: "
                + ", ".join(sorted(faltan))
            )
            st.write(
                "Columnas disponibles:",
                proy_municipal.columns.tolist(),
            )
            st.stop()

        departamentos_proyeccion = sorted(
            proy_municipal["DPTO"]
            .dropna()
            .unique()
            .tolist()
        )

        departamento_proyeccion = st.selectbox(
            "Departamento",
            departamentos_proyeccion,
            key="departamento_proyeccion_municipal",
        )

        municipios_proyeccion = (
            proy_municipal
            .loc[
                proy_municipal["DPTO"]
                == departamento_proyeccion,
                "MUNICIPIO",
            ]
            .dropna()
            .unique()
            .tolist()
        )

        municipio_proyeccion = st.selectbox(
            "Municipio",
            sorted(municipios_proyeccion),
            key="municipio_proyeccion",
        )

        df_municipio = proy_municipal.loc[
            (proy_municipal["DPTO"] == departamento_proyeccion)
            & (proy_municipal["MUNICIPIO"] == municipio_proyeccion)
        ].copy()

        if df_municipio.empty:
            st.warning(
                "No hay proyección municipal para este municipio."
            )

        else:
            fig_proyeccion = px.line(
                df_municipio,
                x="ANIO",
                y="PROYECCION",
                color="ESCENARIO",
                markers=True,
                title=(
                    f"Proyección municipal: "
                    f"{municipio_proyeccion}, {departamento_proyeccion}"
                ),
                labels={
                    "ANIO": "Año",
                    "PROYECCION": "Casos notificados esperados",
                    "ESCENARIO": "Escenario",
                },
                color_discrete_map={
                    "BAJO": "#2ca02c",
                    "CENTRAL": "#1f77b4",
                    "ALTO": "#d62728",
                },
            )

            fig_proyeccion.update_layout(
                height=450,
                margin=dict(l=0, r=0, t=50, b=0),
                hovermode="x unified",
            )

            st.plotly_chart(
                fig_proyeccion,
                use_container_width=True,
            )

            with st.expander("Ver proyección municipal"):
                st.dataframe(
                    tabla_escenarios(df_municipio),
                    hide_index=True,
                    use_container_width=True,
                    column_config=formato_escenarios,
                )

    st.info(
        "La proyección de largo plazo usa supuestos explícitos de crecimiento, "
        "amortiguamiento y escenarios. No debe interpretarse como una predicción "
        "determinista ni como una estimación de riesgo individual."
    )

with tab_modelos:
    st.subheader("Modelos y calidad de los datos")

    st.caption(
        "Esta sección muestra el desempeño de los modelos en validación y prueba, "
        "así como los controles de calidad aplicados a los datos de SIVIGILA."
    )

    st.markdown("### Modelos seleccionados")

    if not isinstance(seleccion_modelos, dict):
        st.error(
            "El archivo seleccion_modelos.json no tiene la estructura esperada."
        )
        st.stop()

    filas_seleccion = []

    for clave, valor in seleccion_modelos.items():
        if isinstance(valor, dict):
            frecuencia = {"M": "Mensual", "W": "Semanal"}.get(clave, clave)
            seleccionado = valor.get("seleccionado", {})
            mejores = valor.get("mejor_validacion_por_nivel", {})

            if isinstance(mejores, dict) and mejores:
                for nivel, modelo in mejores.items():
                    filas_seleccion.append(
                        {
                            "Frecuencia": frecuencia,
                            "Nivel territorial": nivel,
                            "Modelo seleccionado": modelo,
                            "Criterio": seleccionado.get("criterio", ""),
                        }
                    )
            elif seleccionado:
                filas_seleccion.append(
                    {
                        "Frecuencia": frecuencia,
                        "Nivel territorial": seleccionado.get("nivel", ""),
                        "Modelo seleccionado": seleccionado.get("nombre", ""),
                        "Criterio": seleccionado.get("criterio", ""),
                    }
                )

    if filas_seleccion:
        st.dataframe(
            pd.DataFrame(filas_seleccion),
            hide_index=True,
            use_container_width=True,
        )

    else:
        st.info(
            "No se encontraron modelos seleccionados en el archivo JSON."
        )

    st.markdown("### Métricas de los modelos")

    metricas = metricas_modelos.rename(
        columns={
            "Nivel": "Nivel territorial",
            "Mejor_val": "Mejor en validación",
            "n_val": "N validación",
            "n_test": "N prueba",
            "MAE_val": "MAE validación",
            "RMSE_val": "RMSE validación",
            "R2_val": "R² validación",
            "WMAPE_val": "WMAPE validación (%)",
            "MAE_test": "MAE prueba",
            "RMSE_test": "RMSE prueba",
            "R2_test": "R² prueba",
            "WMAPE_test": "WMAPE prueba (%)",
        }
    ).copy()

    if "Frecuencia" in metricas.columns:
        metricas["Frecuencia"] = (
            metricas["Frecuencia"]
            .astype("string")
            .str.strip()
            .str.lower()
            .map({"mensual": "Mensual", "semanal": "Semanal"})
            .fillna(metricas["Frecuencia"])
        )

    columnas_metricas = [
        "Frecuencia",
        "Nivel territorial",
        "Modelo",
        "Clave",
        "Mejor en validación",
        "N validación",
        "N prueba",
        "MAE validación",
        "RMSE validación",
        "R² validación",
        "WMAPE validación (%)",
        "MAE prueba",
        "RMSE prueba",
        "R² prueba",
        "WMAPE prueba (%)",
    ]

    columnas_disponibles = [
        columna
        for columna in columnas_metricas
        if columna in metricas.columns
    ]

    if not columnas_disponibles:
        st.error(
            "El archivo metricas_modelos.csv no contiene las columnas esperadas."
        )
        st.write("Columnas disponibles:", metricas.columns.tolist())
        st.stop()

    frecuencia_filtro = st.selectbox(
        "Frecuencia",
        ["Todas", "Mensual", "Semanal"],
        key="filtro_frecuencia_metricas",
    )

    nivel_filtro = st.selectbox(
        "Nivel territorial",
        [
            "Todos",
            "Municipal",
            "Municipal (estables)",
            "Departamental",
            "Nacional",
        ],
        key="filtro_nivel_metricas",
    )

    metricas_filtradas = metricas.copy()

    if frecuencia_filtro != "Todas":
        metricas_filtradas = metricas_filtradas[
            metricas_filtradas["Frecuencia"] == frecuencia_filtro
        ]

    if nivel_filtro != "Todos":
        metricas_filtradas = metricas_filtradas[
            metricas_filtradas["Nivel territorial"] == nivel_filtro
        ]

    if metricas_filtradas.empty:
        st.warning(
            "No hay métricas para la combinación seleccionada."
        )

    else:
        orden_metricas = [
            columna
            for columna in [
                "Frecuencia",
                "Nivel territorial",
                "Modelo",
                "Clave",
                "Mejor en validación",
                "N validación",
                "N prueba",
                "MAE validación",
                "RMSE validación",
                "R² validación",
                "WMAPE validación (%)",
                "MAE prueba",
                "RMSE prueba",
                "R² prueba",
                "WMAPE prueba (%)",
            ]
            if columna in metricas_filtradas.columns
        ]

        metricas_filtradas = metricas_filtradas[orden_metricas]

        st.dataframe(
            metricas_filtradas,
            hide_index=True,
            use_container_width=True,
        )

    st.download_button(
        label="Descargar métricas filtradas en CSV",
        data=metricas_filtradas.to_csv(
            index=False,
            encoding="utf-8-sig",
        ).encode("utf-8-sig"),
        file_name="metricas_modelos_filtradas.csv",
        mime="text/csv",
    )

    st.markdown("### Calidad de los datos")

    if not isinstance(calidad_datos, dict):
        st.error(
            "El archivo calidad_datos.json no tiene la estructura esperada."
        )
        st.stop()

    calidad_resumen = {
        indicador: valor
        for indicador, valor in calidad_datos.items()
        if not isinstance(valor, (dict, list))
    }
    calidad_df = pd.DataFrame(
        list(calidad_resumen.items()),
        columns=["Indicador", "Valor"],
    )

    st.dataframe(
        calidad_df,
        hide_index=True,
        use_container_width=True,
    )

    if isinstance(calidad_datos.get("exclusiones"), dict):
        with st.expander("Detalle de filas excluidas"):
            st.dataframe(
                pd.DataFrame(
                    list(calidad_datos["exclusiones"].items()),
                    columns=["Motivo", "Filas"],
                ),
                hide_index=True,
                use_container_width=True,
            )

    if calidad_datos.get("fechas_por_ano_archivo"):
        with st.expander("Revisión de fechas por año"):
            st.dataframe(
                pd.DataFrame(calidad_datos["fechas_por_ano_archivo"]),
                hide_index=True,
                use_container_width=True,
            )

    if isinstance(calidad_datos.get("conciliacion_totales"), dict):
        with st.expander("Conciliación de totales"):
            st.dataframe(
                pd.DataFrame(
                    list(calidad_datos["conciliacion_totales"].items()),
                    columns=["Panel", "Casos"],
                ),
                hide_index=True,
                use_container_width=True,
            )

    if calidad_datos.get("pct_faltante_por_columna"):
        with st.expander("Porcentaje de datos faltantes"):
            st.dataframe(
                pd.DataFrame(
                    list(calidad_datos["pct_faltante_por_columna"].items()),
                    columns=["Columna", "Porcentaje faltante"],
                ),
                hide_index=True,
                use_container_width=True,
            )
    else:
        st.caption("El informe no registra faltantes en las columnas revisadas.")

    st.download_button(
        label="Descargar informe completo de calidad (JSON)",
        data=json.dumps(
            calidad_datos,
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8-sig"),
        file_name="calidad_datos.json",
        mime="application/json",
    )

    st.info(
        "Las métricas de prueba se reportan para comparar modelos, pero la selección "
        "se realizó únicamente con la validación de 2023. Las métricas de prueba "
        "no se usaron para elegir hiperparámetros ni modelos."
    )

    st.info(
        "Las cifras corresponden a casos notificados al sistema de vigilancia, "
        "no a incidencia real ni riesgo individual."
    )

with tab_metodologia:
    st.subheader("Metodología y limitaciones")

    st.markdown("### Qué mide NUTRIPREDICT")

    st.write(
        """
        NUTRIPREDICT analiza la evolución de las notificaciones de desnutrición
        aguda infantil correspondientes al evento 113 de SIVIGILA en Colombia.

        La unidad de análisis es la **notificación**, no la persona. Por ello,
        las cifras no deben interpretarse como incidencia real, prevalencia,
        riesgo individual ni diagnóstico clínico.
        """
    )

    st.markdown("### Fuentes y período")

    st.write(
        """
        - **Fuente principal:** notificaciones del evento 113 de SIVIGILA.
        - **Período analizado:** 2016 a 2025.
        - **Unidad territorial:** municipio de residencia, identificado con DIVIPOLA.
        - **Frecuencias:** mensual y semanal epidemiológica.
        - **Proyección:** 2026 a 2030.
        """
    )

    st.markdown("### Cómo se construyeron los modelos")

    st.write(
        """
        El análisis utiliza varios enfoques complementarios:

        - Modelos de referencia, como último valor observado, promedios móviles
          y pronóstico estacional ingenuo.
        - Modelos de aprendizaje automático, incluyendo Random Forest, XGBoost
          y LightGBM.
        - Modelos de conteos, incluyendo GLM Poisson y binomial negativa.
        - Modelos de series de tiempo, incluyendo suavizamiento exponencial,
          Holt-Winters y SARIMA/SARIMAX.
        - Una red neuronal GRU global con pérdida de Poisson.

        Los modelos usan información disponible hasta el periodo anterior. Es decir,
        para predecir un mes o una semana, no utilizan el valor del periodo que se
        quiere predecir.
        """
    )

    st.markdown("### Validación y selección")

    st.write(
        """
        La selección de modelos e hiperparámetros se realizó únicamente con la
        validación de 2023. El período de prueba, 2024–2025, se utilizó para
        evaluar el desempeño final, pero no para elegir modelos.

        El modelo final mensual es **LightGBM Poisson** y el modelo final semanal
        es **Ensamble LGBXGB**.
        """
    )

    st.markdown("### Proyecciones 2026–2030")

    st.write(
        """
        Las proyecciones de largo plazo son escenarios de planeación, no predicciones
        deterministas. Se construyen a partir de un nivel base, una tendencia
        departamental amortiguada y tres escenarios de crecimiento: bajo, central y alto.

        El escenario central limita el crecimiento anual para evitar extrapolaciones
        extremas. Los escenarios bajo y alto representan variaciones de planeación,
        no límites estadísticos exactos.
        """
    )

    st.markdown("### Índice de priorización relativa")

    st.write(
        """
        El IPR es un índice relativo entre municipios. Sirve para ordenar territorios
        según volumen esperado, composición rural e indígena de los casos notificados
        y, cuando está disponible, tasa poblacional.

        El IPR **no es un diagnóstico**, no mide riesgo individual y no debe usarse
        para asignar recursos sin revisar el contexto territorial.
        """
    )

    st.markdown("### Limitaciones principales")

    st.warning(
        """
        **1. Notificaciones, no incidencia real.**  
        Las cifras corresponden a casos notificados al sistema de vigilancia. No
        capturan necesariamente todos los casos de desnutrición aguda infantil.
        """
    )

    st.warning(
        """
        **2. Cambios en la capacidad de notificación.**  
        Variaciones en la detección, reporte, acceso a servicios de salud o
        actualización de registros pueden afectar las tendencias observadas.
        """
    )

    st.warning(
        """
        **3. Municipios con baja confiabilidad.**  
        Los municipios con pocos casos notificados en los últimos dos años tienen
        proyecciones e índices más inestables. Deben interpretarse con precaución.
        """
    )

    st.warning(
        """
        **4. Ruralidad e indigenidad.**  
        Las variables de ruralidad e indigenidad describen la composición de los
        casos notificados, no la composición poblacional total del municipio.
        """
    )

    st.warning(
        """
        **5. Proyecciones de largo plazo.**  
        Las proyecciones 2026–2030 dependen de supuestos explícitos y no incorporan
        cambios futuros en políticas públicas, financiación, cobertura de salud,
        seguridad alimentaria, migración, conflictos o capacidad de notificación.
        """
    )

    st.warning(
        """
        **6. Cobertura cartográfica.**  
        Algunos territorios pueden aparecer en los resultados pero no tener geometría
        disponible en la cartografía utilizada. Esto no elimina sus resultados, pero
        impide mostrarlos en el mapa municipal.
        """
    )

    st.markdown("### Uso responsable")

    st.info(
        """
        Este dashboard es una herramienta de exploración y priorización relativa.
        No reemplaza la vigilancia epidemiológica, la valoración clínica, la
        intervención territorial ni la toma de decisiones basada en evidencia local.
        """
    )

    st.info(
        """
        Para decisiones operativas, el IPR debe complementarse con información local:
        población infantil, cobertura de servicios, acceso a alimentos, condiciones
        socioeconómicas, capacidad institucional y evidencia territorial.
        """
    )