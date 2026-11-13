"""
Página: Evolución mensual - NUTRIPREDICT Colombia 2030
"""

import streamlit as st
import pandas as pd

from app.charts import crear_linea_mensual
from app.filters import (
    render_active_filters_chips,
    selector_departamento_municipal,
    slider_rango_fechas,
)


def render_tab_mensual(panel_mensual: pd.DataFrame):
    """Renderiza la pestaña Evolución mensual."""
    render_active_filters_chips("mensual")
    st.subheader("Evolución mensual por municipio")

    requeridas = {
        "Departamentoresidencia", "Municipioresidencia", "ANIOMESDT",
        "CASOS", "CASOSRURAL", "CASOSINDIGENA",
    }
    faltan = requeridas - set(panel_mensual.columns)
    if faltan:
        st.error("No se puede mostrar la evolución mensual. Faltan columnas: " + ", ".join(sorted(faltan)))
        st.caption("Columnas recibidas del panel: " + ", ".join(map(str, panel_mensual.columns)))
        return
    if panel_mensual.empty:
        st.info("El panel mensual está vacío; no hay observaciones para graficar.")
        return

    st.caption(
        "La línea muestra casos notificados por municipio y mes. "
        "No representa incidencia real ni riesgo individual."
    )

    # Selector departamento → municipio
    departamento_mensual, municipio_mensual = selector_departamento_municipal(
        panel_mensual, "mensual", "Departamento", "Municipio"
    )

    if not departamento_mensual or not municipio_mensual:
        st.warning("No hay departamentos o municipios disponibles en el panel mensual.")
        return

    # Filtrar datos
    df_mensual = panel_mensual.loc[
        (panel_mensual["Departamentoresidencia"] == departamento_mensual)
        & (panel_mensual["Municipioresidencia"] == municipio_mensual)
    ].copy()

    if df_mensual.empty:
        st.warning("No hay datos mensuales para este municipio.")
        return

    df_mensual["ANIOMESDT"] = pd.to_datetime(df_mensual["ANIOMESDT"], errors="coerce")
    df_mensual = df_mensual.dropna(subset=["ANIOMESDT"]).sort_values("ANIOMESDT")

    if df_mensual.empty:
        st.warning("No hay fechas válidas en los datos mensuales.")
        return

    # Slider de rango de fechas
    rango = slider_rango_fechas(
        df_mensual, "ANIOMESDT", "rango_mensual", formato="MM/YYYY"
    )

    if rango:
        fecha_inicio, fecha_fin = rango
        df_mensual = df_mensual.loc[
            (df_mensual["ANIOMESDT"] >= pd.Timestamp(fecha_inicio))
            & (df_mensual["ANIOMESDT"] <= pd.Timestamp(fecha_fin))
        ]

    if df_mensual.empty:
        st.warning("No hay datos en el rango de fechas seleccionado.")
        return

    # Gráfica
    fig = crear_linea_mensual(df_mensual, municipio_mensual, departamento_mensual)
    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False, "responsive": True},
        alt=f"Evolución mensual de casos notificados en {municipio_mensual}, {departamento_mensual}",
    )

    # Expander con datos
    with st.expander("Ver datos mensuales"):
        st.dataframe(
            df_mensual[["ANIOMESDT", "CASOS", "CASOSRURAL", "CASOSINDIGENA"]],
            hide_index=True,
            width="stretch",
            alt=f"Datos mensuales de casos notificados para {municipio_mensual}",
        )

    # Descarga CSV
    st.download_button(
        label="Descargar datos mensuales en CSV",
        data=df_mensual.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        file_name=f"evolucion_mensual_{municipio_mensual.replace(' ', '_')}.csv",
        mime="text/csv",
    )
