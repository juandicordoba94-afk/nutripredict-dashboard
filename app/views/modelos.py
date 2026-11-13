"""
Página: Modelos y calidad - NUTRIPREDICT Colombia 2030
"""

import streamlit as st
import pandas as pd
import json

from app.filters import render_active_filters_chips


def render_tab_modelos(
    seleccion_modelos: dict,
    metricas_modelos: pd.DataFrame,
    calidad_datos: dict,
):
    """Renderiza la pestaña Modelos y calidad."""
    render_active_filters_chips("modelos")
    st.subheader("Modelos y calidad de los datos")

    st.caption(
        "Esta sección muestra el desempeño de los modelos en validación y prueba, "
        "así como los controles de calidad aplicados a los datos de SIVIGILA."
    )

    # Modelos seleccionados
    st.markdown("### Modelos seleccionados")

    if not isinstance(seleccion_modelos, dict):
        st.error("El archivo seleccion_modelos.json no tiene la estructura esperada.")
        return

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
            width="stretch",
            alt="Modelos seleccionados por frecuencia y nivel territorial",
        )
    else:
        st.info("No se encontraron modelos seleccionados en el archivo JSON.")

    # Métricas de los modelos
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
        c for c in columnas_metricas if c in metricas.columns
    ]

    if not columnas_disponibles:
        st.error("El archivo metricas_modelos.csv no contiene las columnas esperadas.")
        st.write("Columnas disponibles:", metricas.columns.tolist())
        return

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
        st.warning("No hay métricas para la combinación seleccionada.")
    else:
        orden_metricas = [
            c for c in columnas_metricas if c in metricas_filtradas.columns
        ]

        metricas_filtradas = metricas_filtradas[orden_metricas]

        st.dataframe(
            metricas_filtradas,
            hide_index=True,
            width="stretch",
            alt="Métricas filtradas de validación y prueba por modelo",
        )

    st.download_button(
        label="Descargar métricas filtradas en CSV",
        data=metricas_filtradas.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
        file_name="metricas_modelos_filtradas.csv",
        mime="text/csv",
    )

    # Calidad de los datos
    st.markdown("### Calidad de los datos")

    if not isinstance(calidad_datos, dict):
        st.error("El archivo calidad_datos.json no tiene la estructura esperada.")
        return

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
        width="stretch",
        alt="Resumen de indicadores de calidad de los datos",
    )

    if isinstance(calidad_datos.get("exclusiones"), dict):
        with st.expander("Detalle de filas excluidas"):
            st.dataframe(
                pd.DataFrame(
                    list(calidad_datos["exclusiones"].items()),
                    columns=["Motivo", "Filas"],
                ),
                hide_index=True,
                width="stretch",
                alt="Conteo de filas excluidas por motivo",
            )

    if calidad_datos.get("fechas_por_ano_archivo"):
        with st.expander("Revisión de fechas por año"):
            st.dataframe(
                pd.DataFrame(calidad_datos["fechas_por_ano_archivo"]),
                hide_index=True,
                width="stretch",
                alt="Revisión de fechas disponibles por año y archivo",
            )

    if isinstance(calidad_datos.get("conciliacion_totales"), dict):
        with st.expander("Conciliación de totales"):
            st.dataframe(
                pd.DataFrame(
                    list(calidad_datos["conciliacion_totales"].items()),
                    columns=["Panel", "Casos"],
                ),
                hide_index=True,
                width="stretch",
                alt="Conciliación de totales de casos por panel",
            )

    if calidad_datos.get("pct_faltante_por_columna"):
        with st.expander("Porcentaje de datos faltantes"):
            st.dataframe(
                pd.DataFrame(
                    list(calidad_datos["pct_faltante_por_columna"].items()),
                    columns=["Columna", "Porcentaje faltante"],
                ),
                hide_index=True,
                width="stretch",
                alt="Porcentaje de datos faltantes por columna",
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
