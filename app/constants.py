"""
Constantes compartidas - NUTRIPREDICT Colombia 2030
"""

# Paleta de colores institucional
COLORES_INSTITUCIONALES = {
    "verde_principal": "#176B50",
    "verde_oscuro": "#164C3B",
    "verde_claro": "#EAF3ED",
    "amarillo_alerta": "#E5B94B",
    "rojo_alerta": "#C94C4C",
    "gris_medio": "#64746B",
}

# Colores para escenarios
COLORES_ESCENARIOS = {
    "BAJO": "#E5B94B",      # Amarillo de alerta
    "CENTRAL": "#176B50",   # Verde institucional
    "ALTO": "#C94C4C",      # Rojo de alerta
}

# Orden de rangos
ORDEN_RANGO = {
    "CRITICO": 0,
    "ALTO": 1,
    "MEDIO": 2,
    "BAJO": 3,
}

# Colores por rango
RANGO_COLORES = {
    "CRITICO": "#C94C4C",
    "ALTO": "#E5B94B",
    "MEDIO": "#176B50",
    "BAJO": "#64746B",
}

# Columnas priorizadas para tabla móvil
COLUMNAS_PRIORITARIAS = [
    "RANGO",
    "IPR",
    "MUNICIPIO",
    "DPTO",
    "CASOS_REALES",
    "PROY_2030",
    "CONFIABILIDAD",
]

COLUMNAS_SECUNDARIAS = [
    "DIVIPOLA",
    "CASOS_PRED",
    "RURAL",
    "INDIGENA",
]

# Configuración de columnas para st.dataframe
COLUMNAS_FORMATO = {
    "CASOS_REALES": {"label": "Casos reales", "format": "%.0f", "width": "small"},
    "CASOS_PRED": {"label": "Casos predichos", "format": "%.0f", "width": "small"},
    "PROY_2030": {"label": "Proyección 2030", "format": "%.0f", "width": "small"},
    "RURAL": {"label": "Rural (%)", "format": "%.1f%%", "width": "small"},
    "INDIGENA": {"label": "Indígena (%)", "format": "%.1f%%", "width": "small"},
    "IPR": {"label": "IPR", "format": "%.2f", "width": "small"},
    "RANGO": {"label": "Rango", "width": "small"},
    "CONFIABILIDAD": {"label": "Confiab.", "width": "small"},
    "MUNICIPIO": {"label": "Municipio", "width": "medium"},
    "DPTO": {"label": "Depto", "width": "small"},
    "DIVIPOLA": {"label": "DIVIPOLA", "width": "small"},
}

# Tab names y keys
TABS = [
    ("Mapa", "mapa"),
    ("Priorización municipal", "priorizacion"),
    ("Evolución mensual", "mensual"),
    ("Evolución semanal", "semanal"),
    ("Proyección 2026-2030", "proyeccion"),
    ("Modelos y calidad", "modelos"),
    ("Metodología y limitaciones", "metodologia"),
]

# Configuración de página
PAGE_CONFIG = {
    "page_title": "NUTRIPREDICT Colombia 2030",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}