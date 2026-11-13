"""
Página: Mapa - NUTRIPREDICT Colombia 2030
"""

import streamlit as st
import pandas as pd

from app.maps import (
    render_mapa_departamental,
    render_exploracion_territorial,
)
from app.filters import render_active_filters_chips


def render_tab_mapa(
    df: pd.DataFrame,
    geo_dep: dict,
    geo_mun: dict,
):
    """Renderiza la exploración territorial completa."""
    render_active_filters_chips("mapa")

    panel_mensual = st.session_state.get("panel_mensual_mapa")
    if not isinstance(panel_mensual, pd.DataFrame):
        st.error(
            "No se recibió el panel mensual para el mapa. Reinicia Streamlit "
            "para cargar la versión actual de la vista territorial."
        )
        return

    # Aplicar filtros globales
    df_vista = df.copy()
    nivel = st.session_state["filtro_nivel"]
    departamento = st.session_state["filtro_departamento"]

    if departamento != "Todos":
        df_vista = df_vista[df_vista["DPTO"] == departamento]

    if df_vista.empty:
        st.info("No hay municipios para los filtros seleccionados. Restablece o cambia el departamento.")
        return

    if nivel != "Departamentos":
        st.subheader("Exploración territorial")
        st.caption(
            "Busca un municipio, cambia la capa y selecciónalo para consultar los valores e historia mensual. "
            "El mapa usa casos notificados y resultados municipales existentes."
        )
        render_exploracion_territorial(df_vista, geo_mun, panel_mensual)
        return

    requeridas = {"CODDPTO", "DPTO", "PROY_2030"}
    faltan = requeridas - set(df_vista.columns)
    if faltan:
        st.error("No se puede construir el mapa departamental. Faltan columnas: " + ", ".join(sorted(faltan)))
        return

    codigos_geo = {
        str(feature.get("properties", {}).get("divipola_dep", "")).strip().zfill(2)
        for feature in geo_dep.get("features", [])
    }
    codigos_datos = set(df_vista["CODDPTO"].astype("string").str.strip().str.zfill(2))
    if not codigos_datos.intersection(codigos_geo):
        st.warning("Los departamentos filtrados no coinciden con códigos del GeoJSON departamental.")
        return
    sin_geometria = len(codigos_datos - codigos_geo)
    if sin_geometria:
        st.warning(f"Hay {sin_geometria} departamento(s) con resultados sin geometría; no aparecen en el mapa.")
    st.subheader("Exploración departamental")
    st.caption("Proyección central 2030 agregada desde los resultados municipales.")
    render_mapa_departamental(df_vista, geo_dep, departamento)
