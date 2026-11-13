"""
Paquete de páginas - NUTRIPREDICT Colombia 2030
"""

from app.pages.mapa import render_tab_mapa
from app.pages.priorizacion import render_tab_priorizacion
from app.pages.mensual import render_tab_mensual
from app.pages.semanal import render_tab_semanal
from app.pages.proyeccion import render_tab_proyeccion
from app.pages.modelos import render_tab_modelos
from app.pages.metodologia import render_tab_metodologia

__all__ = [
    "render_tab_mapa",
    "render_tab_priorizacion",
    "render_tab_mensual",
    "render_tab_semanal",
    "render_tab_proyeccion",
    "render_tab_modelos",
    "render_tab_metodologia",
]