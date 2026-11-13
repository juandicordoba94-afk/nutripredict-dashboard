"""
Página: Metodología y limitaciones - NUTRIPREDICT Colombia 2030
"""

import streamlit as st

from app.filters import render_active_filters_chips
from app.components import render_glosario


def render_tab_metodologia():
    """Renderiza la pestaña Metodología y limitaciones."""
    render_active_filters_chips("metodologia")
    st.subheader("Metodología y limitaciones")

    st.markdown("### Qué mide NUTRIPREDICT")

    st.write(
        """
        NUTRIPREDICT analiza la evolución de las notificaciones de desnutrición
        aguda infantil correspondientes al evento 113 de SIVIGILA en Colombia.

        La unidad de análisis es la **notificación**, no la persona. Por ello,
        las cifras no deben interpretarse como incidencia real, prevalencia,
        riesgo individual ni diagnóstico clínico.
        """
    )

    st.markdown("### Fuentes y período")

    st.write(
        """
        - **Fuente principal:** notificaciones del evento 113 de SIVIGILA.
        - **Período analizado:** 2016 a 2025.
        - **Unidad territorial:** municipio de residencia, identificado con DIVIPOLA.
        - **Frecuencias:** mensual y semanal epidemiológica.
        - **Proyección:** 2026 a 2030.
        """
    )

    st.markdown("### Cómo se construyeron los modelos")

    st.write(
        """
        El análisis compara **tres familias de modelos** con enfoque de regresión de Poisson
        (adecuada para datos de conteo):

        - **LightGBM (Poisson)** — *boosting* de gradiente con pérdida de Poisson.
        - **XGBoost (Poisson)** — *boosting* de gradiente extremo con pérdida de Poisson.
        - **Random Forest** — ensamble de árboles de decisión.

        No se utilizan redes neuronales (GRU), modelos ARIMA/SARIMA, suavizamiento exponencial,
        Holt-Winters, ni modelos lineales generalizados (GLM) Poisson/binomial negativa.
        Estos no forman parte del pipeline de modelamiento actual.

        Los modelos usan información disponible hasta el periodo anterior (predicción a un paso).
        Para predecir un mes o una semana, no utilizan el valor del periodo que se quiere predecir.
        """
    )

    st.markdown("### Validación y selección")

    st.write(
        """
        La selección de modelos e hiperparámetros se realizó **únicamente con la
        validación de 2023** (entrenamiento 2017–2022). El período de prueba,
        2024–2025, se utilizó para evaluar el desempeño final, pero **no para elegir modelos**.

        - Modelo mensual seleccionado: **LightGBM (Poisson)** (menor RMSE en validación, nivel municipal).
        - Modelo semanal seleccionado: **XGBoost (Poisson)** (menor RMSE en validación, nivel municipal).

        Los mismos hiperparámetros se re-ajustan con datos hasta 2023 para la evaluación en prueba.
        """
    )

    st.markdown("### Proyecciones 2026–2030")

    st.write(
        """
        Las proyecciones de largo plazo son **escenarios de planeación**, no predicciones
        deterministas. Se construyen a partir de:

        1. **Nivel base:** media de los últimos 2 años completos (2023–2024).
        2. **Tendencia departamental:** pendiente log-lineal de 4 años (2020–2023), encogida
           hacia la tendencia nacional (parámetro K=300 casos).
        3. **Tope de crecimiento:** ±10% anual para el escenario central.
        4. **Amortiguación:** el crecimiento se reduce 15% cada año (factor 0.85) para evitar
           extrapolaciones extremas a 5 años.
        5. **Escenarios:** Central ± 5 puntos porcentuales de crecimiento anual
           (supuesto de planeación, no estimado estadísticamente).

        La incertidumbre se representa con intervalos IC80 log-normal (σ departamental=0.291,
        σ nacional=0.155), retro-validados solo hasta horizonte 6 meses.
        """
    )

    st.markdown("### Índice de priorización relativa (IPR)")

    st.write(
        """
        El IPR es un **índice relativo entre municipios** (0–100). Sirve para ordenar territorios
        según tres componentes ponderados (**supuestos de planeación**, no estimados):

        | Componente | Peso | Descripción |
        |------------|------|-------------|
        | Volumen esperado | 50% | Percentil de casos esperados a 12 meses (pronóstico recursivo LightGBM mensual, exploratorio). |
        | Ruralidad | 25% | Percentil de % casos rurales notificados (con encogimiento K=20 hacia media nacional). |
        | Indigenidad | 25% | Percentil de % casos indígenas notificados (con encogimiento K=20 hacia media nacional). |

        **Fórmula:** `IPR = 0.50 × Volumen + 0.25 × Ruralidad + 0.25 × Indigenidad`

        La tasa por 100.000 habitantes (**TASA_100K**) **no se calcula** por ausencia de datos
        poblacionales municipales actualizados. Si se aportara población, los pesos cambiarían a
        Volumen=20%, Tasa=40%, Ruralidad=20%, Indigenidad=20% (supuesto experto).

        El IPR se clasifica en cuartiles: **CRÍTICO** (Q4), **ALTO** (Q3), **MEDIO** (Q2), **BAJO** (Q1).

        El IPR **no es un diagnóstico**, no mide riesgo individual y no debe usarse
        para asignar recursos sin revisar el contexto territorial.
        """
    )

    st.markdown("### Limitaciones principales")

    with st.expander("⚠ Ver limitaciones detalladas (6 puntos)", expanded=False):
        st.warning(
            """
            **1. Notificaciones, no incidencia real.**  
            Las cifras corresponden a casos notificados al sistema de vigilancia. No
            capturan necesariamente todos los casos de desnutrición aguda infantil.
            """
        )
        st.warning(
            """
            **2. Cambios en la capacidad de notificación.**  
            Variaciones en la detección, reporte, acceso a servicios de salud o
            actualización de registros pueden afectar las tendencias observadas.
            """
        )
        st.warning(
            """
            **3. Municipios con baja confiabilidad.**  
            Los municipios con pocos casos notificados en los últimos dos años tienen
            proyecciones e índices más inestables. Deben interpretarse con precaución.
            (555 de 1119 municipios tienen CONFIABILIDAD = BAJA, < 10 casos en 24 meses).
            """
        )
        st.warning(
            """
            **4. Ruralidad e indigenidad.**  
            Las variables de ruralidad e indigenidad describen la composición de los
            casos notificados, no la composición poblacional total del municipio.
            """
        )
        st.warning(
            """
            **5. Proyecciones de largo plazo.**  
            Las proyecciones 2026–2030 dependen de supuestos explícitos y no incorporan
            cambios futuros en políticas públicas, financiación, cobertura de salud,
            seguridad alimentaria, migración, conflictos o capacidad de notificación.
            """
        )
        st.warning(
            """
            **6. Cobertura cartográfica.**  
            Algunos territorios pueden aparecer en los resultados pero no tener geometría
            disponible en la cartografía utilizada. Esto no elimina sus resultados, pero
            impide mostrarlos en el mapa municipal.
            """
        )

    st.markdown("### Uso responsable")

    st.info(
        """
        Este dashboard es una herramienta de exploración y priorización relativa.
        No reemplaza la vigilancia epidemiológica, la valoración clínica, la
        intervención territorial ni la toma de decisiones basada en evidencia local.
        """
    )

    st.info(
        """
        Para decisiones operativas, el IPR debe complementarse con información local:
        población infantil, cobertura de servicios, acceso a alimentos, condiciones
        socioeconómicas, capacidad institucional y evidencia territorial.
        """
    )

    # Glosario técnico interactivo
    render_glosario()