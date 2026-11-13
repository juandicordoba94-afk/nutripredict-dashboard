"""
Paquete de páginas - NUTRIPREDICT Colombia 2030
"""

from app.views.mapa import render_tab_mapa
from app.views.priorizacion import render_tab_priorizacion
from app.views.mensual import render_tab_mensual
from app.views.semanal import render_tab_semanal
from app.views.proyeccion import render_tab_proyeccion
from app.views.modelos import render_tab_modelos
from app.views.metodologia import render_tab_metodologia

__all__ = [
    "render_tab_mapa",
    "render_tab_priorizacion",
    "render_tab_mensual",
    "render_tab_semanal",
    "render_tab_proyeccion",
    "render_tab_modelos",
    "render_tab_metodologia",
]
