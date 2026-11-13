"""
Página: Mapa - NUTRIPREDICT Colombia 2030
"""

import streamlit as st
import pandas as pd

from app.maps import (
    crear_mapa_departamental,
    crear_mapa_municipal,
    agregar_overlay_confiabilidad_baja,
    crear_mapa_proyeccion_animado,
    preparar_datos_mapa_departamental,
)
from app.filters import render_active_filters_chips


def render_tab_mapa(df: pd.DataFrame, geo_dep: dict, geo_mun: dict, proy_municipal: pd.DataFrame):
    """Renderiza la pestaña Mapa."""
    render_active_filters_chips("mapa")

    # Aplicar filtros globales
    df_vista = df.copy()
    nivel = st.session_state["filtro_nivel"]
    departamento = st.session_state["filtro_departamento"]

    if departamento != "Todos":
        df_vista = df_vista[df_vista["DPTO"] == departamento]

    # Construir figura según nivel
    if nivel == "Departamentos":
        mapa = preparar_datos_mapa_departamental(df_vista)
        fig = crear_mapa_departamental(mapa, geo_dep)
    else:
        fig = crear_mapa_municipal(df_vista, geo_mun)
        # Overlay CONFIABILIDAD BAJA
        fig = agregar_overlay_confiabilidad_baja(fig, df_vista, geo_mun)

    st.plotly_chart(fig, use_container_width=True)

    # Mini-mapa proyección animado (solo nivel municipal)
    if nivel == "Municipios":
        st.markdown("---")
        st.subheader("📈 Proyección animada 2026–2030 (Escenario Central)")
        st.caption(
            "Mapa animado que muestra la evolución de la proyección central por municipio. "
            "Use el botón ▶ para reproducir. Los municipios con confiabilidad BAJA "
            "tienen proyecciones más inestables (ver overlay rojo en mapa principal)."
        )
        mapa_animado = crear_mapa_proyeccion_animado(
            df_vista,
            proy_municipal,
            geo_mun,
            "CENTRAL",
        )
        if mapa_animado:
            st.plotly_chart(mapa_animado, use_container_width=True)
        else:
            st.info("Datos de proyección municipal no disponibles para la vista actual.")

    st.caption(
        "El IPR es una prioridad relativa municipal, no un diagnostico individual. "
        "Rural e indigena corresponden a la composicion de los casos notificados, "
        "no a la composicion poblacional del municipio. "
        "⚠ Overlay rojo = CONFIABILIDAD BAJA (< 10 casos en 24 meses; IPR inestable)."
    )