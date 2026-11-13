"""
NUTRIPREDICT Colombia 2030 - Orquestador principal
Aplicación Streamlit modularizada (< 200 líneas).
"""

import streamlit as st

from app import (
    inicializar_datos,
    init_filters,
    load_css,
)
from app.constants import PAGE_CONFIG, TABS
from app.pages import (
    render_tab_mapa,
    render_tab_priorizacion,
    render_tab_mensual,
    render_tab_semanal,
    render_tab_proyeccion,
    render_tab_modelos,
    render_tab_metodologia,
)
from app.components import tooltip


# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(**PAGE_CONFIG)

# Inicializar filtros globales
init_filters()

# Cargar e inyectar CSS
css_content = load_css()
if css_content:
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


# ============================================================
# CARGA DE DATOS (cacheada)
# ============================================================
data = inicializar_datos()

df = data["df"]
geo_dep = data["geo_dep"]
geo_mun = data["geo_mun"]
panel_mensual = data["panel_mensual"]
panel_semanal = data["panel_semanal"]
proy_nacional = data["proy_nacional"]
proy_departamental = data["proy_departamental"]
proy_municipal = data["proy_municipal"]
metricas_modelos = data["metricas_modelos"]
seleccion_modelos = data["seleccion_modelos"]
calidad_datos = data["calidad_datos"]


# ============================================================
# HEADER CON TÍTULO Y BOTÓN DE FILTROS
# ============================================================
st.markdown(
    """
    <div class="nutripredict-header">
        <div class="nutripredict-title"></div>
        <div class="nutripredict-filter-btn"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_title, col_filter = st.columns([0.85, 0.15])
with col_title:
    st.title("NUTRIPREDICT Colombia 2030")
    st.caption(
        f"Dashboard de {tooltip('IPR', 'priorización territorial')} para desnutrición aguda infantil en Colombia. "
        f"Basado en notificaciones del {tooltip('SIVIGILA_113', 'evento 113 de SIVIGILA')} (2016–2025)."
    )
with col_filter:
    if st.button("🔍 Filtros", use_container_width=True, key="toggle_sidebar"):
        st.session_state["sidebar_open"] = not st.session_state.get("sidebar_open", False)
        st.rerun()


# ============================================================
# JAVASCRIPT PARA SIDEBAR COLAPSABLE
# ============================================================
st.markdown(
    """
    <script>
    (function() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const toggleBtn = window.parent.document.querySelector('[data-testid="stButton"] button[key="toggle_sidebar"]');
        if (!sidebar || !toggleBtn) return;
        const observer = new MutationObserver(() => {
            const isOpen = sessionStorage.getItem('sidebar_open') === 'true';
            sidebar.style.transform = isOpen ? 'translateX(0)' : 'translateX(-100%)';
            sidebar.style.transition = 'transform 0.3s ease';
        });
        observer.observe(document.body, { attributes: true, subtree: true });
    })();
    </script>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR CON FILTROS GLOBALES
# ============================================================
from app.filters import render_sidebar_filtros
render_sidebar_filtros(df)


# ============================================================
# TABS PRINCIPALES
# ============================================================
tab_mapa, tab_priorizacion, tab_mensual, tab_semanal, tab_proyeccion, tab_modelos, tab_metodologia = st.tabs(
    [label for label, _ in TABS]
)

with tab_mapa:
    render_tab_mapa(df, geo_dep, geo_mun, proy_municipal)

with tab_priorizacion:
    render_tab_priorizacion(df)

with tab_mensual:
    render_tab_mensual(panel_mensual)

with tab_semanal:
    render_tab_semanal(panel_semanal)

with tab_proyeccion:
    render_tab_proyeccion(proy_nacional, proy_departamental, proy_municipal)

with tab_modelos:
    render_tab_modelos(seleccion_modelos, metricas_modelos, calidad_datos)

with tab_metodologia:
    render_tab_metodologia()