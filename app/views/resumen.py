"""Resumen ejecutivo con indicadores derivados de los resultados existentes."""

import pandas as pd
import streamlit as st

from app.charts import crear_proyeccion_nacional
from app.filters import render_active_filters_chips
from app.maps import render_mapa_resumen


def _abrir_exploracion_territorial() -> None:
    st.session_state["seccion_dashboard"] = "Panorama territorial"


def render_resumen(
    df: pd.DataFrame, proy_nacional: pd.DataFrame
) -> None:
    """Presenta una síntesis descriptiva; no recalcula métricas científicas."""
    render_active_filters_chips("resumen")
    st.subheader("Resumen nacional")
    st.caption(
        "Panorama de resultados municipales, priorización relativa y escenarios de casos notificados. "
        "Use el filtro de departamento para explorar un territorio."
    )

    df_vista = df.copy()
    departamento = st.session_state.get("filtro_departamento", "Todos")
    if departamento != "Todos":
        df_vista = df_vista.loc[df_vista["DPTO"] == departamento]

    if df_vista.empty:
        st.info("No hay resultados para los filtros seleccionados.")
        return

    municipios = len(df_vista)
    criticos = int(df_vista["RANGO"].astype("string").str.upper().eq("CRITICO").sum())
    proyeccion = pd.to_numeric(df_vista["PROY_2030"], errors="coerce").sum(min_count=1)
    confiabilidad_baja = int(
        df_vista["CONFIABILIDAD"].astype("string").str.upper().eq("BAJA").sum()
    )

    with st.container(horizontal=True):
        st.metric("Municipios con resultados", f"{municipios:,}", border=True)
        st.metric("Clasificados como críticos", f"{criticos:,}", border=True)
        st.metric(
            "Proyección central 2030",
            f"{proyeccion:,.0f}" if pd.notna(proyeccion) else "Sin dato",
            border=True,
        )
        st.metric("Con confiabilidad baja", f"{confiabilidad_baja:,}", border=True)

    resumen_contexto = (
        "Los indicadores resumen los registros incluidos en los resultados municipales. "
        "La proyección corresponde al escenario central y el IPR expresa prioridad relativa."
    )
    if departamento != "Todos":
        resumen_contexto += " La gráfica de escenarios conserva el alcance nacional."
    st.caption(resumen_contexto)

    with st.container(border=True):
        st.markdown("#### Escenarios nacionales 2026–2030")
        if {"ANIO", "ESCENARIO", "PROYECCION"}.issubset(proy_nacional.columns):
            proyeccion_nacional = proy_nacional.loc[
                pd.to_numeric(proy_nacional["ANIO"], errors="coerce").between(2026, 2030)
            ].copy()
            if proyeccion_nacional.empty:
                st.info("No hay escenarios nacionales disponibles entre 2026 y 2030.")
            else:
                fig = crear_proyeccion_nacional(proyeccion_nacional)
                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={"displayModeBar": False, "responsive": True},
                    key="resumen_proyeccion_nacional",
                    alt="Escenarios nacionales de casos notificados proyectados entre 2026 y 2030",
                )
        else:
            st.info("La proyección nacional no tiene las columnas necesarias para mostrarse.")

    with st.container(border=True):
        st.markdown("#### Vista rápida de prioridad municipal")
        st.caption(
            "El color resume el IPR. Busca municipios, cambia indicadores y consulta su historia en "
            "Panorama territorial."
        )
        geo_mun = st.session_state.get("geojson_municipios_resumen")
        if isinstance(geo_mun, dict):
            render_mapa_resumen(df_vista, geo_mun)
        else:
            st.warning(
                "No se recibió el GeoJSON municipal para el mapa resumido. "
                "Reinicia Streamlit para cargar los datos actualizados."
            )
        st.button(
            "Explorar el mapa territorial",
            icon=":material/map:",
            key="ir_exploracion_territorial",
            on_click=_abrir_exploracion_territorial,
        )
    with st.container(border=True):
        st.markdown("#### Municipios con mayor IPR")
        columnas = [
            c for c in ["MUNICIPIO", "DPTO", "IPR", "RANGO", "CONFIABILIDAD"]
            if c in df_vista.columns
        ]
        top = df_vista.sort_values("IPR", ascending=False, na_position="last").loc[:, columnas].head(8)
        st.dataframe(
            top,
            hide_index=True,
            width="stretch",
            column_config={
                "IPR": st.column_config.NumberColumn("IPR", format="%.1f"),
                "MUNICIPIO": st.column_config.TextColumn("Municipio", width="medium"),
                "DPTO": st.column_config.TextColumn("Departamento", width="small"),
            },
            height=360,
            alt="Municipios con mayor índice de priorización relativa",
        )
