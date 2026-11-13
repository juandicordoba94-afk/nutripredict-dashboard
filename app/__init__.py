"""
NUTRIPREDICT Colombia 2030 - Dashboard de priorización territorial
Paquete principal de la aplicación.
"""

from app.data_loader import inicializar_datos
from app.filters import init_filters, reset_filters
from app.components import load_css, tooltip, render_glosario

__all__ = [
    "inicializar_datos",
    "init_filters",
    "reset_filters",
    "load_css",
    "tooltip",
    "render_glosario",
]