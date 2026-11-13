"""
Módulo de filtros - NUTRIPREDICT Colombia 2030
Centraliza la gestión de filtros globales y por tab.
"""

import streamlit as st
import pandas as pd


# ============================================================
# INICIALIZACIÓN Y RESET DE FILTROS GLOBALES
# ============================================================

def init_filters():
    """Inicializa filtros globales en session_state si no existen."""
    defaults = {
        "sidebar_open": False,
        "filtro_nivel": "Municipios",
        "filtro_departamento": "Todos",
        "filtro_municipio": None,  # Para tabs que lo usan
        "filtro_fecha_inicio": None,
        "filtro_fecha_fin": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_filters():
    """Restablece todos los filtros a valores por defecto."""
    st.session_state["filtro_nivel"] = "Municipios"
    st.session_state["filtro_departamento"] = "Todos"
    st.session_state["filtro_municipio"] = None
    st.session_state["filtro_fecha_inicio"] = None
    st.session_state["filtro_fecha_fin"] = None
    # También limpiar claves específicas de tabs
    for key in list(st.session_state.keys()):
        if key.startswith(("departamento_", "municipio_", "rango_")):
            del st.session_state[key]


# ============================================================
# APLICACIÓN DE FILTROS
# ============================================================

def aplicar_filtros_globales(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica filtros globales (nivel territorial + departamento) al DataFrame principal."""
    df_vista = df.copy()
    nivel = st.session_state["filtro_nivel"]
    departamento = st.session_state["filtro_departamento"]

    if departamento != "Todos":
        df_vista = df_vista[df_vista["DPTO"] == departamento]

    return df_vista, nivel, departamento


# ============================================================
# RENDERIZADO DE SIDEBAR Y CHIPS
# ============================================================

def render_sidebar_filtros(df: pd.DataFrame):
    """Renderiza los controles de filtros en el sidebar (solo si está abierto)."""
    if not st.session_state.get("sidebar_open", False):
        return

    st.sidebar.header("Filtros globales")

    # Nivel territorial — sincroniza con session_state
    nivel = st.sidebar.radio(
        "Nivel territorial",
        ["Departamentos", "Municipios"],
        horizontal=True,
        index=0 if st.session_state["filtro_nivel"] == "Departamentos" else 1,
        key="sidebar_nivel",
        on_change=lambda: setattr(st.session_state, "filtro_nivel", st.session_state["sidebar_nivel"]),
    )

    # Departamento — sincroniza con session_state
    departamentos_list = ["Todos"] + sorted(df["DPTO"].dropna().unique().tolist())
    dept_index = (
        departamentos_list.index(st.session_state["filtro_departamento"])
        if st.session_state["filtro_departamento"] in departamentos_list
        else 0
    )
    departamento = st.sidebar.selectbox(
        "Departamento",
        departamentos_list,
        index=dept_index,
        key="sidebar_departamento",
        on_change=lambda: setattr(st.session_state, "filtro_departamento", st.session_state["sidebar_departamento"]),
    )

    # Botón de reset en sidebar
    st.sidebar.divider()
    if st.sidebar.button("🔄 Restablecer filtros", use_container_width=True, key="reset_sidebar"):
        reset_filters()
        st.rerun()

    # Info de filtros activos en sidebar
    if st.session_state["filtro_nivel"] != "Municipios" or st.session_state["filtro_departamento"] != "Todos":
        st.sidebar.caption(
            f"Activo: {st.session_state['filtro_nivel']} • {st.session_state['filtro_departamento']}"
        )


def render_active_filters_chips(tab_key: str):
    """Muestra chips de filtros activos arriba de cada tab."""
    chips = []
    if st.session_state["filtro_nivel"] != "Municipios":
        chips.append(f"📍 Nivel: {st.session_state['filtro_nivel']}")
    if st.session_state["filtro_departamento"] != "Todos":
        chips.append(f"🏛️ Depto: {st.session_state['filtro_departamento']}")
    if st.session_state.get("filtro_municipio"):
        chips.append(f"🏘️ Mpio: {st.session_state['filtro_municipio']}")
    if st.session_state.get("filtro_fecha_inicio") and st.session_state.get("filtro_fecha_fin"):
        chips.append(f"📅 {st.session_state['filtro_fecha_inicio']} – {st.session_state['filtro_fecha_fin']}")

    if chips:
        chip_html = "".join(
            f'<span style="display:inline-block; background:#eaf3ed; color:#176b50; '
            f'padding:0.25rem 0.75rem; margin:0.25rem 0.5rem 0.25rem 0; '
            f'border-radius:999px; font-size:0.85rem; border:1px solid #176b50;">{c}</span>'
            for c in chips
        )
        st.markdown(
            f'<div style="margin-bottom:0.5rem;">{chip_html}</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "🔄 Restablecer filtros",
            key=f"reset_global_{tab_key}",
            use_container_width=False,
            help="Limpiar todos los filtros",
        ):
            reset_filters()
            st.rerun()


# ============================================================
# SELECTORES ESPECÍFICOS POR TAB
# ============================================================

def selector_departamento_municipal(
    panel: pd.DataFrame,
    key_prefix: str,
    label_depto: str = "Departamento",
    label_mpio: str = "Municipio",
) -> tuple[str | None, str | None]:
    """
    Selector encadenado de departamento → municipio para paneles mensual/semanal.
    Retorna (departamento, municipio) seleccionados.
    """
    departamentos = sorted(panel["Departamentoresidencia"].dropna().unique().tolist())
    if not departamentos:
        return None, None

    departamento = st.selectbox(label_depto, departamentos, key=f"{key_prefix}_departamento")

    municipios = (
        panel.loc[
            panel["Departamentoresidencia"] == departamento,
            "Municipioresidencia",
        ]
        .dropna()
        .unique()
        .tolist()
    )

    if not municipios:
        return departamento, None

    municipio = st.selectbox(label_mpio, sorted(municipios), key=f"{key_prefix}_municipio")
    return departamento, municipio


def selector_proyeccion_departamental(
    proy_departamental: pd.DataFrame,
    key_prefix: str,
) -> str | None:
    """Selector de departamento para proyección departamental."""
    if "DEPARTAMENTO" not in proy_departamental.columns:
        return None
    departamentos = sorted(proy_departamental["DEPARTAMENTO"].dropna().unique().tolist())
    if not departamentos:
        return None
    return st.selectbox("Departamento", departamentos, key=f"{key_prefix}_departamento_proyeccion")


def selector_proyeccion_municipal(
    proy_municipal: pd.DataFrame,
    key_prefix: str,
) -> tuple[str | None, str | None]:
    """Selector encadenado de departamento → municipio para proyección municipal."""
    if "DPTO" not in proy_municipal.columns:
        return None, None

    departamentos = sorted(proy_municipal["DPTO"].dropna().unique().tolist())
    if not departamentos:
        return None, None

    departamento = st.selectbox("Departamento", departamentos, key=f"{key_prefix}_departamento_proyeccion_mun")

    municipios = (
        proy_municipal.loc[
            proy_municipal["DPTO"] == departamento, "MUNICIPIO"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    if not municipios:
        return departamento, None

    municipio = st.selectbox("Municipio", sorted(municipios), key=f"{key_prefix}_municipio_proyeccion")
    return departamento, municipio


def slider_rango_fechas(
    df: pd.DataFrame,
    col_fecha: str,
    key: str,
    formato: str = "MM/YYYY",
) -> tuple | None:
    """
    Crea un slider de rango de fechas.
    Retorna (fecha_inicio, fecha_fin) o None si no hay datos válidos.
    """
    df_copy = df.copy()
    df_copy[col_fecha] = pd.to_datetime(df_copy[col_fecha], errors="coerce")
    df_copy = df_copy.dropna(subset=[col_fecha]).sort_values(col_fecha)

    if df_copy.empty:
        return None

    fecha_minima = df_copy[col_fecha].min()
    fecha_maxima = df_copy[col_fecha].max()

    if fecha_minima >= fecha_maxima:
        return None

    rango = st.slider(
        "Rango de fechas",
        min_value=fecha_minima.to_pydatetime(),
        max_value=fecha_maxima.to_pydatetime(),
        value=(fecha_minima.to_pydatetime(), fecha_maxima.to_pydatetime()),
        format=formato,
        key=key,
    )
    return rango