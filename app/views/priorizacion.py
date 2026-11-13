"""
Página: Priorización municipal - NUTRIPREDICT Colombia 2030
"""

import streamlit as st
import pandas as pd

from app.components import (
    render_metricas_kpi,
    render_paginacion,
    render_tarjetas_prioridad,
    preparar_dataframe_prioridad,
    get_column_config,
)
from app.filters import render_active_filters_chips


def render_tab_priorizacion(df: pd.DataFrame):
    """Renderiza la pestaña Priorización municipal."""
    render_active_filters_chips("priorizacion")
    st.subheader("Priorización municipal")

    st.caption(
        "La tabla muestra los municipios con mayor índice de Priorización Relativa (IPR). "
        "El IPR es una prioridad relativa entre municipios, no un diagnóstico individual. "
        "TASA_100K no se calcula por ausencia de datos poblacionales."
    )

    # Aplicar filtros globales
    df_vista = df.copy()
    if st.session_state["filtro_departamento"] != "Todos":
        df_vista = df_vista[df_vista["DPTO"] == st.session_state["filtro_departamento"]]

    if df_vista.empty:
        st.info("No hay resultados de priorización para el departamento seleccionado.")
        return

    requeridas = {"RANGO", "PROY_2030", "CASOS_REALES", "IPR", "CONFIABILIDAD"}
    faltan = requeridas - set(df_vista.columns)
    if faltan:
        st.error("No se puede mostrar la priorización. Faltan columnas: " + ", ".join(sorted(faltan)))
        st.caption("Columnas disponibles: " + ", ".join(map(str, df_vista.columns)))
        return

    # Preparar y ordenar DataFrame
    mostrar_todo = st.checkbox(
        "Mostrar todas las columnas",
        value=False,
        key="show_all_cols",
    )

    df_prioridad = preparar_dataframe_prioridad(df_vista, mostrar_todo)

    if df_prioridad.empty:
        st.info("No hay columnas de priorización disponibles para mostrar.")
        return

    # Métricas KPI
    total_municipios = len(df_prioridad)
    criticos = len(df_prioridad[df_prioridad["RANGO"] == "CRITICO"])
    alta = len(df_prioridad[df_prioridad["RANGO"] == "ALTO"])
    media = len(df_prioridad[df_prioridad["RANGO"] == "MEDIO"])
    baja = len(df_prioridad[df_prioridad["RANGO"] == "BAJO"])
    total_proy = df_prioridad["PROY_2030"].sum()
    total_reales = df_prioridad["CASOS_REALES"].sum()
    ipr_prom = df_prioridad["IPR"].mean()
    ipr_max = df_prioridad["IPR"].max()
    conf_baja = len(df_prioridad[df_prioridad["CONFIABILIDAD"] == "BAJA"])

    render_metricas_kpi(
        total_municipios, criticos, alta, media, baja,
        total_proy, total_reales, ipr_prom, ipr_max, conf_baja
    )

    # Toggle vista tarjeta/tabla
    vista_tarjeta = st.toggle(
        "🃏 Vista tarjetas (móvil)",
        value=False,
        key="vista_tarjetas_prioridad",
        help="Activa para ver municipios como tarjetas apiladas (mejor en móvil)",
    )

    # Paginación
    _, start_idx, end_idx = render_paginacion(len(df_prioridad), "prio", 15)

    # Slice de datos para la página actual
    tabla_prioridad = df_prioridad.iloc[start_idx:end_idx]

    # Renderizar vista
    if vista_tarjeta:
        # Las tarjetas incluyen ruralidad e indigenidad aunque la tabla compacta las oculte.
        df_tarjetas = preparar_dataframe_prioridad(df_vista, mostrar_todo=True)
        render_tarjetas_prioridad(df_tarjetas.iloc[start_idx:end_idx])
    else:
        # Vista tabla estándar
        column_config = {col: get_column_config(col) for col in tabla_prioridad.columns}
        st.dataframe(
            tabla_prioridad,
            hide_index=True,
            width="stretch",
            column_config=column_config,
            alt="Tabla de priorización municipal ordenada por rango e índice IPR",
        )

    # Descarga CSV completa (dataset filtrado completo, no solo página)
    cols_descarga = [c for c in df_prioridad.columns]
    st.download_button(
        label="Descargar tabla de priorizacion en CSV",
        data=df_prioridad[cols_descarga].to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        file_name="priorizacion_municipal.csv",
        mime="text/csv",
    )

    st.info(
        "Los municipios con confiabilidad baja tienen pocos casos notificados "
        "en los ultimos dos años; sus proyecciones e indices son mas inestables."
    )
