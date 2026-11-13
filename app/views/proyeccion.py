"""
Página: Proyección 2026-2030 - NUTRIPREDICT Colombia 2030
"""

import streamlit as st
import pandas as pd

from app.charts import (
    crear_proyeccion_nacional,
    crear_proyeccion_departamental,
    crear_proyeccion_municipal,
    tabla_escenarios,
    FORMATO_ESCENARIOS,
)
from app.filters import (
    render_active_filters_chips,
    selector_proyeccion_departamental,
    selector_proyeccion_municipal,
)


def render_tab_proyeccion(
    proy_nacional: pd.DataFrame,
    proy_departamental: pd.DataFrame,
    proy_municipal: pd.DataFrame,
):
    """Renderiza la pestaña Proyección 2026-2030."""
    render_active_filters_chips("proyeccion")
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
        # Validar columnas
        columnas_requeridas = {"ANIO", "ESCENARIO", "PROYECCION"}
        faltan = columnas_requeridas - set(proy_nacional.columns)
        if faltan:
            st.error(
                "La hoja Proy_Nacional no contiene estas columnas: "
                + ", ".join(sorted(faltan))
            )
            st.write("Columnas disponibles:", proy_nacional.columns.tolist())
            return

        fig = crear_proyeccion_nacional(proy_nacional)
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False, "responsive": True},
            alt="Escenarios nacionales de proyección de casos notificados de 2026 a 2030",
        )

        with st.expander("Ver proyección nacional"):
            st.dataframe(
                tabla_escenarios(proy_nacional),
                hide_index=True,
                width="stretch",
                column_config=FORMATO_ESCENARIOS,
                alt="Tabla nacional de proyecciones por año y escenario",
            )

    elif nivel_proyeccion == "Departamental":
        # Validar columnas
        columnas_requeridas = {"CODDPTO", "DEPARTAMENTO", "ANIO", "ESCENARIO", "PROYECCION"}
        faltan = columnas_requeridas - set(proy_departamental.columns)
        if faltan:
            st.error(
                "La hoja Proy_Departamental no contiene estas columnas: "
                + ", ".join(sorted(faltan))
            )
            st.write("Columnas disponibles:", proy_departamental.columns.tolist())
            return

        departamento_proyeccion = selector_proyeccion_departamental(
            proy_departamental, "proyeccion"
        )

        if not departamento_proyeccion:
            return

        df_departamento = proy_departamental.loc[
            proy_departamental["DEPARTAMENTO"] == departamento_proyeccion
        ].copy()

        if df_departamento.empty:
            st.warning("No hay proyección departamental para este departamento.")
            return

        fig = crear_proyeccion_departamental(df_departamento, departamento_proyeccion)
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False, "responsive": True},
            alt=f"Escenarios de proyección de casos notificados para {departamento_proyeccion}",
        )

        with st.expander("Ver proyección departamental"):
            st.dataframe(
                tabla_escenarios(df_departamento),
                hide_index=True,
                width="stretch",
                column_config=FORMATO_ESCENARIOS,
                alt=f"Tabla de proyecciones por año y escenario para {departamento_proyeccion}",
            )

    else:  # Municipal
        # Validar columnas
        columnas_requeridas = {"DIVIPOLA", "DPTO", "MUNICIPIO", "ANIO", "ESCENARIO", "PROYECCION"}
        faltan = columnas_requeridas - set(proy_municipal.columns)
        if faltan:
            st.error(
                "La hoja Proy_Municipal no contiene estas columnas: "
                + ", ".join(sorted(faltan))
            )
            st.write("Columnas disponibles:", proy_municipal.columns.tolist())
            return

        departamento_proyeccion, municipio_proyeccion = selector_proyeccion_municipal(
            proy_municipal, "proyeccion"
        )

        if not departamento_proyeccion or not municipio_proyeccion:
            return

        df_municipio = proy_municipal.loc[
            (proy_municipal["DPTO"] == departamento_proyeccion)
            & (proy_municipal["MUNICIPIO"] == municipio_proyeccion)
        ].copy()

        if df_municipio.empty:
            st.warning("No hay proyección municipal para este municipio.")
            return

        fig = crear_proyeccion_municipal(df_municipio, municipio_proyeccion, departamento_proyeccion)
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False, "responsive": True},
            alt=f"Escenarios de proyección de casos notificados para {municipio_proyeccion}, {departamento_proyeccion}",
        )

        with st.expander("Ver proyección municipal"):
            st.dataframe(
                tabla_escenarios(df_municipio),
                hide_index=True,
                width="stretch",
                column_config=FORMATO_ESCENARIOS,
                alt=f"Tabla de proyecciones por año y escenario para {municipio_proyeccion}",
            )

    st.info(
        "La proyección de largo plazo usa supuestos explícitos de crecimiento, "
        "amortiguamiento y escenarios. No debe interpretarse como una predicción "
        "determinista ni como una estimación de riesgo individual."
    )
