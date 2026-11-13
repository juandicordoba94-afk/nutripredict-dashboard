"""
Página: Evolución semanal - NUTRIPREDICT Colombia 2030
"""

import streamlit as st
import pandas as pd

from app.charts import crear_linea_semanal
from app.filters import (
    render_active_filters_chips,
    selector_departamento_municipal,
    slider_rango_fechas,
)


def render_tab_semanal(panel_semanal: pd.DataFrame):
    """Renderiza la pestaña Evolución semanal."""
    render_active_filters_chips("semanal")
    st.subheader("Evolución semanal por municipio")

    requeridas = {
        "Departamentoresidencia", "Municipioresidencia", "SEMANAINI",
        "CASOS", "CASOSRURAL", "CASOSINDIGENA",
    }
    faltan = requeridas - set(panel_semanal.columns)
    if faltan:
        st.error("No se puede mostrar la evolución semanal. Faltan columnas: " + ", ".join(sorted(faltan)))
        st.caption("Columnas recibidas del panel: " + ", ".join(map(str, panel_semanal.columns)))
        return
    if panel_semanal.empty:
        st.info("El panel semanal está vacío; no hay observaciones para graficar.")
        return

    st.caption(
        "La línea muestra casos notificados por semana epidemiológica. "
        "No representa incidencia real ni riesgo individual."
    )

    # Selector departamento → municipio
    departamento_semanal, municipio_semanal = selector_departamento_municipal(
        panel_semanal, "semanal", "Departamento", "Municipio"
    )

    if not departamento_semanal or not municipio_semanal:
        st.warning("No hay departamentos o municipios disponibles en el panel semanal.")
        return

    # Filtrar datos
    df_semanal = panel_semanal.loc[
        (panel_semanal["Departamentoresidencia"] == departamento_semanal)
        & (panel_semanal["Municipioresidencia"] == municipio_semanal)
    ].copy()

    if df_semanal.empty:
        st.warning("No hay datos semanales para este municipio.")
        return

    df_semanal["SEMANAINI"] = pd.to_datetime(df_semanal["SEMANAINI"], errors="coerce")
    df_semanal = df_semanal.dropna(subset=["SEMANAINI"]).sort_values("SEMANAINI")

    if df_semanal.empty:
        st.warning("El panel no contiene fechas semanales válidas.")
        return

    # Slider de rango de fechas
    rango = slider_rango_fechas(
        df_semanal, "SEMANAINI", "rango_semanal", formato="DD/MM/YYYY"
    )

    if rango:
        fecha_inicio, fecha_fin = rango
        df_semanal = df_semanal.loc[
            (df_semanal["SEMANAINI"] >= pd.Timestamp(fecha_inicio))
            & (df_semanal["SEMANAINI"] <= pd.Timestamp(fecha_fin))
        ]

    if df_semanal.empty:
        st.warning("No hay datos en el rango de fechas seleccionado.")
        return

    # Gráfica
    fig = crear_linea_semanal(df_semanal, municipio_semanal, departamento_semanal)
    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False, "responsive": True},
        alt=f"Evolución semanal de casos notificados en {municipio_semanal}, {departamento_semanal}",
    )

    # Expander con datos
    with st.expander("Ver datos semanales"):
        st.dataframe(
            df_semanal[["SEMANAINI", "CASOS", "CASOSRURAL", "CASOSINDIGENA"]],
            hide_index=True,
            width="stretch",
            alt=f"Datos semanales de casos notificados para {municipio_semanal}",
        )

    # Descarga CSV
    st.download_button(
        label="Descargar datos semanales en CSV",
        data=df_semanal.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        file_name=f"evolucion_semanal_{municipio_semanal.replace(' ', '_')}.csv",
        mime="text/csv",
    )
