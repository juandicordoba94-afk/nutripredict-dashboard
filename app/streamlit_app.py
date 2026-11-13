"""
NUTRIPREDICT Colombia 2030 - Orquestador principal
Aplicación Streamlit modularizada (< 200 líneas).
"""

import sys
from pathlib import Path

import streamlit as st

# Streamlit Cloud puede iniciar el script desde /app. Añade la raíz del
# repositorio para resolver el paquete `app` en cualquier directorio de ejecución.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import (
    inicializar_datos,
    init_filters,
    load_css,
)
from app.constants import PAGE_CONFIG
from app.views import (
    render_tab_priorizacion,
    render_tab_mensual,
    render_tab_semanal,
    render_tab_proyeccion,
    render_tab_modelos,
    render_tab_metodologia,
)
from app.views.mapa import render_tab_mapa
from app.views.resumen import render_resumen
from app.filters import render_sidebar_filtros


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
# CARGA DE DATOS (cacheada por archivo)
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
st.session_state["panel_mensual_mapa"] = panel_mensual
st.session_state["geojson_municipios_resumen"] = geo_mun


# ============================================================
# ENCABEZADO Y NAVEGACIÓN
# ============================================================
st.title("NUTRIPREDICT Colombia 2030")
st.caption(
    "Explora los casos notificados de desnutrición aguda en menores de 5 años en Colombia "
    "y consulta su evolución, proyecciones y prioridades por municipio (2016–2025)."
)

secciones = [
    "Resumen nacional",
    "Panorama territorial",
    "Priorización municipal",
    "Evolución mensual",
    "Evolución semanal",
    "Proyecciones 2026–2030",
    "Modelos y calidad",
    "Metodología y alcance",
]
seccion = st.selectbox(
    "Sección del dashboard",
    secciones,
    key="seccion_dashboard",
)

render_sidebar_filtros(df)

if seccion == "Resumen nacional":
    render_resumen(df, proy_nacional)
elif seccion == "Panorama territorial":
    render_tab_mapa(df, geo_dep, geo_mun)
elif seccion == "Priorización municipal":
    render_tab_priorizacion(df)
elif seccion == "Evolución mensual":
    render_tab_mensual(panel_mensual)
elif seccion == "Evolución semanal":
    render_tab_semanal(panel_semanal)
elif seccion == "Proyecciones 2026–2030":
    render_tab_proyeccion(proy_nacional, proy_departamental, proy_municipal)
elif seccion == "Modelos y calidad":
    render_tab_modelos(seleccion_modelos, metricas_modelos, calidad_datos)
else:
    render_tab_metodologia(data["cobertura"])
