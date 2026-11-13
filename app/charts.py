"""
Módulo de gráficas - NUTRIPREDICT Colombia 2030
Centraliza la creación de todas las gráficas Plotly.
"""

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure

from app.constants import COLORES_ESCENARIOS


# ============================================================
# GRÁFICAS DE SERIES TEMPORALES
# ============================================================

def crear_linea_mensual(
    df: pd.DataFrame,
    municipio: str,
    departamento: str,
) -> Figure:
    """Crea gráfica de línea mensual con marcadores y hovertemplate táctil."""
    fig = px.line(
        df,
        x="ANIOMESDT",
        y="CASOS",
        title=f"Casos notificados por mes: {municipio}, {departamento}",
        labels={"ANIOMESDT": "Mes", "CASOS": "Casos notificados"},
    )

    fig.update_traces(
        mode="lines+markers",
        line=dict(width=2, color="#176B50"),
        marker=dict(size=8, color="#176B50"),
        hovertemplate="Mes: %{x|%b %Y}<br>Casos: %{y:.0f}<extra></extra>",
    )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode="x unified",
        xaxis=dict(
            tickfont=dict(size=11),
            tickangle=-45,
            nticks=10,
        ),
        yaxis=dict(tickfont=dict(size=11)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
    )

    return fig


def crear_linea_semanal(
    df: pd.DataFrame,
    municipio: str,
    departamento: str,
) -> Figure:
    """Crea gráfica de línea semanal con marcadores y hovertemplate táctil."""
    fig = px.line(
        df,
        x="SEMANAINI",
        y="CASOS",
        title=f"Casos notificados por semana: {municipio}, {departamento}",
        labels={"SEMANAINI": "Semana epidemiológica (inicio)", "CASOS": "Casos notificados"},
    )

    fig.update_traces(
        mode="lines+markers",
        line=dict(width=2, color="#176B50"),
        marker=dict(size=7, color="#176B50"),
        hovertemplate="Semana: %{x|%d/%m/%Y}<br>Casos: %{y:.0f}<extra></extra>",
    )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode="x unified",
        xaxis=dict(
            tickfont=dict(size=11),
            tickangle=-45,
            nticks=10,
        ),
        yaxis=dict(tickfont=dict(size=11)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
    )

    return fig


def crear_proyeccion_nacional(
    df: pd.DataFrame,
    show_ic80: bool = True,
) -> Figure:
    """Crea gráfica de proyección nacional con escenarios e IC80."""
    fig = px.line(
        df,
        x="ANIO",
        y="PROYECCION",
        color="ESCENARIO",
        markers=True,
        title="Proyección nacional de casos notificados, 2026–2030",
        labels={
            "ANIO": "Año",
            "PROYECCION": "Casos notificados esperados",
            "ESCENARIO": "Escenario",
        },
        color_discrete_map=COLORES_ESCENARIOS,
    )

    if show_ic80 and {"IC80BAJO", "IC80ALTO"}.issubset(df.columns):
        central = df[df["ESCENARIO"] == "CENTRAL"].sort_values("ANIO")
        if not central.empty:
            fig.add_scatter(
                x=central["ANIO"],
                y=central["IC80ALTO"],
                mode="lines",
                name="Intervalo 80% superior",
                line=dict(width=1, dash="dash", color="#176B50"),
                showlegend=True,
            )
            fig.add_scatter(
                x=central["ANIO"],
                y=central["IC80BAJO"],
                mode="lines",
                name="Intervalo 80% inferior",
                line=dict(width=1, dash="dash", color="#176B50"),
                fill="tonexty",
                fillcolor="rgba(23,107,80,0.12)",
                showlegend=True,
            )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode="x unified",
        xaxis=dict(tickfont=dict(size=11), tickangle=0, dtick=1),
        yaxis=dict(tickfont=dict(size=11)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
    )

    return fig


def crear_proyeccion_departamental(
    df: pd.DataFrame,
    departamento: str,
    show_ic80: bool = True,
) -> Figure:
    """Crea gráfica de proyección departamental con escenarios e IC80."""
    fig = px.line(
        df,
        x="ANIO",
        y="PROYECCION",
        color="ESCENARIO",
        markers=True,
        title=f"Proyección departamental: {departamento}, 2026–2030",
        labels={
            "ANIO": "Año",
            "PROYECCION": "Casos notificados esperados",
            "ESCENARIO": "Escenario",
        },
        color_discrete_map=COLORES_ESCENARIOS,
    )

    if show_ic80 and {"IC80BAJO", "IC80ALTO"}.issubset(df.columns):
        central = df[df["ESCENARIO"] == "CENTRAL"].sort_values("ANIO")
        if not central.empty:
            fig.add_scatter(
                x=central["ANIO"],
                y=central["IC80ALTO"],
                mode="lines",
                name="Intervalo 80% superior",
                line=dict(width=1, dash="dash", color="#176B50"),
                showlegend=True,
            )
            fig.add_scatter(
                x=central["ANIO"],
                y=central["IC80BAJO"],
                mode="lines",
                name="Intervalo 80% inferior",
                line=dict(width=1, dash="dash", color="#176B50"),
                fill="tonexty",
                fillcolor="rgba(23,107,80,0.12)",
                showlegend=True,
            )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode="x unified",
        xaxis=dict(tickfont=dict(size=11), tickangle=0, dtick=1),
        yaxis=dict(tickfont=dict(size=11)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
    )

    return fig


def crear_proyeccion_municipal(
    df: pd.DataFrame,
    municipio: str,
    departamento: str,
) -> Figure:
    """Crea gráfica de proyección municipal con escenarios."""
    fig = px.line(
        df,
        x="ANIO",
        y="PROYECCION",
        color="ESCENARIO",
        markers=True,
        title=f"Proyección municipal: {municipio}, {departamento}",
        labels={
            "ANIO": "Año",
            "PROYECCION": "Casos notificados esperados",
            "ESCENARIO": "Escenario",
        },
        color_discrete_map=COLORES_ESCENARIOS,
    )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode="x unified",
        xaxis=dict(tickfont=dict(size=11), tickangle=0, dtick=1),
        yaxis=dict(tickfont=dict(size=11)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
    )

    return fig


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def tabla_escenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte formato largo a ancho para mostrar escenarios como columnas."""
    columnas_id = [
        c for c in df.columns
        if c not in {"ESCENARIO", "PROYECCION", "IC80BAJO", "IC80ALTO"}
    ]
    tabla = (
        df.pivot(
            index=columnas_id,
            columns="ESCENARIO",
            values="PROYECCION",
        )
        .reset_index()
    )
    tabla.columns.name = None
    escenarios = ["BAJO", "CENTRAL", "ALTO"]
    columnas = columnas_id + [e for e in escenarios if e in tabla.columns]
    return tabla[columnas]


FORMATO_ESCENARIOS = {
    "BAJO": {"format": "%.0f"},
    "CENTRAL": {"format": "%.0f"},
    "ALTO": {"format": "%.0f"},
}