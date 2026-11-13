"""
Módulo de mapas - NUTRIPREDICT Colombia 2030
Centraliza la creación de todos los mapas coropléticos.
"""

from typing import Optional
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure


# ============================================================
# MAPAS COROPLÉTICOS
# ============================================================

def crear_mapa_departamental(
    df: pd.DataFrame,
    geo_dep: dict,
    color_col: str = "PROY_2030",
    title: str = "Escenario central 2030: total por departamento",
) -> Figure:
    """Crea mapa coroplético a nivel departamental."""
    fig = px.choropleth(
        df,
        geojson=geo_dep,
        locations="CODDPTO",
        featureidkey="properties.divipola_dep",
        color=color_col,
        hover_name="DPTO",
        hover_data=[color_col],
        color_continuous_scale="YlOrRd",
        title=title,
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
    )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="Casos 2030",
            len=0.75,
            thickness=15,
            tickfont=dict(size=11),
        ),
    )

    return fig


def crear_mapa_municipal(
    df: pd.DataFrame,
    geo_mun: dict,
    color_col: str = "IPR",
    title: str = "Índice de Priorización Municipal (IPR)",
) -> Figure:
    """Crea mapa coroplético a nivel municipal con range_color dinámico."""
    ipr_min = float(df[color_col].min())
    ipr_max = float(df[color_col].max())

    fig = px.choropleth(
        df,
        geojson=geo_mun,
        locations="DIVIPOLA",
        featureidkey="properties.divipola_mun",
        color=color_col,
        hover_name="MUNICIPIO",
        custom_data=["DPTO", "PROY_2030", "CASOS_PRED", "RANGO", "CONFIABILIDAD", "IPR", "RURAL", "INDIGENA"],
        color_continuous_scale="YlOrRd",
        range_color=(ipr_min, ipr_max),
        title=title,
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Departamento: %{customdata[0]}<br>"
            "IPR: %{customdata[5]:.2f} (%{customdata[6]:.1f}% rural, %{customdata[7]:.1f}% indígena)<br>"
            "Proyección 2030: %{customdata[1]:.0f}<br>"
            "Casos predichos: %{customdata[2]:.0f}<br>"
            "Rango: %{customdata[3]}<br>"
            "Confiabilidad: %{customdata[4]}<extra></extra>"
        )
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
    )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="IPR",
            len=0.75,
            thickness=15,
            tickfont=dict(size=11),
        ),
    )

    return fig


def agregar_overlay_confiabilidad_baja(
    fig: Figure,
    df_vista: pd.DataFrame,
    geo_mun: dict,
) -> Figure:
    """
    Agrega un overlay con patrón para municipios CONFIABILIDAD = BAJA.
    Usa un segundo trace choropleth con opacidad y patrón visual.
    """
    codigos_baja = set(
        df_vista.loc[df_vista["CONFIABILIDAD"] == "BAJA", "DIVIPOLA"]
        .astype(str)
        .str.strip()
        .str.zfill(5)
    )

    if not codigos_baja:
        return fig

    # Crear dataframe solo con municipios BAJA
    df_baja = df_vista[
        df_vista["DIVIPOLA"].astype(str).str.strip().str.zfill(5).isin(codigos_baja)
    ].copy()

    if df_baja.empty:
        return fig

    # Agregar overlay translúcido usando colores RGBA
    fig.add_choropleth(
        geojson=geo_mun,
        locations=df_baja["DIVIPOLA"],
        featureidkey="properties.divipola_mun",
        z=[1] * len(df_baja),  # Valor constante
        colorscale=[[0, "rgba(201,76,76,0.15)"], [1, "rgba(201,76,76,0.25)"]],  # Rojo institucional translúcido
        zmin=0,
        zmax=1,
        showscale=False,
        hoverinfo="skip",
        name="Confiabilidad BAJA",
    )

    return fig


def crear_mapa_proyeccion_animado(
    df_vista: pd.DataFrame,
    df_proyeccion: pd.DataFrame,
    geo_mun: dict,
    escenario: str = "CENTRAL",
) -> Optional[Figure]:
    """
    Crea un mapa coroplético animado de la proyección 2026-2030.
    Usa la tabla municipal normalizada a formato largo.
    """
    columnas_requeridas = {
        "DIVIPOLA", "MUNICIPIO", "DPTO", "ANIO", "ESCENARIO", "PROYECCION"
    }
    if not columnas_requeridas.issubset(df_proyeccion.columns):
        return None

    codigos_vista = set(df_vista["DIVIPOLA"].astype(str).str.strip().str.zfill(5))
    proy_filtrado = df_proyeccion[
        df_proyeccion["DIVIPOLA"].astype(str).str.strip().str.zfill(5).isin(codigos_vista)
        & df_proyeccion["ESCENARIO"].astype(str).str.upper().eq(escenario.upper())
    ].copy()

    if proy_filtrado.empty:
        return None

    proy_filtrado["DIVIPOLA"] = (
        proy_filtrado["DIVIPOLA"].astype(str).str.strip().str.zfill(5)
    )
    proy_filtrado["ANIO"] = pd.to_numeric(proy_filtrado["ANIO"], errors="coerce")
    proy_filtrado["PROYECCION"] = pd.to_numeric(proy_filtrado["PROYECCION"], errors="coerce")
    df_anim = proy_filtrado.dropna(subset=["ANIO", "PROYECCION"]).copy()

    if df_anim.empty:
        return None

    df_anim["ANIO"] = df_anim["ANIO"].astype(int)
    max_proyeccion = float(df_anim["PROYECCION"].max())

    fig = px.choropleth(
        df_anim,
        geojson=geo_mun,
        locations="DIVIPOLA",
        featureidkey="properties.divipola_mun",
        color="PROYECCION",
        animation_frame="ANIO",
        animation_group="DIVIPOLA",
        color_continuous_scale="YlOrRd",
        range_color=(0, max(max_proyeccion * 1.1, 1)),
        category_orders={"ANIO": [2026, 2027, 2028, 2029, 2030]},
        title=f"Proyección municipal {escenario} 2026–2030 (animado)",
        hover_name="MUNICIPIO",
        hover_data={"DIVIPOLA": True, "DPTO": True, "PROYECCION": ":.0f"},
    )

    fig.update_layout(
        height=460,
        margin=dict(l=0, r=0, t=50, b=0),
        transition={"duration": 800, "easing": "cubic-in-out"},
        coloraxis_colorbar=dict(
            title="Casos esperados",
            len=0.7,
            thickness=12,
            tickfont=dict(size=10),
        ),
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
    )

    return fig


# ============================================================
# PREPARACIÓN DE DATOS PARA MAPAS
# ============================================================

def preparar_datos_mapa_departamental(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega datos municipales a nivel departamental para mapa."""
    return (
        df.groupby(["CODDPTO", "DPTO"], as_index=False)["PROY_2030"]
        .sum(min_count=1)
    )