"""
Módulo de mapas - NUTRIPREDICT Colombia 2030
Centraliza la creación de todos los mapas coropléticos.
"""

import copy
import math

import folium
import pandas as pd
import streamlit as st
from branca.colormap import LinearColormap
from folium.plugins import Fullscreen, Search
from streamlit_folium import st_folium

import plotly.express as px
from plotly.graph_objs import Figure


# ============================================================
# MAPAS COROPLÉTICOS
# ============================================================

def crear_mapa_departamental(
    df: pd.DataFrame,
    geo_dep: dict,
    color_col: str = "PROY_2030",
    title: str = "Escenario central 2030: total por departamento",
) -> Figure:
    """Crea mapa coroplético a nivel departamental."""
    fig = px.choropleth(
        df,
        geojson=geo_dep,
        locations="CODDPTO",
        featureidkey="properties.divipola_dep",
        color=color_col,
        hover_name="DPTO",
        hover_data=[color_col],
        color_continuous_scale="Greens",
        title=title,
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
    )

    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="Casos 2030",
            len=0.75,
            thickness=15,
            tickfont=dict(size=11),
        ),
    )

    return fig


def crear_mapa_municipal(
    df: pd.DataFrame,
    geo_mun: dict,
    color_col: str = "IPR",
    title: str = "Índice de Priorización Municipal (IPR)",
    height: int = 450,
) -> Figure:
    """Crea mapa coroplético a nivel municipal con range_color dinámico."""
    ipr_min = float(df[color_col].min())
    ipr_max = float(df[color_col].max())

    fig = px.choropleth(
        df,
        geojson=geo_mun,
        locations="DIVIPOLA",
        featureidkey="properties.divipola_mun",
        color=color_col,
        hover_name="MUNICIPIO",
        custom_data=["DPTO", "PROY_2030", "CASOS_PRED", "RANGO", "CONFIABILIDAD", "IPR", "RURAL", "INDIGENA"],
        color_continuous_scale="Greens",
        range_color=(ipr_min, ipr_max),
        title=title,
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Departamento: %{customdata[0]}<br>"
            "IPR: %{customdata[5]:.2f} (%{customdata[6]:.1f}% rural, %{customdata[7]:.1f}% indígena)<br>"
            "Proyección 2030: %{customdata[1]:.0f}<br>"
            "Casos predichos: %{customdata[2]:.0f}<br>"
            "Rango: %{customdata[3]}<br>"
            "Confiabilidad: %{customdata[4]}<extra></extra>"
        )
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
    )

    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="IPR",
            len=0.75,
            thickness=15,
            tickfont=dict(size=11),
        ),
    )

    return fig


def agregar_overlay_confiabilidad_baja(
    fig: Figure,
    df_vista: pd.DataFrame,
    geo_mun: dict,
) -> Figure:
    """
    Agrega un overlay con patrón para municipios CONFIABILIDAD = BAJA.
    Usa un segundo trace choropleth con opacidad y patrón visual.
    """
    codigos_baja = set(
        df_vista.loc[df_vista["CONFIABILIDAD"] == "BAJA", "DIVIPOLA"]
        .astype(str)
        .str.strip()
        .str.zfill(5)
    )

    if not codigos_baja:
        return fig

    # Crear dataframe solo con municipios BAJA
    df_baja = df_vista[
        df_vista["DIVIPOLA"].astype(str).str.strip().str.zfill(5).isin(codigos_baja)
    ].copy()

    if df_baja.empty:
        return fig

    # Agregar overlay translúcido usando colores RGBA
    fig.add_choropleth(
        geojson=geo_mun,
        locations=df_baja["DIVIPOLA"],
        featureidkey="properties.divipola_mun",
        z=[1] * len(df_baja),  # Valor constante
        colorscale=[[0, "rgba(201,76,76,0.15)"], [1, "rgba(201,76,76,0.25)"]],  # Rojo institucional translúcido
        zmin=0,
        zmax=1,
        showscale=False,
        hoverinfo="skip",
        name="Confiabilidad BAJA",
    )

    return fig


# ============================================================
# PREPARACIÓN DE DATOS PARA MAPAS
# ============================================================

def preparar_datos_mapa_departamental(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega datos municipales a nivel departamental para mapa."""
    return (
        df.groupby(["CODDPTO", "DPTO"], as_index=False)["PROY_2030"]
        .sum(min_count=1)
    )


def _normalizar_codigo(value, longitud: int) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().removesuffix(".0").zfill(longitud)


def _valor_serializable(value):
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _texto_o_sin_dato(value) -> str:
    return "Sin dato" if value is None or pd.isna(value) else str(value)


def _parsear_fechas_mensuales(serie: pd.Series) -> pd.Series:
    texto = serie.astype("string").str.strip()
    fecha = pd.to_datetime(texto, format="%Y%m", errors="coerce")
    pendientes = fecha.isna()
    if pendientes.any():
        fecha.loc[pendientes] = pd.to_datetime(texto.loc[pendientes], errors="coerce")
    return fecha


def _punto_en_anillo(lon: float, lat: float, anillo: list) -> bool:
    dentro = False
    anterior = anillo[-1] if anillo else None
    if anterior is None:
        return False
    for actual in anillo:
        x1, y1 = actual[:2]
        x2, y2 = anterior[:2]
        cruza = (y1 > lat) != (y2 > lat)
        if cruza and lon < (x2 - x1) * (lat - y1) / ((y2 - y1) or 1e-15) + x1:
            dentro = not dentro
        anterior = actual
    return dentro


def _punto_en_geometria(lon: float, lat: float, geometria: dict) -> bool:
    tipo = geometria.get("type")
    coordenadas = geometria.get("coordinates", [])
    poligonos = [coordenadas] if tipo == "Polygon" else coordenadas if tipo == "MultiPolygon" else []
    for poligono in poligonos:
        if poligono and _punto_en_anillo(lon, lat, poligono[0]):
            if not any(_punto_en_anillo(lon, lat, hueco) for hueco in poligono[1:]):
                return True
    return False


def _codigo_en_punto(features: list[dict], punto: dict | None) -> str | None:
    if not isinstance(punto, dict):
        return None
    try:
        lat, lon = float(punto["lat"]), float(punto["lng"])
    except (KeyError, TypeError, ValueError):
        return None
    for feature in features:
        if _punto_en_geometria(lon, lat, feature.get("geometry") or {}):
            return _normalizar_codigo(
                feature.get("properties", {}).get("divipola_mun"), 5
            )
    return None


def _limites_geograficos(features: list[dict]) -> list[list[float]] | None:
    coordenadas = []

    def recolectar(valor):
        if isinstance(valor, (list, tuple)) and len(valor) >= 2 and all(
            isinstance(item, (int, float)) for item in valor[:2]
        ):
            coordenadas.append(valor)
        elif isinstance(valor, (list, tuple)):
            for item in valor:
                recolectar(item)

    for feature in features:
        recolectar((feature.get("geometry") or {}).get("coordinates", []))
    if not coordenadas:
        return None
    return [
        [min(punto[1] for punto in coordenadas), min(punto[0] for punto in coordenadas)],
        [max(punto[1] for punto in coordenadas), max(punto[0] for punto in coordenadas)],
    ]


def _abrir_evolucion_mensual(departamento: str, municipio: str) -> None:
    st.session_state["seccion_dashboard"] = "Evolución mensual"
    st.session_state["mensual_departamento"] = departamento
    st.session_state["mensual_municipio"] = municipio


def _seleccionar_municipio_desde_widget() -> None:
    st.session_state["mapa_municipio_seleccionado"] = st.session_state.get(
        "mapa_municipio_selector"
    )


def _aplicar_fechas_panel(panel: pd.DataFrame) -> pd.DataFrame:
    datos = panel.copy()
    if "ANIOMESDT" not in datos:
        datos["_FECHA_MAPA"] = pd.NaT
    else:
        datos["_FECHA_MAPA"] = _parsear_fechas_mensuales(datos["ANIOMESDT"])
    return datos


def _crear_mapa_leaflet(
    geojson: dict,
    df_municipios: pd.DataFrame,
    indicador: str,
    seleccionado: str | None,
    departamento: str,
    resumen: bool = False,
) -> folium.Map:
    codigos_datos = set(df_municipios["DIVIPOLA"].dropna().astype(str))
    features = []
    for feature in geojson.get("features", []):
        codigo = _normalizar_codigo(
            feature.get("properties", {}).get("divipola_mun"), 5
        )
        if codigo in codigos_datos:
            copia = copy.deepcopy(feature)
            copia.setdefault("properties", {})["_codigo_municipio"] = codigo
            features.append(copia)

    propiedades = df_municipios.set_index("DIVIPOLA").to_dict("index")
    valores = []
    for feature in features:
        codigo = feature["properties"]["_codigo_municipio"]
        dato = propiedades.get(codigo, {})
        valor = dato.get(indicador)
        feature["properties"].update(
            {
                "_nombre": _texto_o_sin_dato(dato.get("MUNICIPIO")),
                "_departamento": _texto_o_sin_dato(dato.get("DPTO")),
                "_ipr": _valor_serializable(dato.get("IPR")),
                "_casos_periodo": _valor_serializable(dato.get("CASOS_PERIODO")),
                "_rural": _valor_serializable(dato.get("RURAL")),
                "_indigena": _valor_serializable(dato.get("INDIGENA")),
                "_confiabilidad": _texto_o_sin_dato(dato.get("CONFIABILIDAD")),
                "_rango": _texto_o_sin_dato(dato.get("RANGO")),
                "_valor_mapa": _valor_serializable(valor),
            }
        )
        if indicador != "CONFIABILIDAD" and pd.notna(valor):
            valores.append(float(valor))

    centro = [4.4, -74.3]
    mapa = folium.Map(
        location=centro,
        zoom_start=6 if departamento != "Todos" else 5,
        tiles="OpenStreetMap",
        control_scale=True,
        prefer_canvas=True,
        scrollWheelZoom=True,
        zoom_control=True,
    )
    mapa.fit_bounds([[-4.3, -81.9], [13.5, -66.8]])
    if not resumen:
        Fullscreen(
            position="bottomright",
            title="Pantalla completa",
            title_cancel="Salir de pantalla completa",
        ).add_to(mapa)

    if indicador == "CONFIABILIDAD":
        colores = {"ALTA": "#176B50", "MEDIA": "#E5B94B", "BAJA": "#C94C4C"}

        def estilo(feature):
            props = feature["properties"]
            nivel = str(props.get("_confiabilidad", "")).upper()
            seleccionado_actual = props.get("_codigo_municipio") == seleccionado
            return {
                "fillColor": colores.get(nivel, "#D9E2DC"),
                "color": "#103B2D" if seleccionado_actual else "#FFFFFF",
                "weight": 2.5 if seleccionado_actual else 0.5,
                "fillOpacity": 0.78,
            }

        legenda = "Confiabilidad de la información"
    else:
        minimo = min(valores) if valores else 0.0
        maximo = max(valores) if valores else 1.0
        if math.isclose(minimo, maximo):
            maximo = minimo + 1.0
        escala = (
            LinearColormap(
                colors=["#EAF3ED", "#8DBDA5", "#176B50", "#164C3B"],
                vmin=minimo,
                vmax=maximo,
                caption=("IPR (0–100)" if indicador == "IPR" else "Casos notificados"),
            )
            if valores
            else None
        )

        def estilo(feature):
            props = feature["properties"]
            value = props.get("_valor_mapa")
            seleccionado_actual = props.get("_codigo_municipio") == seleccionado
            try:
                color = escala(float(value)) if escala is not None and value is not None else "#E1E6E3"
            except (TypeError, ValueError):
                color = "#E1E6E3"
            return {
                "fillColor": color,
                "color": "#103B2D" if seleccionado_actual else "#FFFFFF",
                "weight": 2.5 if seleccionado_actual else 0.45,
                "fillOpacity": 0.82 if value is not None else 0.3,
            }

        if escala is not None:
            escala.add_to(mapa)
        legenda = escala.caption if escala is not None else "Sin valores en el período"

    capa = folium.FeatureGroup(name=legenda, show=True)
    geo_layer = folium.GeoJson(
        {"type": "FeatureCollection", "features": features},
        name="Municipios",
        style_function=estilo,
        highlight_function=lambda _: {"weight": 2.2, "color": "#164C3B", "fillOpacity": 0.92},
        tooltip=folium.GeoJsonTooltip(
            fields=["_nombre", "_departamento", "_ipr", "_casos_periodo", "_confiabilidad"],
            aliases=["Municipio", "Departamento", "IPR", "Casos del período", "Confiabilidad"],
            localize=True,
            sticky=False,
            max_width=320,
        ),
        popup=folium.GeoJsonPopup(
            fields=[
                "_nombre",
                "_departamento",
                "_ipr",
                "_casos_periodo",
                "_rural",
                "_indigena",
                "_confiabilidad",
                "_rango",
            ],
            aliases=[
                "Municipio",
                "Departamento",
                "IPR",
                "Casos del período",
                "% rural en notificaciones",
                "% indígena en notificaciones",
                "Confiabilidad",
                "Rango",
            ],
            localize=True,
        ),
    ).add_to(capa)
    capa.add_to(mapa)
    if not resumen:
        Search(
            layer=geo_layer,
            geom_type="Polygon",
            search_label="_nombre",
            placeholder="Buscar municipio",
            collapsed=False,
            search_zoom=9,
            position="topright",
        ).add_to(mapa)
    if indicador == "CONFIABILIDAD":
        folium.Element(
            '<div style="position:fixed;bottom:12px;left:12px;z-index:999;'
            'background:#fff;padding:7px 9px;border:1px solid #d9e2dc;border-radius:4px;'
            'font:12px sans-serif">'
            '<b>Confiabilidad</b><br>'
            '<span style="color:#176B50">●</span> Alta &nbsp; '
            '<span style="color:#E5B94B">●</span> Media &nbsp; '
            '<span style="color:#C94C4C">●</span> Baja &nbsp; '
            '<span style="color:#AAB5AF">●</span> Sin dato'
            '</div>'
        ).add_to(mapa.get_root().html)

    if seleccionado and seleccionado in propiedades:
        feature_seleccionado = next(
            (f for f in features if f["properties"].get("_codigo_municipio") == seleccionado),
            None,
        )
        if feature_seleccionado:
            coords = []

            def recolectar(valor):
                if isinstance(valor, (list, tuple)) and len(valor) >= 2 and all(
                    isinstance(item, (int, float)) for item in valor[:2]
                ):
                    coords.append(valor)
                elif isinstance(valor, (list, tuple)):
                    for item in valor:
                        recolectar(item)

            recolectar(feature_seleccionado.get("geometry", {}).get("coordinates", []))
            if coords:
                mapa.fit_bounds(
                    [[min(p[1] for p in coords), min(p[0] for p in coords)],
                     [max(p[1] for p in coords), max(p[0] for p in coords)]]
                )
    elif departamento != "Todos":
        codigos_departamento = {codigo[:2] for codigo in codigos_datos}
        departamento_features = [
            f for f in features
            if _normalizar_codigo(f["properties"].get("divipola_mun"), 5)[:2]
            in codigos_departamento
        ]
        coords = []

        def recolectar_departamento(valor):
            if isinstance(valor, (list, tuple)) and len(valor) >= 2 and all(
                isinstance(item, (int, float)) for item in valor[:2]
            ):
                coords.append(valor)
            elif isinstance(valor, (list, tuple)):
                for item in valor:
                    recolectar_departamento(item)

        for feature in departamento_features:
            recolectar_departamento(feature.get("geometry", {}).get("coordinates", []))
        if coords:
            mapa.fit_bounds(
                [[min(p[1] for p in coords), min(p[0] for p in coords)],
                 [max(p[1] for p in coords), max(p[0] for p in coords)]]
            )
    return mapa


def render_mapa_resumen(df: pd.DataFrame, geo_mun: dict) -> None:
    """Mapa compacto de IPR para la portada, sin la batería de exploración."""
    datos = df.copy()
    datos["DIVIPOLA"] = datos["DIVIPOLA"].map(lambda x: _normalizar_codigo(x, 5))
    codigos_geo = {
        _normalizar_codigo(f.get("properties", {}).get("divipola_mun"), 5)
        for f in geo_mun.get("features", [])
    }
    datos = datos.loc[datos["DIVIPOLA"].isin(codigos_geo)].copy()
    if datos.empty:
        st.info("No hay coincidencias entre estos resultados y las geometrías municipales.")
        return
    departamento = st.session_state.get("filtro_departamento", "Todos")
    mapa = _crear_mapa_leaflet(
        geo_mun,
        datos,
        "IPR",
        None,
        departamento,
        resumen=True,
    )
    st_folium(
        mapa,
        height=350,
        width=None,
        returned_objects=[],
        key="resumen_mapa_ipr_leaflet",
    )


def render_mapa_departamental(
    df: pd.DataFrame, geo_dep: dict, departamento: str
) -> None:
    """Muestra la proyección departamental sobre mapa base, sin alterar agregados."""
    datos = preparar_datos_mapa_departamental(df)
    datos["CODDPTO"] = datos["CODDPTO"].map(lambda x: _normalizar_codigo(x, 2))
    valores = datos.set_index("CODDPTO")["PROY_2030"].to_dict()
    nombres = datos.set_index("CODDPTO")["DPTO"].to_dict()
    features = []
    for feature in geo_dep.get("features", []):
        codigo = _normalizar_codigo(
            feature.get("properties", {}).get("divipola_dep"), 2
        )
        if codigo in valores:
            copia = copy.deepcopy(feature)
            valor = valores[codigo]
            copia.setdefault("properties", {}).update(
                {
                    "_codigo_departamento": codigo,
                    "_nombre_departamento": _texto_o_sin_dato(nombres.get(codigo)),
                    "_proyeccion_2030": _valor_serializable(valor),
                }
            )
            features.append(copia)

    datos_disponibles = [float(valor) for valor in valores.values() if pd.notna(valor)]
    if not features:
        st.warning("Los departamentos no coinciden con los códigos del GeoJSON.")
        return
    minimo = min(datos_disponibles) if datos_disponibles else 0.0
    maximo = max(datos_disponibles) if datos_disponibles else 1.0
    if math.isclose(minimo, maximo):
        maximo = minimo + 1.0
    escala = (
        LinearColormap(
            ["#EAF3ED", "#8DBDA5", "#176B50", "#164C3B"],
            vmin=minimo,
            vmax=maximo,
            caption="Casos proyectados · escenario central 2030",
        )
        if datos_disponibles
        else None
    )
    mapa = folium.Map(
        location=[4.4, -74.3],
        zoom_start=6 if departamento != "Todos" else 5,
        tiles="OpenStreetMap",
        control_scale=True,
        scrollWheelZoom=True,
    )
    Fullscreen(
        position="bottomright",
        title="Pantalla completa",
        title_cancel="Salir de pantalla completa",
    ).add_to(mapa)

    def estilo(feature):
        valor = feature["properties"].get("_proyeccion_2030")
        try:
            color = escala(float(valor)) if escala is not None and valor is not None else "#E1E6E3"
        except (TypeError, ValueError):
            color = "#E1E6E3"
        return {"fillColor": color, "color": "#FFFFFF", "weight": 1, "fillOpacity": 0.82 if valor is not None else 0.3}

    folium.GeoJson(
        {"type": "FeatureCollection", "features": features},
        name="Proyección 2030",
        style_function=estilo,
        highlight_function=lambda _: {"weight": 2.3, "color": "#164C3B", "fillOpacity": 0.92},
        tooltip=folium.GeoJsonTooltip(
            fields=["_nombre_departamento", "_proyeccion_2030"],
            aliases=["Departamento", "Casos proyectados en 2030"],
            localize=True,
        ),
        popup=folium.GeoJsonPopup(
            fields=["_nombre_departamento", "_proyeccion_2030"],
            aliases=["Departamento", "Escenario central 2030"],
            localize=True,
        ),
    ).add_to(mapa)
    if escala:
        escala.add_to(mapa)
    bounds = _limites_geograficos(features)
    if bounds:
        mapa.fit_bounds(bounds)
    st_folium(
        mapa,
        height=570,
        width=None,
        returned_objects=[],
        key="exploracion_departamental_leaflet",
    )


def render_exploracion_territorial(
    df: pd.DataFrame,
    geo_mun: dict,
    panel_mensual: pd.DataFrame,
) -> None:
    """Mapa Leaflet con capas, búsqueda y ficha vinculada al municipio seleccionado."""
    departamento = st.session_state.get("filtro_departamento", "Todos")
    datos = df.copy()
    datos["DIVIPOLA"] = datos["DIVIPOLA"].map(lambda x: _normalizar_codigo(x, 5))
    if departamento != "Todos":
        datos = datos.loc[datos["DPTO"] == departamento].copy()
    if datos.empty:
        st.info("No hay municipios para los filtros seleccionados.")
        return

    indicador_label = st.selectbox(
        "Capa temática",
        ["IPR", "Casos notificados", "Confiabilidad"],
        key="mapa_capa_temática",
    )
    indicador = {"IPR": "IPR", "Casos notificados": "CASOS_PERIODO", "Confiabilidad": "CONFIABILIDAD"}[indicador_label]

    panel = _aplicar_fechas_panel(panel_mensual)
    panel["DIVIPOLARESIDENCIA"] = panel["DIVIPOLARESIDENCIA"].map(lambda x: _normalizar_codigo(x, 5))
    fechas = panel["_FECHA_MAPA"].dropna()
    if not fechas.empty:
        minimo, maximo = fechas.min().date(), fechas.max().date()
        if minimo < maximo:
            periodo = st.slider(
                "Período de casos notificados",
                min_value=minimo,
                max_value=maximo,
                value=(minimo, maximo),
                format="MM/YYYY",
                key="mapa_periodo_casos",
            )
        else:
            periodo = (minimo, maximo)
            st.caption(f"Período disponible: {minimo:%m/%Y}")
        panel_periodo = panel.loc[
            panel["_FECHA_MAPA"].between(pd.Timestamp(periodo[0]), pd.Timestamp(periodo[1]) + pd.offsets.MonthEnd(0))
        ]
        casos = panel_periodo.groupby("DIVIPOLARESIDENCIA", as_index=True)["CASOS"].sum(min_count=1)
        datos["CASOS_PERIODO"] = datos["DIVIPOLA"].map(casos)
    else:
        st.info("No hay fechas válidas en ANIOMESDT para filtrar el panel mensual.")
        datos["CASOS_PERIODO"] = float("nan")

    codigos_geometria = {
        _normalizar_codigo(f.get("properties", {}).get("divipola_mun"), 5)
        for f in geo_mun.get("features", [])
    }
    datos_con_geo = datos.loc[datos["DIVIPOLA"].isin(codigos_geometria)].copy()
    if datos_con_geo.empty:
        st.warning("Los resultados no coinciden con los códigos DIVIPOLA del GeoJSON.")
        return
    codigos_sin_geo = set(datos["DIVIPOLA"]) - codigos_geometria
    if codigos_sin_geo:
        st.warning(f"{len(codigos_sin_geo)} municipio(s) con resultados no tienen geometría y no se dibujan.")
    if indicador == "CASOS_PERIODO" and datos_con_geo["CASOS_PERIODO"].notna().sum() == 0:
        st.info("No hay casos disponibles para el período elegido; las geometrías sin datos permanecen neutrales.")

    codigos = datos_con_geo.set_index("DIVIPOLA")["MUNICIPIO"].to_dict()
    opciones = [None] + sorted(codigos, key=lambda c: str(codigos[c]).casefold())
    seleccionado = st.session_state.get("mapa_municipio_seleccionado")
    if seleccionado not in set(datos_con_geo["DIVIPOLA"]):
        seleccionado = None
        st.session_state["mapa_municipio_seleccionado"] = None
    if st.session_state.get("mapa_municipio_selector") != seleccionado:
        st.session_state["mapa_municipio_selector"] = seleccionado
    st.selectbox(
        "Buscar o seleccionar municipio",
        opciones,
        format_func=lambda codigo: (
            "Selecciona un municipio"
            if codigo is None
            else f"{codigos.get(codigo, 'Municipio')} · {codigo}"
        ),
        key="mapa_municipio_selector",
        on_change=_seleccionar_municipio_desde_widget,
    )
    seleccionado = st.session_state.get("mapa_municipio_seleccionado")

    mapa = _crear_mapa_leaflet(
        geo_mun, datos_con_geo, indicador, seleccionado, departamento
    )
    eventos = st_folium(
        mapa,
        height=570,
        width=None,
        returned_objects=["last_clicked", "last_object_clicked", "last_object_clicked_count"],
        key="exploracion_municipal_leaflet",
    )

    # Al hacer clic sobre una geometría, Leaflet devuelve las coordenadas del clic.
    # Se asigna la selección mediante point-in-polygon en el GeoJSON local.
    if isinstance(eventos, dict):
        count = eventos.get("last_object_clicked_count")
        last_count = st.session_state.get("_mapa_ultimo_click_count")
        if count is not None and count != last_count:
            st.session_state["_mapa_ultimo_click_count"] = count
            punto = eventos.get("last_object_clicked") or eventos.get("last_clicked")
            codigos_visibles = set(datos_con_geo["DIVIPOLA"])
            codigo_click = _codigo_en_punto(
                [
                    feature
                    for feature in geo_mun.get("features", [])
                    if _normalizar_codigo(
                        feature.get("properties", {}).get("divipola_mun"), 5
                    )
                    in codigos_visibles
                ],
                punto,
            )
            if codigo_click and codigo_click != st.session_state.get("mapa_municipio_seleccionado"):
                st.session_state["mapa_municipio_seleccionado"] = codigo_click
                st.rerun()

    seleccionado = st.session_state.get("mapa_municipio_seleccionado")
    if seleccionado:
        fila = datos_con_geo.loc[datos_con_geo["DIVIPOLA"] == seleccionado]
        if fila.empty:
            st.info("El municipio seleccionado no tiene datos en los resultados actuales.")
            return
        registro = fila.iloc[0]
        nombre = str(registro.get("MUNICIPIO", "Municipio"))
        depto = str(registro.get("DPTO", "Departamento"))
        posicion_ipr = (
            datos_con_geo["IPR"].rank(method="min", ascending=False).loc[fila.index[0]]
            if "IPR" in datos_con_geo and pd.notna(registro.get("IPR"))
            else None
        )
        mensual = panel.loc[panel["DIVIPOLARESIDENCIA"] == seleccionado].copy()
        mensual = mensual.dropna(subset=["_FECHA_MAPA"])
        dept_code = seleccionado[:2]
        mensual_depto = panel.loc[
            panel["DIVIPOLARESIDENCIA"].astype("string").str[:2] == dept_code
        ].dropna(subset=["_FECHA_MAPA"])
        serie_municipio = (
            mensual.groupby("_FECHA_MAPA", as_index=False)["CASOS"]
            .sum(min_count=1)
            .rename(columns={"CASOS": "Municipio seleccionado"})
        )
        serie_departamento = (
            mensual_depto.groupby("_FECHA_MAPA", as_index=False)["CASOS"]
            .sum(min_count=1)
            .rename(columns={"CASOS": "Departamento"})
        )
        evolucion = (
            serie_municipio.merge(serie_departamento, on="_FECHA_MAPA", how="outer")
            .rename(columns={"_FECHA_MAPA": "Mes"})
            .sort_values("Mes")
        )

        st.markdown(f"### {nombre}, {depto}")
        col1, col2 = st.columns(2)
        casos_municipio = registro.get("CASOS_PERIODO")
        col1.metric(
            "Casos notificados",
            f"{casos_municipio:,.0f}" if pd.notna(casos_municipio) else "Sin dato",
        )
        col2.metric("IPR", f"{registro.get('IPR'):.1f}" if pd.notna(registro.get("IPR")) else "Sin dato")
        col1, col2 = st.columns(2)
        col1.metric("Posición IPR en la vista", f"#{posicion_ipr:.0f}" if pd.notna(posicion_ipr) else "Sin dato")
        col2.metric("Confiabilidad", _texto_o_sin_dato(registro.get("CONFIABILIDAD")))
        st.metric("Rango", _texto_o_sin_dato(registro.get("RANGO")))
        composicion = [
            (etiqueta, registro.get(columna))
            for etiqueta, columna in [("Rural", "RURAL"), ("Indígena", "INDIGENA")]
            if pd.notna(registro.get(columna))
        ]
        if composicion:
            st.caption(
                "Composición de los casos notificados: "
                + " · ".join(f"{etiqueta}: {valor:.1f}%" for etiqueta, valor in composicion)
                + ". No representa la composición total de la población municipal."
            )
        with st.expander("Evolución mensual y comparación con el departamento", expanded=True):
            if evolucion.empty:
                st.info("No hay historia mensual suficiente para este municipio.")
            else:
                st.line_chart(
                    evolucion,
                    x="Mes",
                    y=["Municipio seleccionado", "Departamento"],
                    x_label="Mes",
                    y_label="Casos notificados",
                    height=300,
                    alt=f"Casos mensuales de {nombre} comparados con {depto}",
                )
        municipio_panel = mensual.loc[
            mensual["DIVIPOLARESIDENCIA"] == seleccionado
        ]
        if not municipio_panel.empty:
            fila_panel = municipio_panel.iloc[0]
            depto_panel = fila_panel.get("Departamentoresidencia")
            municipio_panel_nombre = fila_panel.get("Municipioresidencia")
            if pd.notna(depto_panel) and pd.notna(municipio_panel_nombre):
                st.button(
                    "Abrir análisis mensual de este municipio",
                    icon=":material/open_in_new:",
                    key="mapa_abrir_analisis_mensual",
                    on_click=_abrir_evolucion_mensual,
                    args=(str(depto_panel), str(municipio_panel_nombre)),
                )
        st.caption(
            "El IPR es relativo y no representa riesgo individual. La serie departamental "
            "suma las notificaciones municipales e incluye al municipio seleccionado."
        )
    else:
        st.info("Busca o selecciona un municipio en el mapa para consultar su ficha e historia mensual.")
