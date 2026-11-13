"""
Módulo de carga de datos - NUTRIPREDICT Colombia 2030
Centraliza toda la carga y caché de datos (JSON, Parquet, Excel, CSV).
"""

from pathlib import Path
import json

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"


# ============================================================
# RUTAS DE ARCHIVOS
# ============================================================
ARCHIVOS = {
    "resultados": DATA / "resultados_nutripredict.json",
    "departamentos": DATA / "col_departamentos_inset_nacional.geojson",
    "municipios": DATA / "col_municipios_inset_nacional.geojson",
    "panel_mensual": DATA / "panel_mensual.parquet",
    "panel_semanal": DATA / "panel_semanal.parquet",
    "excel": OUTPUTS / "resultados_consolidados.xlsx",
    "metricas": OUTPUTS / "metricas_modelos.csv",
    "seleccion": OUTPUTS / "seleccion_modelos.json",
    "calidad": OUTPUTS / "calidad_datos.json",
}


# ============================================================
# VALIDACIÓN DE ARCHIVOS
# ============================================================
def validar_archivos():
    """Verifica que todos los archivos requeridos existan."""
    faltantes = [
        str(ruta.relative_to(ROOT))
        for ruta in ARCHIVOS.values()
        if not ruta.exists()
    ]
    if faltantes:
        st.error("Faltan estos archivos:")
        st.write(faltantes)
        st.stop()


validar_archivos()


# ============================================================
# FUNCIONES DE CARGA CON CACHÉ
# ============================================================
@st.cache_data
def leer_json(ruta: Path):
    """Carga un archivo JSON con codificación UTF-8-SIG."""
    with open(ruta, encoding="utf-8-sig") as archivo:
        return json.load(archivo)


@st.cache_data
def leer_parquet(ruta: Path):
    """Carga un archivo Parquet."""
    return pd.read_parquet(ruta)


@st.cache_data
def leer_excel(ruta: Path, hoja: str):
    """Carga una hoja de Excel."""
    return pd.read_excel(ruta, sheet_name=hoja)


@st.cache_data
def leer_csv(ruta: Path):
    """Carga un archivo CSV."""
    return pd.read_csv(ruta)


# ============================================================
# CARGA DE DATOS PRINCIPALES
# ============================================================
def cargar_datos_principales():
    """
    Carga todos los datasets principales.
    Retorna una tupla con todos los DataFrames y objetos necesarios.
    """
    # JSON y GeoJSON
    resultados = leer_json(ARCHIVOS["resultados"])
    geo_dep = leer_json(ARCHIVOS["departamentos"])
    geo_mun = leer_json(ARCHIVOS["municipios"])

    # Paneles Parquet
    panel_mensual = leer_parquet(ARCHIVOS["panel_mensual"])
    panel_semanal = leer_parquet(ARCHIVOS["panel_semanal"])

    # Excel (múltiples hojas)
    proy_nacional = leer_excel(ARCHIVOS["excel"], "Proy_Nacional")
    proy_departamental = leer_excel(ARCHIVOS["excel"], "Proy_Departamental")
    proy_municipal = leer_excel(ARCHIVOS["excel"], "Proy_Municipal")

    # CSVs y JSONs de outputs
    metricas_modelos = leer_csv(ARCHIVOS["metricas"])
    seleccion_modelos = leer_json(ARCHIVOS["seleccion"])
    calidad_datos = leer_json(ARCHIVOS["calidad"])

    return (
        resultados,
        geo_dep,
        geo_mun,
        panel_mensual,
        panel_semanal,
        proy_nacional,
        proy_departamental,
        proy_municipal,
        metricas_modelos,
        seleccion_modelos,
        calidad_datos,
    )


# ============================================================
# NORMALIZACIÓN DE COLUMNAS
# ============================================================
def normalizar_columnas_proyeccion(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas en DataFrames de proyección."""
    renombres = {}
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

    for columna in df.columns:
        clave = "".join(
            caracter
            for caracter in str(columna).casefold()
            if caracter.isalnum()
        )
        destino = equivalencias.get(clave)
        if destino and destino not in df.columns:
            renombres[columna] = destino

    return df.rename(columns=renombres)


def normalizar_paneles(panel_mensual: pd.DataFrame, panel_semanal: pd.DataFrame):
    """Normaliza columnas de paneles mensual y semanal."""
    # Panel mensual
    columnas_interfaz = {
        "divipolaresidencia": "DIVIPOLARESIDENCIA",
        "departamentoresidencia": "Departamentoresidencia",
        "municipioresidencia": "Municipioresidencia",
        "aniomesdt": "ANIOMESDT",
        "casosrural": "CASOSRURAL",
        "casosindigena": "CASOSINDIGENA",
    }
    renombres = {}
    for columna in panel_mensual.columns:
        clave = "".join(c for c in str(columna).casefold() if c.isalnum())
        destino = columnas_interfaz.get(clave)
        if destino and destino not in panel_mensual.columns:
            renombres[columna] = destino
    panel_mensual = panel_mensual.rename(columns=renombres)

    # Panel semanal
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
    renombres = {}
    for columna in panel_semanal.columns:
        clave = "".join(c for c in str(columna).casefold() if c.isalnum())
        destino = columnas_semanal.get(clave)
        if destino and destino not in panel_semanal.columns:
            renombres[columna] = destino
    panel_semanal = panel_semanal.rename(columns=renombres)

    return panel_mensual, panel_semanal


def validar_paneles(panel_mensual: pd.DataFrame, panel_semanal: pd.DataFrame):
    """Valida que los paneles tengan las columnas requeridas."""
    requeridas_mensual = {
        "DIVIPOLARESIDENCIA",
        "Departamentoresidencia",
        "Municipioresidencia",
        "ANIOMESDT",
        "CASOS",
        "CASOSRURAL",
        "CASOSINDIGENA",
    }
    faltan = requeridas_mensual - set(panel_mensual.columns)
    if faltan:
        st.error(
            "El panel mensual no contiene estas columnas: "
            + ", ".join(sorted(faltan))
        )
        st.write("Columnas disponibles:", panel_mensual.columns.tolist())
        st.stop()

    requeridas_semanal = {
        "DIVIPOLARESIDENCIA",
        "Departamentoresidencia",
        "Municipioresidencia",
        "SEMANAINI",
        "CASOS",
        "CASOSRURAL",
        "CASOSINDIGENA",
    }
    faltan = requeridas_semanal - set(panel_semanal.columns)
    if faltan:
        st.error(
            "El panel semanal no contiene estas columnas: "
            + ", ".join(sorted(faltan))
        )
        st.write("Columnas disponibles:", panel_semanal.columns.tolist())
        st.stop()


def preparar_resultados_df(resultados: list) -> pd.DataFrame:
    """Convierte la lista de resultados a DataFrame y normaliza columnas."""
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
    faltan = requeridas - set(df.columns)
    if faltan:
        st.error(f"Faltan columnas: {sorted(faltan)}")
        st.write("Columnas disponibles:", df.columns.tolist())
        st.stop()

    # Normalizar DIVIPOLA
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
        st.error("El JSON tiene más de una fila por municipio.")
        st.stop()

    # Código de departamento
    df["CODDPTO"] = df["DIVIPOLA"].str[:2]

    # Columnas numéricas
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
                valores = (
                    valores.astype("string")
                    .str.strip()
                    .str.replace("%", "", regex=False)
                )
            df[columna] = pd.to_numeric(valores, errors="coerce")

    return df


def normalizar_geojson(geo_dep, geo_mun):
    """Normaliza códigos en GeoJSON."""
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

    return geo_dep, geo_mun


def verificar_cobertura(df: pd.DataFrame, geo_mun):
    """Verifica coincidencia entre resultados y geometrías."""
    codigos_resultados = set(df["DIVIPOLA"])
    codigos_geo = {
        elemento["properties"]["divipola_mun"]
        for elemento in geo_mun["features"]
    }

    sin_geometria = sorted(codigos_resultados - codigos_geo)
    sin_resultados = sorted(codigos_geo - codigos_resultados)

    return {
        "con_resultados": len(codigos_resultados),
        "con_geometria": len(codigos_geo),
        "sin_geometria": sin_geometria,
        "sin_resultados": sin_resultados,
    }


def melt_proyeccion_nacional(proy_nacional: pd.DataFrame) -> pd.DataFrame:
    """Convierte proyección nacional a formato largo."""
    escenarios = ["BAJO", "CENTRAL", "ALTO"]
    if {"ANIO", *escenarios, "IC80BAJO", "IC80ALTO"}.issubset(proy_nacional.columns):
        return proy_nacional.melt(
            id_vars=["ANIO", "IC80BAJO", "IC80ALTO"],
            value_vars=escenarios,
            var_name="ESCENARIO",
            value_name="PROYECCION",
        )
    return proy_nacional


def melt_proyeccion_municipal(proy_municipal: pd.DataFrame) -> pd.DataFrame:
    """Convierte proyección municipal a formato largo."""
    escenarios = ["BAJO", "CENTRAL", "ALTO"]
    columnas_escenario = [
        c for c in proy_municipal.columns
        if str(c).startswith("PROY_") and str(c).endswith(tuple(f"_{e}" for e in escenarios))
    ]
    if columnas_escenario and {"DIVIPOLA", "DPTO", "MUNICIPIO"}.issubset(proy_municipal.columns):
        columnas_id = [
            c for c in proy_municipal.columns
            if c not in columnas_escenario
        ]
        df_long = proy_municipal.melt(
            id_vars=columnas_id,
            value_vars=columnas_escenario,
            var_name="ESCENARIO_COL",
            value_name="PROYECCION",
        )
        # Extraer año y escenario de la columna
        df_long["ANIO"] = df_long["ESCENARIO_COL"].str.extract(r"PROY_(\d{4})_").astype(int)
        df_long["ESCENARIO"] = df_long["ESCENARIO_COL"].str.extract(r"_(BAJO|CENTRAL|ALTO)$")
        return df_long.drop(columns=["ESCENARIO_COL"])
    return proy_municipal


# ============================================================
# FUNCIÓN PRINCIPAL DE INICIALIZACIÓN
# ============================================================
def inicializar_datos():
    """
    Función principal que carga y prepara todos los datos.
    Retorna un diccionario con todos los objetos listos para usar.
    """
    # Cargar datos raw
    (
        resultados,
        geo_dep,
        geo_mun,
        panel_mensual,
        panel_semanal,
        proy_nacional,
        proy_departamental,
        proy_municipal,
        metricas_modelos,
        seleccion_modelos,
        calidad_datos,
    ) = cargar_datos_principales()

    # Normalizar proyecciones
    proy_nacional = normalizar_columnas_proyeccion(proy_nacional)
    proy_departamental = normalizar_columnas_proyeccion(proy_departamental)
    proy_municipal = normalizar_columnas_proyeccion(proy_municipal)

    proy_nacional = melt_proyeccion_nacional(proy_nacional)
    proy_municipal = melt_proyeccion_municipal(proy_municipal)

    # Normalizar paneles
    panel_mensual, panel_semanal = normalizar_paneles(panel_mensual, panel_semanal)
    validar_paneles(panel_mensual, panel_semanal)

    # Preparar DataFrame de resultados
    df = preparar_resultados_df(resultados)

    # Normalizar GeoJSON
    geo_dep, geo_mun = normalizar_geojson(geo_dep, geo_mun)

    # Verificar cobertura
    cobertura = verificar_cobertura(df, geo_mun)

    return {
        "df": df,
        "geo_dep": geo_dep,
        "geo_mun": geo_mun,
        "panel_mensual": panel_mensual,
        "panel_semanal": panel_semanal,
        "proy_nacional": proy_nacional,
        "proy_departamental": proy_departamental,
        "proy_municipal": proy_municipal,
        "metricas_modelos": metricas_modelos,
        "seleccion_modelos": seleccion_modelos,
        "calidad_datos": calidad_datos,
        "cobertura": cobertura,
    }
