"""
Módulo de componentes UI - NUTRIPREDICT Colombia 2030
Componentes reutilizables: KPI cards, tarjetas de priorización, paginación, tooltips, badges.
"""

from pathlib import Path
import streamlit as st
import pandas as pd

from app.constants import (
    RANGO_COLORES,
    COLUMNAS_PRIORITARIAS,
    COLUMNAS_SECUNDARIAS,
    COLUMNAS_FORMATO,
    ORDEN_RANGO,
)


# ============================================================
# COMPONENTES DE MÉTRICAS KPI
# ============================================================

def render_metricas_kpi(
    total_municipios: int,
    criticos: int,
    alta: int,
    media: int,
    baja: int,
    total_proy: float,
    total_reales: float,
    ipr_prom: float,
    ipr_max: float,
    conf_baja: int,
):
    """Renderiza 4 tarjetas de métricas KPI arriba de la tabla de priorización."""
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.metric(
            "🏛️ Municipios",
            f"{total_municipios:,}",
            delta=f"Crít: {criticos} | Alt: {alta} | Med: {media} | Baj: {baja}",
            delta_color="off",
        )
    with col_m2:
        st.metric(
            "📊 Proyección 2030 (total)",
            f"{total_proy:,.0f}",
            delta=f"Casos reales: {total_reales:,.0f}",
            delta_color="normal",
        )
    with col_m3:
        st.metric(
            "📈 IPR promedio",
            f"{ipr_prom:.1f}",
            delta=f"Máx: {ipr_max:.1f}",
            delta_color="off",
        )
    with col_m4:
        pct_conf_baja = (conf_baja / total_municipios * 100) if total_municipios > 0 else 0
        st.metric(
            "⚠ Confiabilidad BAJA",
            f"{conf_baja:,}",
            delta=f"{pct_conf_baja:.0f}% del total",
            delta_color="inverse",
        )


# ============================================================
# PAGINACIÓN TÁCTIL
# ============================================================

def render_paginacion(
    total_rows: int,
    key_prefix: str = "prio",
    default_rows: int = 15,
) -> tuple[int, int, int]:
    """
    Renderiza controles de paginación táctil.
    Retorna (rows_per_page, start_idx, end_idx).
    """
    rows_per_page = st.selectbox(
        "Filas por página",
        [10, 15, 25, 50, 100],
        index=[10, 15, 25, 50, 100].index(default_rows) if default_rows in [10, 15, 25, 50, 100] else 1,
        key=f"rows_per_page_{key_prefix}",
    )

    total_pages = (total_rows + rows_per_page - 1) // rows_per_page

    page_key = f"page_{key_prefix}"
    if page_key not in st.session_state:
        st.session_state[page_key] = 1
    max_page = max(1, total_pages)
    if st.session_state[page_key] > max_page:
        st.session_state[page_key] = max_page
        st.session_state.pop(f"page_input_{key_prefix}", None)

    col_prev, col_page, col_next = st.columns([1, 3, 1])

    with col_prev:
        if st.button("⬅ Anterior", key=f"prev_{key_prefix}", disabled=(st.session_state[page_key] <= 1), width="stretch"):
            st.session_state[page_key] -= 1
            st.rerun()

    with col_page:
        page_input = st.number_input(
            f"Página (1-{total_pages})",
            min_value=1,
            max_value=max_page,
            value=st.session_state[page_key],
            step=1,
            key=f"page_input_{key_prefix}",
            label_visibility="collapsed",
        )
        if page_input != st.session_state[page_key]:
            st.session_state[page_key] = page_input
            st.rerun()

    with col_next:
        if st.button("Siguiente ➡", key=f"next_{key_prefix}", disabled=(st.session_state[page_key] >= total_pages), width="stretch"):
            st.session_state[page_key] += 1
            st.rerun()

    start_idx = (st.session_state[page_key] - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)

    st.caption(f"Mostrando {start_idx + 1}–{end_idx} de {total_rows} municipios")

    return rows_per_page, start_idx, end_idx


# ============================================================
# TARJETAS DE PRIORIZACIÓN (VISTA MÓVIL)
# ============================================================

def render_tarjetas_prioridad(df_page: pd.DataFrame):
    """Renderiza una tarjeta por municipio (vista móvil apilada)."""
    for _, row in df_page.iterrows():
        rango = str(row.get("RANGO", "")).strip().upper()
        rango_color = RANGO_COLORES.get(rango, "#176B50")

        conf = str(row.get("CONFIABILIDAD", "")).strip().upper()
        conf_badge = "⚠ BAJA" if conf == "BAJA" else "✓ ADECUADA"
        conf_color = "#C94C4C" if conf == "BAJA" else "#176B50"

        st.markdown(
            f"""
            <div style="
                border: 1px solid #e0e6e3;
                border-left: 4px solid {rango_color};
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 0.75rem;
                background: #fafbfa;
            ">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem;">
                    <div>
                        <strong style="font-size: 1.1rem; color: #164C3B;">{row['MUNICIPIO']}</strong>
                        <span style="margin-left: 0.5rem; font-size: 0.85rem; color: #64746B;">({row['DPTO']})</span>
                    </div>
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        <span style="
                            background: {rango_color}; color: white;
                            padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600;
                        ">{rango}</span>
                        <span style="
                            background: {conf_color}; color: white;
                            padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.75rem;
                        ">{conf_badge}</span>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 0.5rem; margin-top: 0.75rem; font-size: 0.9rem;">
                    <div><strong>IPR:</strong> {row['IPR']:.2f}</div>
                    <div><strong>Casos reales:</strong> {row['CASOS_REALES']:.0f}</div>
                    <div><strong>Proyección 2030:</strong> {row['PROY_2030']:.0f}</div>
                    <div><strong>Rural:</strong> {row.get('RURAL', 0):.1f}%</div>
                    <div><strong>Indígena:</strong> {row.get('INDIGENA', 0):.1f}%</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# COLUMNAS Y FORMATO DE TABLA (usa constants.py)
# ============================================================

def get_column_config(col_name: str) -> dict:
    """Retorna configuración de columna para st.dataframe."""
    base = COLUMNAS_FORMATO.get(col_name, {"label": col_name, "width": "small"})
    if "format" in base:
        return st.column_config.NumberColumn(base["label"], format=base["format"], width=base["width"])
    return st.column_config.TextColumn(base["label"], width=base["width"])


def preparar_dataframe_prioridad(df: pd.DataFrame, mostrar_todo: bool = False) -> pd.DataFrame:
    """Prepara y ordena el DataFrame de priorización."""
    df_prio = df.copy()
    df_prio["IPR"] = pd.to_numeric(df_prio["IPR"], errors="coerce")

    if "RANGO" in df_prio.columns:
        df_prio["ORDEN_RANGO"] = (
            df_prio["RANGO"]
            .astype("string")
            .str.strip()
            .str.upper()
            .map(ORDEN_RANGO)
            .fillna(99)
        )
        df_prio = df_prio.sort_values(["ORDEN_RANGO", "IPR"], ascending=[True, False], na_position="last")
        df_prio = df_prio.drop(columns="ORDEN_RANGO")
    else:
        df_prio = df_prio.sort_values("IPR", ascending=False, na_position="last")

    if mostrar_todo:
        cols_disponibles = [c for c in COLUMNAS_PRIORITARIAS + COLUMNAS_SECUNDARIAS if c in df_prio.columns]
    else:
        cols_disponibles = [c for c in COLUMNAS_PRIORITARIAS if c in df_prio.columns]

    return df_prio[cols_disponibles]


# ============================================================
# TOOLTIPS / GLOSARIO
# ============================================================

GLOSARIO = {
    "IPR": (
        "Índice de Priorización Relativa (0–100). "
        "Ordena municipios según volumen esperado (50%), ruralidad (25%) e indigenidad (25%). "
        "No es un diagnóstico ni mide riesgo individual."
    ),
    "CONFIABILIDAD": (
        "Clasifica la estabilidad del IPR según casos notificados en 24 meses. "
        "ADECUADA ≥ 10 casos; BAJA < 10 casos (IPR inestable, interpretar con precaución)."
    ),
    "RANGO": (
        "Clasificación por cuartiles del IPR: CRÍTICO (Q4), ALTO (Q3), MEDIO (Q2), BAJO (Q1). "
        "Sirve para priorizar visualmente; no implica umbrales de riesgo absoluto."
    ),
    "PROY_2030": (
        "Proyección de casos notificados esperados para 2030 (escenario central). "
        "Basado en nivel base (media 2023–2024), tendencia departamental encogida y tope ±10% anual "
        "amortiguado 15%/año. Es un escenario de planeación, no una predicción determinista."
    ),
    "RURAL": (
        "% de casos notificados en zonas rurales del municipio (con encogimiento K=20 hacia media nacional). "
        "Describe composición de notificaciones, no composición poblacional total."
    ),
    "INDIGENA": (
        "% de casos notificados en población indígena del municipio (con encogimiento K=20 hacia media nacional). "
        "Describe composición de notificaciones, no composición poblacional total."
    ),
    "CASOS_REALES": (
        "Casos notificados observados en el período de prueba (2024–2025). "
        "Unidad: notificación al evento 113 de SIVIGILA, no persona ni incidencia real."
    ),
    "CASOS_PRED": (
        "Casos predichos por el modelo seleccionado (LightGBM mensual / XGBoost semanal) "
        "en validación a un paso (usa información hasta el periodo anterior)."
    ),
    "ESCENARIO": (
        "Tres trayectorias de planeación 2026–2030: BAJO (−5 pp), CENTRAL (base), ALTO (+5 pp). "
        "Variación de crecimiento anual; no son intervalos de confianza estadísticos."
    ),
    "IC80": (
        "Intervalo de credibilidad 80% (log-normal, σ departamental=0.291, nacional=0.155). "
        "Retro-validado solo hasta horizonte 6 meses; más allá es supuesto de planeación."
    ),
    "DIVIPOLA": (
        "Código único de 5 dígitos (DANE) que identifica el municipio de residencia. "
        "Primeros 2 dígitos = código de departamento."
    ),
    "SIVIGILA_113": (
        "Sistema de Vigilancia en Salud Pública (Colombia). "
        "Evento 113 = Desnutrición aguda en menores de 5 años. "
        "Fuente primaria de todos los datos de esta app."
    ),
}


def tooltip(term: str, label: str = None) -> str:
    """
    Genera HTML para un término con tooltip del glosario.
    Uso: st.markdown(tooltip("IPR", "IPR"), unsafe_allow_html=True)
    """
    definition = GLOSARIO.get(term.upper(), "")
    display = label or term
    if definition:
        return (
            f'<span class="np-tooltip" data-tooltip="{definition}" tabindex="0">'
            f'{display}</span>'
        )
    return display


def render_glosario():
    """Renderiza el glosario técnico en 3 columnas."""
    st.markdown("---")
    st.markdown("### 📖 Glosario técnico interactivo")
    st.caption(
        "Pasa el cursor (o toca en móvil) sobre los términos subrayados para ver su definición. "
        "Los tooltips funcionan en hover (desktop) y tap (móvil)."
    )

    glosario_items = list(GLOSARIO.items())
    cols = st.columns(3)
    for idx, (term, definition) in enumerate(glosario_items):
        with cols[idx % 3]:
            st.markdown(
                f'<div class="np-tooltip" data-tooltip="{definition}" tabindex="0">'
                f'<strong>{term}</strong></div>',
                unsafe_allow_html=True,
            )
            st.caption(definition[:120] + "…" if len(definition) > 120 else definition)


# ============================================================
# BADGES SEMÁNTICOS
# ============================================================

def badge_rango(rango: str) -> str:
    """Genera HTML para badge de rango."""
    colores = {
        "CRITICO": "#C94C4C",
        "ALTO": "#E5B94B",
        "MEDIO": "#176B50",
        "BAJO": "#64746B",
    }
    color = colores.get(str(rango).strip().upper(), "#176B50")
    return (
        f'<span style="background: {color}; color: white; '
        f'padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600;">'
        f'{rango}</span>'
    )


def badge_confiabilidad(conf: str) -> str:
    """Genera HTML para badge de confiabilidad."""
    es_baja = str(conf).strip().upper() == "BAJA"
    color = "#C94C4C" if es_baja else "#176B50"
    texto = "⚠ BAJA" if es_baja else "✓ ADECUADA"
    return (
        f'<span style="background: {color}; color: white; '
        f'padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.75rem;">'
        f'{texto}</span>'
    )


# ============================================================
# CARGA DE CSS EXTERNO
# ============================================================

@st.cache_data
def load_css() -> str:
    """Carga el archivo CSS externo y lo retorna como string."""
    css_path = Path(__file__).resolve().parents[1] / "app" / "styles.css"
    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            return f.read()
    return ""
