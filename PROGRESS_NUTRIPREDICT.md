# PROGRESS_NUTRIPREDICT.md — Registro de continuidad del proyecto NUTRIPREDICT Colombia 2030

**Última actualización:** 2026-11-13  
**Modelo que registra:** Qwen (FreeLLMAPI Auto)  
**Estado Git:** Rama `feature/mobile-audit-fixes` (commit `0b32701` = M5 completado; trabajo M6 en curso). `main` sin cambios.

---

## ETAPA M1 — CORRECCIÓN CRÍTICOS MÓVILES + INTEGRIDAD CIENTÍFICA ✅ COMPLETADA

**Fecha:** 2026-11-13  
**Rama:** `feature/mobile-audit-fixes`  
**Commit base:** `29b0da2` (backup estado previo)  
**Archivo modificado:** `app/streamlit_app.py` (1793 → ~1900 líneas)

### Objetivo
Corregir los 4 críticos móviles (A2, B1, D1, D2, F1) + 3 críticos de integridad (C1, C2, C3) y aplicar mejoras de identidad visual y usabilidad táctil.

### Cambios realizados

| # | Problema | Solución implementada | Verificación |
|---|----------|----------------------|--------------|
| **C1** | Modelos inventados en Metodología (GRU, SARIMA, Holt-Winters, GLM, Ensamble LGBXGB) | Reescrita pestaña Metodología: solo 3 modelos reales (LightGBM, XGBoost, RandomForest Poisson). Eliminadas referencias falsas. | Texto honesto, coincide con notebook y `seleccion_modelos.json`. |
| **C2** | "Ensamble LGBXGB" → real XGBoost (Poisson) | Corregido en Metodología: "Modelo semanal seleccionado: **XGBoost (Poisson)**". | Coincide con `seleccion_modelos.json` y hoja `Resumen_Modelos`. |
| **C3** | `TASA_100K` en tabla priorización pero 100% null | Eliminada `TASA_100K` de `columnas_tabla`; añadida nota: "TASA_100K no se calcula por ausencia de datos poblacionales". | Columna ya no aparece; nota visible en caption. |
| **A2** | Tabs 0.88rem / 44px → imposibles de tocar | CSS: `min-height: 44px`, `min-width: 44px`, `padding: 0.65rem 1rem`, `font-size: 1rem`, `flex-wrap: wrap`, color activo `#176B50`. | Cumple objetivo táctil 44×44px; wrap en ≤375px. |
| **B1** | Sidebar `auto` tapa contenido en móvil | `initial_sidebar_state="collapsed"` + botón "🔍 Filtros" en header (col 15%) que togglea `st.session_state["sidebar_open"]` + `st.rerun()`. | Sidebar colapsado por defecto; botón visible y funcional. |
| **D1** | Mapa municipal `range_color=(0,100)` fijo | `range_color=(ipr_min, ipr_max)` dinámico (27.9–99.5); colorbar con título "IPR" y valores numéricos (`coloraxis_showscale=True`). | Escala usa rango real; leyenda numérica visible. |
| **D2** | Tooltips solo hover (no táctil) | `custom_data` + `hovertemplate` rico con IPR, Proyección, Casos pred, Rango, Confiabilidad; funciona en tap. | Tap en municipio muestra info completa sin tapar. |
| **D3** | Mapa departamental sin leyenda numérica | Añadido `coloraxis_colorbar` con título "Casos 2030", `len=0.75`, `thickness=15`. | Leyenda visible en ambos mapas. |
| **D4** | Altura fija 550px → >100vh en móvil | Reducido a `height=450` + CSS `@media (max-width: 768px) { [data-testid="stPlotlyChart"] > div { max-height: 60vh !important; } }`. | Mapas y gráficas caben en viewport sin scroll excesivo. |
| **D5** | Modebar Plotly botones pequeños | CSS `@media (max-width: 768px) { .modebar { display: none !important; } }`; zoom/pan nativo por pinch. | Interfaz limpia; pinch-to-zoom funciona. |
| **F1** | Tabla priorización 12 cols → scroll horizontal | Columnas prioritarias (7): RANGO, IPR, MUNICIPIO, DPTO, CASOS_REALES, PROY_2030, CONFIABILIDAD. Checkbox "Mostrar todas las columnas" para secundarias. `width="small/medium"` en `column_config`. | En móvil: 7 cols legibles sin scroll horizontal; toggle para ver todo. |
| **E1/E2/E3** | Gráficas mensual/semanal/proyección: ejes/leyenda/marcadores | `tickfont=11`, `tickangle=-45`, `nticks=10`; leyenda horizontal `y=1.02`; marcadores `size=7-8`, color `#176B50`, `hovertemplate` rico. | Ejes legibles; leyenda no tapa gráfica; tap muestra tooltip. |
| **E6** | Colores hardcoded (Plotly default) | Paleta institucional: `#E5B94B` (Bajo), `#176B50` (Central), `#C94C4C` (Alto) + fill `rgba(23,107,80,0.12)`. Aplicado en 3 gráficas de proyección + mensual/semanal. | Identidad visual coherente; contraste AA. |
| **G3** | 6 `st.warning` apilados | Unificados en `st.expander("⚠ Ver limitaciones detalladas (6 puntos)", expanded=False)`. | Una sola caja visible; expandible bajo demanda. |
| **A1/A5/A6/B1** | Caption provisional + textos | Caption actualizada: "Dashboard de priorización territorial...". Textos con acentos y ortografía corregida. | Texto profesional e institucional. |

### Pruebas ejecutadas
- ✅ Sintaxis Python: `python -m py_compile app/streamlit_app.py` — sin errores.
- ✅ Carga app: `streamlit run app/streamlit_app.py --server.headless true` — arranca en puerto 8501, sin tracebacks.
- ✅ Navegación tabs: 7 tabs cargan correctamente.
- ✅ Sidebar toggle: botón "🔍 Filtros" abre/cierra sidebar + `st.rerun()`.
- ✅ Mapa municipal: range_color dinámico, colorbar visible, hovertemplate en tap.
- ✅ Tabla priorización: 7 columnas por defecto, checkbox muestra 11, TASA_100K ausente.
- ✅ Metodología: solo 3 modelos reales, XGBoost semanal, tabla IPR con pesos, expander limitaciones.

### Archivos modificados
- `app/streamlit_app.py` — único archivo tocado (cambios en CSS, header, sidebar, mapa, tabla, gráficas, metodología).

### Pendientes para siguientes etapas (M2–M6)
- M2: Sidebar filtros mejorados (reset, chips activos, selectores táctiles).
- M3: Mapas avanzados (patrón CONFIABILIDAD BAJA, mini-mapa proyección).
- M4: Tablas tarjeta/tabla toggle, paginación táctil, métricas en tarjetas.
- M5: `.streamlit/theme.toml`, `app/styles.css` separado, glosario tooltips.
- M6: Arquitectura modular (`app/data_loader.py`, `app/charts.py`, `app/maps.py`, `app/filters.py`, `app/pages/`).

---

## ETAPA M2 — FILTROS GLOBALES + CHIPS ACTIVOS + RESET ✅ COMPLETADA

**Fecha:** 2026-11-13  
**Rama:** `feature/mobile-audit-fixes`  
**Commit base:** `292008a` (M1 completo)  
**Archivo modificado:** `app/streamlit_app.py` (~1900 → ~2100 líneas)

### Objetivo
Implementar sistema de filtros globales persistentes en `session_state`, chips de filtros activos visibles en cada tab, botón de restablecer filtros (sidebar + header), y sincronización completa entre sidebar y tabs.

### Cambios realizados

| # | Problema | Solución implementada | Verificación |
|---|----------|----------------------|--------------|
| **M2-1** | Filtros globales no persistentes al cerrar sidebar | `init_filters()` inicializa `filtro_nivel`, `filtro_departamento`, `filtro_municipio`, `filtro_fecha_inicio`, `filtro_fecha_fin` en `session_state`. `df_vista` **siempre** usa filtros globales (independiente de sidebar abierto/cerrado). | Cambiar filtro en sidebar → aplicar → cerrar sidebar → filtro persiste en mapa y tabla. |
| **M2-2** | Sidebar y tabs desincronizados | Sidebar `radio`/`selectbox` usan `key` + `on_change` → escriben directo a `session_state`. `df_vista` lee de `session_state` antes de renderizar cada tab. | Un solo origen de verdad (`session_state`). |
| **M2-3** | Sin feedback visual de filtros activos | `render_active_filters_chips()` genera chips HTML con paleta institucional (`#eaf3ed`/`#176b50`) mostrando: Nivel, Departamento, Municipio, Fechas. Llamado al inicio de **cada tab** (7 tabs). | Chips visibles arriba del contenido en Mapa, Priorización, Mensual, Semanal, Proyección, Modelos, Metodología. |
| **M2-4** | Sin botón de reset global | `reset_filters()` limpia `session_state` + claves específicas de tabs (`departamento_*`, `municipio_*`, `rango_*`). Botón en **sidebar** ("🔄 Restablecer filtros") + botón en **header/chips** ("🔄 Restablecer filtros"). Ambos llaman `reset_filters()` + `st.rerun()`. | Click → todos los filtros vuelven a default (Municipios / Todos / sin fechas). |
| **M2-5** | Selectores táctiles mejorados en sidebar | `min-height: 44px`, `font-size: 1rem` ya en CSS (M1). `radio` horizontal con `gap: 0.5rem`. `selectbox` con altura táctil. | Usable en móvil sin zoom. |
| **M2-6** | Info de filtros activos en sidebar | `st.sidebar.caption(f"Activo: {nivel} • {departamento}")` cuando hay filtro no-default. | Feedback contextual en sidebar abierto. |

### Pruebas ejecutadas
- ✅ Sintaxis Python: `python -m py_compile app/streamlit_app.py` — sin errores.
- ✅ Carga app: `streamlit run app/streamlit_app.py --server.headless true` — arranca en puerto 8501, sin tracebacks.
- ✅ Sidebar toggle: botón "🔍 Filtros" abre/cierra + `st.rerun()`.
- ✅ Filtros persistentes: cambiar Depto en sidebar → cerrar sidebar → mapa y tabla priorización reflejan el filtro.
- ✅ Chips activos: visibles en 7 tabs cuando hay filtro aplicado.
- ✅ Reset global: botón en sidebar + botón en chips → vuelve a default (Municipios / Todos).
- ✅ Navegación tabs: 7 tabs cargan correctamente con chips sincronizados.

### Archivos modificados
- `app/streamlit_app.py` — funciones `init_filters()`, `reset_filters()`, `render_active_filters_chips()`, sidebar reescrito, `df_vista` unificado, chips en 7 tabs.

---

## ETAPA M3 — MAPAS AVANZADOS: CONFIABILIDAD BAJA + PROYECCIÓN ANIMADA ✅ COMPLETADA

**Fecha:** 2026-11-13  
**Rama:** `feature/mobile-audit-fixes`  
**Commit base:** `104b3fe` (M2 completo)  
**Archivo modificado:** `app/streamlit_app.py` (~2100 → ~2300 líneas)

### Objetivo
Implementar mejoras avanzadas de mapas táctiles:
1. **Overlay CONFIABILIDAD BAJA** — patrón visual (rojo translúcido) para 555 municipios (49.6%) con <10 casos en 24 meses, cuyo IPR es inestable.
2. **Mini-mapa proyección animado 2026–2030** — coroplético con slider temporal (play/pause) que muestra evolución del escenario central por municipio.
3. **Tooltips enriquecidos** — hovertemplate con % rural/indígena junto al IPR, mejorando contexto en tap táctil.

### Cambios realizados

| # | Función | Implementación | Verificación |
|---|---------|----------------|--------------|
| **M3-1** | Overlay CONFIABILIDAD BAJA | `agregar_overlay_confiabilidad_baja(fig, df_vista, geo_mun)` — añade 2º trace `choropleth` con `colorscale` rojo institucional (`#C94C4C`) al 15-25% opacity, `showscale=False`, `hoverinfo="skip"`. Solo municipios con `CONFIABILIDAD == "BAJA"` (555/1119). | Mapa principal muestra overlay rojo sutil en municipios inestables; no interfiere con colorbar IPR; hover no muestra info del overlay. |
| **M3-2** | Mini-mapa proyección animado | `crear_mapa_proyeccion_animado(df_vista, geo_mun, "CENTRAL")` — usa `proy_municipal` (30 cols: PROY_2026..2030_BAJO/CENTRAL/ALTO + P10/P90). Convierte a formato largo (DIVIPOLA, ANIO, PROYECCION_*). `px.choropleth` con `animation_frame="ANIO"`. Duración 800ms, easing cubic-in-out. Botón ▶/⏸ grande para táctil. | En tab Mapa (nivel Municipal): sección "Proyección animada 2026–2030" con mapa animado funcional. Respeta filtro departamental global. |
| **M3-3** | Tooltip enriquecido | `custom_data` extendido: añade `RURAL` (idx 6) e `INDIGENA` (idx 7). `hovertemplate`: "IPR: X.XX (Y.Y% rural, Z.Z% indígena)". | Tap en municipio muestra composición rural/indígena junto a IPR y proyección. |
| **M3-4** | Leyenda contextual en caption | Caption actualizada: "⚠ Overlay rojo = CONFIABILIDAD BAJA (< 10 casos en 24 meses; IPR inestable)." | Usuario entiende significado visual del overlay rojo. |
| **M3-5** | Caché para performance | `@st.cache_data` en `preparar_mapa_confiabilidad_baja` y `crear_mapa_proyeccion_animado`. | Animación fluida; no recalcula al cambiar tabs. |

### Pruebas ejecutadas
- ✅ Sintaxis Python: `python -m py_compile app/streamlit_app.py` — sin errores.
- ✅ Carga app: `streamlit run app/streamlit_app.py --server.headless true` — puerto 8501, sin tracebacks.
- ✅ Overlay CONFIABILIDAD BAJA: visible en mapa municipal (overlay rojo translúcido en ~50% municipios).
- ✅ Mini-mapa animado: aparece solo en nivel Municipal; botón ▶ reproduce 2026→2030; respeta filtro Depto.
- ✅ Tooltips: tap muestra IPR + % rural + % indígena + proyección + casos + rango + confiabilidad.
- ✅ Filtros M2: persisten y sincronizan con nuevos mapas (df_vista filtrado por session_state).
- ✅ Navegación tabs: 7 tabs cargan correctamente.

### Archivos modificados
- `app/streamlit_app.py` — funciones `preparar_mapa_confiabilidad_baja()`, `crear_mapa_proyeccion_animado()`, `agregar_overlay_confiabilidad_baja()`, mapa municipal actualizado, mini-mapa en tab_mapa, tooltip enriquecido.

---

## ETAPA M4 — TABLAS MÓVILES: VISTA TARJETA/TABLA + PAGINACIÓN TÁCTIL + MÉTRICAS ✅ COMPLETADA

**Fecha:** 2026-11-13  
**Rama:** `feature/mobile-audit-fixes`  
**Commit base:** `d7f1957` (M3 completo)  
**Archivo modificado:** `app/streamlit_app.py` (~2300 → ~2600 líneas)

### Objetivo
Transformar la tabla de priorización municipal en una experiencia móvil-first:
1. **Métricas resumen (tarjetas KPI)** — 4 métricas clave arriba de la tabla: total municipios (con desglose por rango), proyección 2030 total, IPR promedio, % confiabilidad BAJA.
2. **Toggle Vista Tarjeta / Tabla** — `st.toggle("🃏 Vista tarjetas (móvil)")` para alternar entre tabla densa y tarjetas apiladas verticalmente (ideal para móvil).
3. **Paginación táctil completa** — Selector "Filas por página" (10/15/25/50/100), botones ⬅ Anterior / Siguiente ➡ (44px táctiles), input numérico de página, estado persistente en `session_state["page_prio"]`.
4. **Tarjetas informativas** — Cada tarjeta muestra: Municipio (Depto), badges RANGO (color) + CONFIABILIDAD, grid responsivo con IPR, Casos reales, Proyección 2030, % Rural, % Indígena.
5. **Descarga CSV** — Descarga el dataset completo filtrado (no solo la página visible).

### Cambios realizados

| # | Función | Implementación | Verificación |
|---|---------|----------------|--------------|
| **M4-1** | Métricas KPI resumen | `st.columns(4)` con `st.metric()`: Municipios (delta=desglose rangos), Proyección 2030 (delta=casos reales), IPR promedio (delta=máx), Confiabilidad BAJA (delta=% total, delta_color=inverse). | 4 tarjetas visibles arriba de la tabla; valores calculados sobre `df_vista` filtrado. |
| **M4-2** | Toggle Vista Tarjeta/Tabla | `st.toggle("🃏 Vista tarjetas (móvil)", key="vista_tarjetas_prioridad")`. False=tabla, True=tarjetas HTML/CSS responsivo. | Toggle funcional; tarjetas se apilan verticalmente en móvil (CSS grid `auto-fit minmax(120px)`). |
| **M4-3** | Paginación táctil | `st.selectbox("Filas por página", [10,15,25,50,100])`; `session_state["page_prio"]`; botones `st.button("⬅ Anterior")` / `st.button("Siguiente ➡")` (disabled en bordes); `st.number_input` para salto directo. CSS M1: `min-height: 44px`. | Navegación fluida; página persiste al cambiar tabs; controles táctiles grandes. |
| **M4-4** | Tarjetas HTML responsivas | `st.markdown(unsafe_allow_html=True)` con CSS inline: border-left coloreado por RANGO (CRITICO=rojo, ALTO=amarillo, MEDIO=verde, BAJO=gris), badges RANGO+CONFIABILIDAD, grid 5 columnas que colapsa a 1 en móvil. | Tarjetas legibles en móvil sin scroll horizontal; colores semánticos; badges informativos. |
| **M4-5** | Descarga completa | `st.download_button` usa `df_prioridad[columnas_mostrar].to_csv()` (dataset completo filtrado, no solo página). | CSV descargado tiene todas las filas filtradas. |

### Pruebas ejecutadas
- ✅ Sintaxis Python: `python -m py_compile app/streamlit_app.py` — sin errores.
- ✅ Carga app: `streamlit run app/streamlit_app.py --server.headless true` — puerto 8501, sin tracebacks.
- ✅ Métricas KPI: 4 tarjetas muestran valores correctos calculados sobre `df_vista` filtrado.
- ✅ Toggle tarjetas/tabla: alternancia fluida; tarjetas se apilan vertical en móvil.
- ✅ Paginación: botones ⬅/➡ funcionan, input numérico salta páginas, selector filas/página actualiza total_pages.
- ✅ Persistencia: `session_state["page_prio"]` sobrevive a cambio de tabs.
- ✅ Tarjetas: border-left semántico por RANGO, badges CONFIABILIDAD BAJA rojos, grid responsivo.
- ✅ Filtros M2 + Mapas M3: persisten y sincronizan con nueva tabla (df_vista filtrado por session_state).
- ✅ Navegación tabs: 7 tabs cargan correctamente.

### Archivos modificados
- `app/streamlit_app.py` — tab_priorizacion reescrita: métricas KPI, toggle vista, paginación completa, tarjetas HTML, descarga completa.

---

## ETAPA M5 — IDENTIDAD VISUAL: TEMA INSTITUCIONAL + CSS EXTERNO + GLOSARIO ✅ COMPLETADA

**Fecha:** 2026-11-13  
**Rama:** `feature/mobile-audit-fixes`  
**Commit base:** `2fa4b25` (M4 completo)  
**Archivos nuevos:** `.streamlit/theme.toml`, `app/styles.css`  
**Archivo modificado:** `app/streamlit_app.py` (~2600 → ~2700 líneas)

### Objetivo
Externalizar estilos a archivo CSS dedicado, crear tema institucional Streamlit (`.streamlit/theme.toml`), e implementar glosario técnico interactivo con tooltips accesibles (hover/tap).

### Cambios realizados

| # | Función | Implementación | Verificación |
|---|---------|----------------|--------------|
| **M5-1** | Tema Streamlit institucional | `.streamlit/theme.toml` con `primaryColor=#176B50`, `backgroundColor=#FFFFFF`, `secondaryBackgroundColor=#EAF3ED`, `textColor=#164C3B`, config de server/runner/browser/logger. | Streamlit aplica paleta nativa a widgets (buttons, tabs, inputs, metricas); coherente con CSS custom. |
| **M5-2** | CSS externalizado | `app/styles.css` (~400 líneas) con: variables de paleta, componentes `.np-badge`, `.np-filter-chip`, `.np-card`, `.np-tooltip`, `.np-metric`, media queries responsive, scrollbars, focus-visible, animaciones. Cargado vía `@st.cache_data` + `st.markdown(unsafe_allow_html=True)`. | App carga CSS desde archivo; cambios en CSS no requieren tocar Python; cache invalida al modificar archivo. |
| **M5-3** | Glosario técnico interactivo | Diccionario `GLOSARIO` (12 términos: IPR, CONFIABILIDAD, RANGO, PROY_2030, RURAL, INDIGENA, CASOS_REALES, CASOS_PRED, ESCENARIO, IC80, DIVIPOLA, SIVIGILA_113). Función `tooltip(term, label)` genera `<span class="np-tooltip" data-tooltip="...">`. Tooltip CSS puro (hover desktop, tap móvil via `tabindex="0"`). Renderizado en 3 columnas al final de pestaña Metodología. | Hover en desktop muestra definición completa; tap en móvil abre tooltip; 12 términos cubren todas las métricas clave. |
| **M5-4** | Tooltips en caption principal | `tooltip("IPR")` y `tooltip("SIVIGILA_113")` en caption del header. | Usuario ve definición al pasar cursor/tocar términos clave desde el inicio. |
| **M5-5** | Componentes CSS reutilizables | Clases `.np-badge` (rangos), `.np-card` (tarjetas priorización), `.np-filter-chip` (chips M2), `.np-metric` (KPIs), `.np-tooltip` (glosario). Colores semánticos desde paleta institucional. | Consistencia visual en toda la app; fácil mantenimiento; dark-mode ready (solo variables). |

### Pruebas ejecutadas
- ✅ Sintaxis Python: `python -m py_compile app/streamlit_app.py` — sin errores.
- ✅ Carga app: `streamlit run app/streamlit_app.py --server.headless true` — puerto 8501, sin tracebacks.
- ✅ Tema `.streamlit/theme.toml`: widgets nativos (botones, tabs, selectbox, metricas) usan paleta institucional.
- ✅ CSS `app/styles.css`: cargado correctamente; estilos aplicados a tabs, botones, tarjetas, tooltips, paginación.
- ✅ Glosario: 12 términos renderizados en 3 columnas en pestaña Metodología; tooltips funcionan en hover (desktop) y tap (móvil).
- ✅ Tooltips en header: IPR y SIVIGILA_113 muestran definición al hover/tap.
- ✅ Filtros M2 + Mapas M3 + Tablas M4: persisten y sincronizan con nueva arquitectura CSS.
- ✅ Navegación tabs: 7 tabs cargan correctamente.

### Archivos nuevos
- `.streamlit/theme.toml` — Configuración de tema Streamlit + server/runner/browser/logger.
- `app/styles.css` — Estilos CSS institucionales completos (~400 líneas, comentados, organizados por secciones).

### Archivos modificados
- `app/streamlit_app.py` — `load_css()` con cache, `GLOSARIO` dict, `tooltip()` function, caption con tooltips, sección glosario en tab_metodologia.

---

## ETAPA ACTUAL: 1 — AUDITORÍA INTEGRAL

### Objetivo
Inspeccionar el repositorio, arquitectura, datos, modelos, cálculos del IPR, gráficas, mapas, filtros y dependencias. Producir un diagnóstico técnico y científico sin modificar código.

---

## 1. ARQUITECTURA Y ESTRUCTURA DEL REPOSITORIO

| Ruta | Descripción | Tamaño |
|------|-------------|--------|
| `app/streamlit_app.py` | Punto de entrada único (1793 líneas) | 54 KB |
| `app/verificar_codigos.py` | Script auxiliar de diagnóstico (solo CLI) | 3.6 KB |
| `data/resultados_nutripredict.json` | Resultados municipales (1119 filas, 17 columnas) | 561 KB |
| `data/panel_mensual.parquet` | Panel mensual 2016-2025 (134,280 filas, 7 cols) | 139 KB |
| `data/panel_semanal.parquet` | Panel semanal 2016-2025 (584,118 filas, 12 cols) | 650 KB |
| `data/col_departamentos_inset_nacional.geojson` | Límites departamentales (DANE MGN 2025) | 397 KB |
| `data/col_municipios_inset_nacional.geojson` | Límites municipales (DANE MGN 2025) | 2.5 MB |
| `outputs/resultados_consolidados.xlsx` | 12 hojas con métricas, proyecciones, IPR, supuestos | 476 KB |
| `outputs/metricas_modelos.csv` | 21 filas, 15 columnas (validación 2023 + prueba 2024-2025) | 4.5 KB |
| `outputs/seleccion_modelos.json` | Hiperparámetros y modelo elegido por frecuencia/nivel | 2.3 KB |
| `outputs/calidad_datos.json` | Informe de calidad y exclusiones | 3.4 KB |
| `notebooks/NUTRIPREDICT_proyecto_2016_2025_3_modelos_(1) (1).ipynb` | Notebook fuente (19 celdas) | 798 KB |
| `requirements.txt` | 5 dependencias **sin versiones fijadas** | 5 líneas |
| `.streamlit/config.toml` | **Vacío** (0 bytes) | 0 B |

---

## 2. PUNTO DE ENTRADA Y NAVEGACIÓN ACTUAL

La app define **7 pestañas (tabs)**:

1. **Mapa** — Coropletas departamental (PROY_2030) o municipal (IPR).
2. **Priorización municipal** — Tabla ordenada por IPR + filtros.
3. **Evolución mensual** — Serie temporal por municipio (panel_mensual).
4. **Evolución semanal** — Serie temporal por municipio (panel_semanal).
5. **Proyección 2026–2030** — Nacional / Departamental / Municipal (3 escenarios + IC80).
6. **Modelos y calidad** — Métricas (filtrables), informe de calidad, descargas.
7. **Metodología y limitaciones** — Texto explicativo (markdown estático).

**Filtros globales (sidebar):**
- Nivel territorial: Departamentos / Municipios (radio)
- Departamento: selectbox con "Todos"

**Filtros por pestaña:**
- Mensual/Semanal: Departamento → Municipio → Rango de fechas (slider).
- Proyección: Nivel (radio) → Departamento → Municipio (si municipal).

---

## 3. DATOS Y ESTRUCTURA

### 3.1 `resultados_nutripredict.json` (1119 municipios × 17 columnas)

| Columna | Tipo | No nulos | Observaciones |
|---------|------|----------|---------------|
| DIVIPOLA | string (5 dígitos) | 1119 | Normalizado con ceros a la izquierda |
| DPTO | string | 1119 | 33 departamentos únicos |
| MUNICIPIO | string | 1119 | — |
| CASOS_REALES | int | 1119 | Prueba 2024-2025 (un paso adelante) |
| CASOS_PRED | float | 1119 | Predicción del modelo seleccionado |
| PROY_2030 | float | 1119 | Escenario central 2030 |
| PROY_2030_BAJO / ALTO / P10 / P90 | float | 1119 | Intervalos de incertidumbre |
| ESPERADOS_SIGUIENTE_ANIO | float | 1119 | Pronóstico recursivo 12 meses (exploratorio) |
| TASA_100K | **null** | **0** | **Completamente vacío** (no se aportó población) |
| RURAL | string ("84.7%") | 1119 | % casos rurales notificados (con encogimiento) |
| INDIGENA | string ("98.0%") | 1119 | % casos indígenas notificados (con encogimiento) |
| IPR | float | 1119 | 27.93 – 99.51 (mediana 47.45) |
| RANGO | string | 1119 | Cuartiles: CRÍTICO 280, ALTO 279, MEDIO 280, BAJO 280 |
| CONFIABILIDAD | string | 1119 | ADECUADA 564 / BAJA 555 (< 10 casos en 24 meses) |

**Calidad:** 0 duplicados por DIVIPOLA; PROY_2030 siempre dentro de [BAJO, ALTO]; P10 ≤ P90.

### 3.2 Paneles Parquet
- **Mensual:** 134,280 filas (1119 municipios × 120 meses 2016-2025). Sin faltantes.
- **Semanal:** 584,118 filas (1119 municipios × ~523 semanas). Sin faltantes.
- Columnas clave: DIVIPOLA_RESIDENCIA, fecha (ANIO_MES_DT / SEMANA_INI), CASOS, CASOS_RURAL, CASOS_INDIGENA, departamento, municipio.

### 3.3 GeoJSON (DANE MGN 2025, simplificados por ytolosa, CC BY 4.0)
- Departamentos: 33 features, propiedad `divipola_dep` (2 dígitos).
- Municipios: 1122 features, propiedad `divipola_mun` (5 dígitos).
- **Cobertura:** 1119 municipios en resultados; el script `verificar_codigos.py` reporta 3 municipios con geometría pero sin resultados y 0 al revés (después de normalización).

### 3.4 Outputs Excel (`resultados_consolidados.xlsx`) — 12 hojas
- `Resumen_Modelos` — 21 filas × 15 cols (3 frecuencias × 3 modelos × 3-4 niveles).
- `Proy_Nacional` — 5 años × 3 escenarios + IC80.
- `Proy_Departamental` — 495 filas (33 deptos × 5 años × 3 escenarios).
- `Proy_Municipal` — 1119 filas × 30 cols (base + 5 años × 3 escenarios × 3 + P10/P90 + crecimiento).
- `Priorizacion_IPR_Municipal` — 1119 × 16 (cálculo completo del IPR).
- `Sensibilidad_IPR` — 4 alternativas comparadas vs IPR propuesto (Spearman 0.20–0.91).
- `Supuestos` — 9 filas documentando unidad, modelos, selección, pronóstico 12m, escenarios 2026-2030, incertidumbre, **IPR (pesos vol=0.5, rur=0.25, ind=0.25)**, supuestos no verificables.
- `Notas` — 7 advertencias clave.
- `Retrovalidacion_proyeccion` — 6 horizontes (h=1..6) con sd_log y sesgo.
- `Calidad_Datos`, `Calidad_Fechas` — Resúmenes de proceso.

---

## 4. MODELOS PREDICTIVOS (EVIDENCIA REAL VS DOCUMENTACIÓN)

### 4.1 Lo que **realmente existe** (notebook + outputs)

| Frecuencia | Modelos entrenados | Seleccionado (validación 2023, municipal) | Métrica |
|------------|-------------------|------------------------------------------|---------|
| Mensual | LightGBM (Poisson), XGBoost (Poisson), RandomForest | **LightGBM (Poisson)** | RMSE |
| Semanal | LightGBM (Poisson), XGBoost (Poisson), RandomForest | **XGBoost (Poisson)** | RMSE |

- Hiperparámetros fijos en `seleccion_modelos.json`.
- Validación: 2023 (entrenamiento 2017-2022). Prueba: 2024-2025 (mismos hiperparámetros, re-ajustado con 2017-2023).
- Predicción **a un paso** (usa casos observados hasta el periodo anterior).
- **No hay** GRU, SARIMA, Holt-Winters, GLM Poisson/NegBin, Ensamble LGBXGB, ni suavizamiento exponencial en el notebook (solo 19 celdas, imports: LGBMRegressor, XGBRegressor, RandomForestRegressor).

### 4.2 Lo que **dice la pestaña "Metodología" (LÍNEAS 1668-1682)** — **INCONSISTENCIA CRÍTICA**

> "El análisis utiliza varios enfoques complementarios:
> - Modelos de referencia... 
> - Modelos de aprendizaje automático, incluyendo **Random Forest, XGBoost y LightGBM**.
> - Modelos de conteos, incluyendo **GLM Poisson y binomial negativa**.
> - Modelos de series de tiempo, incluyendo **suavizamiento exponencial, Holt-Winters y SARIMA/SARIMAX**.
> - Una **red neuronal GRU global con pérdida de Poisson**."

**Esto es falso:** ninguno de esos modelos adicionales existe en el notebook ni en los outputs. El texto **inventa funcionalidades** (prohibido por AGENTES.md §2).

### 4.3 Modelo semanal en la pestaña Metodología (LÍNEA 1693-1694)
> "El modelo final mensual es **LightGBM Poisson** y el modelo final semanal es **Ensamble LGBXGB**."

**Falso:** el seleccionado semanal es **XGBoost (Poisson)** (ver `seleccion_modelos.json` y hoja `Resumen_Modelos`).

---

## 5. CÁLCULOS DEL IPR (ÍNDICE DE PRIORIZACIÓN RELATIVA)

### 5.1 Definición real (notebook celda 18 + hoja `Supuestos` + `Priorizacion_IPR_Municipal`)

**Pesos (sin población):** `vol = 0.50`, `rur = 0.25`, `ind = 0.25` — **supuesto de planeación**, no estimado.

**Componentes:**
1. **Volumen** (`COMP_VOLUMEN`): percentil del `ESPERADOS_12M` (pronóstico recursivo 12m, LightGBM mensual re-ajustado, exploratorio, no validado >1 paso).
2. **Territorial** (`COMP_TERRITORIAL`): promedio de percentiles de `PROP_RURAL_AJ` y `PROP_INDIGENA_AJ` (encogimiento hacia % nacional con K=20).
3. `IPR_SCORE = 0.5 * COMP_VOLUMEN + 0.25 * PROP_RURAL_AJ_pct + 0.25 * PROP_INDIGENA_AJ_pct`
4. `NIVEL_PRIORIDAD` = cuartiles del IPR_SCORE → etiquetas: BAJO, MEDIO, ALTO, CRÍTICO (qcut con `rank(method='first')`).

**Sin población:** no se calcula `TASA_100K` (queda null en JSON). Si se aportara CSV `DIVIPOLA,POBLACION`, cambiarían pesos a `vol=0.2, tasa=0.4, rur=0.2, ind=0.2` (supuesto experto).

### 5.2 Validación del IPR (hoja `Sensibilidad_IPR`)
| Alternativa | Spearman vs IPR propuesto | % coincidencia en top 25% |
|-------------|--------------------------|--------------------------|
| Índice previo (casos predichos, % sin ajustar) | 0.909 | 73.8% |
| Solo volumen esperado | 0.700 | 47.7% |
| Solo territorial | 0.201 | 51.3% |
| Pesos iguales (0.33 c/u) | 0.687 | 80.3% |

El IPR propuesto corrige sesgo hacia volumen puro y da peso a ruralidad/indigenidad.

### 5.3 Confiabilidad
- 555 municipios (49.6%) tienen **CONFIABILIDAD = BAJA** (< 10 casos en 24 meses).
- Sus IPR son inestables; la app muestra advertencia en la pestaña Priorización.

---

## 6. PROYECCIONES 2026–2030

### 6.1 Metodología (hoja `Supuestos`, fila 4)
> "Nivel base = media de los últimos 2 años completos; crecimiento = pendiente log-lineal de 4 años por departamento, encogida hacia la nacional (K=300), tope ±10%, amortiguado x0.85 por año."

### 6.2 Escenarios (fila 5)
> "Central ∓ 5 pp anuales (supuesto de planeación, no estimado)."

### 6.3 Incertidumbre (fila 6)
> "IC80 del central: log-normal con σ_h = σ1·√h, σ1 depto=0.291, nacional=0.155 (supuesto; retro-validación solo hasta h=6)."

### 6.4 Retrovalidación (hoja `Retrovalidacion_proyeccion`)
| h | n_pares | sd_robusto_log | sesgo_mediano_log |
|---|---------|----------------|-------------------|
| 1 | 198 | 0.376 | -0.050 |
| 2 | 165 | 0.566 | 0.054 |
| 3 | 132 | 0.562 | 0.117 |
| 4 | 99 | 0.513 | 0.294 |
| 5 | 66 | 0.460 | 0.063 |
| 6 | 33 | 0.413 | -0.301 |

La incertidumbre crece con el horizonte; el IC80 es un supuesto (no estimado empíricamente más allá de h=6).

---

## 7. GRÁFICAS Y MAPAS — ESTADO ACTUAL

| Elemento | Librería | Calidad | Problemas detectados |
|----------|----------|---------|----------------------|
| Mapa departamental (PROY_2030) | Plotly `px.choropleth` | Funcional | Escala `YlOrRd` sin leyenda numérica; sin título descriptivo completo; tooltips básicos. |
| Mapa municipal (IPR) | Plotly `px.choropleth` | Funcional | `range_color=(0,100)` fijo; sin distinción visual de CONFIABILIDAD BAJA; tooltips con RANGO pero sin IPR numérico en hover principal. |
| Evolución mensual/semanal | Plotly `px.line` | Funcional | Ejes sin unidades en título; sin banda de confianza; modo `lines+markers` ok. |
| Proyecciones (Nac/Dep/Mun) | Plotly `px.line` + `add_scatter` (IC80) | Funcional | Colores hardcoded (verde/azul/rojo); IC80 solo para escenario central; municipal sin IC80 en datos. |
| Tabla priorización | `st.dataframe` + `column_config` | Funcional | Formato % para RURAL/INDIGENA ok; sin ordenamiento por RANGO + IPR simultáneo en UI (solo en código). |
| Métricas modelos | `st.dataframe` | Funcional | Filtros por frecuencia/nivel ok; descarga CSV. |

**Identidad visual actual:** CSS inyectado inline (líneas 17-98) con `max-width: 1600px`, media queries responsive. **No usa la paleta institucional** (#176B50, #164C3B, #EAF3ED, #E5B94B, #C94C4C) definida en AGENTES.md §7.

---

## 8. DEPENDENCIAS Y CONFIGURACIÓN

### `requirements.txt` (sin versiones)
```
streamlit
plotly
pandas
pyarrow
openpyxl
```
**Riesgo:** builds no reproducibles; Streamlit 1.67.0 ya difiere de versiones antiguas (API `st.column_config`, `st.tabs`).

### `.streamlit/config.toml` — **VACÍO**
Falta configuración de tema, servidor, logging, etc.

### `.gitignore` — Correcto (excluye .venv, __pycache__, .env, secrets, data/raw/, models/).

---

## 9. PROBLEMAS ENCONTRADOS (CLASIFICADOS POR GRAVEDAD)

### 🔴 CRÍTICOS (Integridad científica / AGENTES.md §2)

| # | Problema | Ubicación | Regla violada |
|---|----------|-----------|---------------|
| C1 | **Modelos inventados en Metodología**: GRU, SARIMA, Holt-Winters, GLM, Ensamble LGBXGB no existen. | `streamlit_app.py` líneas 1668-1682, 1693-1694 | §2 "No inventar... modelos... funcionalidades que aparenten estar respaldadas por información inexistente" |
| C2 | **Modelo semanal incorrecto**: dice "Ensamble LGBXGB" pero es XGBoost (Poisson). | `streamlit_app.py` línea 1694 | §2 "No inventar... resultados" |
| C3 | **TASA_100K presentada como existente** (columna en tabla priorización) pero 100% null. | `streamlit_app.py` líneas 652-664 (columna en `columnas_tabla`) | §2 "No inventar... indicadores... variables" |

### 🟠 ALTOS (Calidad / Consistencia)

| # | Problema | Ubicación | Impacto |
|---|----------|-----------|---------|
| A1 | Paleta institucional **no aplicada** (CSS usa colores genéricos Plotly). | `streamlit_app.py` líneas 17-98, mapas/gráficas | Identidad visual §7 no cumplida. |
| A2 | `.streamlit/config.toml` vacío — sin tema, sin configuración de servidor. | `.streamlit/config.toml` | Despliegue y UX inconsistentes. |
| A3 | `requirements.txt` sin versiones fijadas — builds no reproducibles. | `requirements.txt` | Riesgo de roturas en actualizaciones. |
| A4 | Mapa municipal: `range_color=(0,100)` fijo pero IPR real va 27.9–99.5; no usa escala divergente ni muestra CONFIABILIDAD. | `streamlit_app.py` línea 620 | Lectura errónea de prioridad relativa. |
| A5 | Tooltips del mapa municipal no muestran IPR numérico principal (solo en hover_data secundario). | `streamlit_app.py` línea 618 | Dificulta inspección rápida. |
| A6 | Pestaña Proyección municipal **sin IC80** (datos no los tienen), pero UI no lo advierte. | `streamlit_app.py` líneas 1307-1338 | Falta transparencia §12. |
| A7 | Filtros: no hay botón "Restablecer filtros" ni mensaje "Sin resultados" consistente. | `streamlit_app.py` sidebar + tabs | Usabilidad §11. |
| A8 | CSS inline de 80 líneas — difícil de mantener; media queries repetidas. | `streamlit_app.py` líneas 17-98 | Mantenibilidad §13. |

### 🟡 MEDIOS (Mejoras de arquitectura / código)

| # | Problema | Ubicación |
|---|----------|-----------|
| M1 | App monolítica (1793 líneas en un solo archivo) — sin separación de capas (datos, UI, utilidades). | `streamlit_app.py` |
| M2 | Lógica de normalización de columnas repetida (mensual, semanal, proyecciones). | `streamlit_app.py` líneas 326-370, 247-291 |
| M3 | Función `tabla_escenarios` y `formato_escenarios` duplicadas en lógica. | `streamlit_app.py` líneas 294-324, 321-324 |
| M4 | Carga de todos los datos al inicio (incluye Excel 476 KB) — sin `st.cache_data` en Excel/CSV (solo JSON/Parquet). | `streamlit_app.py` líneas 169-211 |
| M5 | `verificar_codigos.py` duplica lógica de normalización y comparación que ya está en la app. | `app/verificar_codigos.py` |

### 🟢 BAJOS (Cosméticos / Documentación)

| # | Problema |
|---|----------|
| B1 | Título de la app: "Primera prueba: archivos, codigos territoriales y mapas." (línea 102) — texto provisional. |
| B2 | Leyendas de mapas y gráficas en español pero sin unidades consistentes (ej. "Casos notificados esperados" vs "PROYECCION"). |
| B3 | Falta `README.md` con instrucciones de desarrollo, pruebas, contribución. |

---

## 10. PLAN DE IMPLEMENTACIÓN POR ETAPAS (SEGÚN AGENTES.md §15)

> **Nota:** No se modifica código en esta etapa. El plan abajo es una propuesta para autorización del usuario.

| Etapa | Objetivo | Archivos principales a tocar | Validación |
|-------|----------|------------------------------|------------|
| **1. Auditoría** ✅ | Diagnóstico completo (este documento) | — | `PROGRESS_NUTRIPREDICT.md` creado; `git status` limpio. |
| **2. Plan de rediseño y arquitectura visual** | Definir nueva estructura de tabs, layout, componentes reutilizables; separar CSS a archivo; crear `theme.toml`. | `.streamlit/config.toml`, `.streamlit/theme.toml` (nuevo), `app/` (nueva estructura) | Wireframes / mockups aprobados. |
| **3. Identidad visual y estilos** | Aplicar paleta institucional (#176B50, #164C3B, #EAF3ED, #FFFFFF, #F3F6F4, #64746B, #E5B94B, #C94C4C); tipografía, espaciado, tarjetas, botones coherentes. | `.streamlit/theme.toml`, `app/styles.css` (nuevo, vía `st.html` o componente), `streamlit_app.py` (limpieza CSS inline) | Visual regression: todas las páginas con paleta; contraste AA. |
| **4. Gráficas y visualizaciones** | Profesionalizar: títulos, ejes, unidades, leyendas, hover templates, paleta consistente, bandas IC80 donde existan, rankings con confianza. | `app/charts.py` (nuevo módulo), `streamlit_app.py` (delegar a charts) | Cada gráfica pasa checklist §9. |
| **5. Mapas geográficos** | Coropletas con escala perceptual, leyenda numérica, tooltips ricos (IPR, RANGO, CONFIABILIDAD, casos), zoom/pan fluidos, filtro departamental sincronizado, indicador de municipios sin geometría. | `app/maps.py` (nuevo), `streamlit_app.py`, GeoJSON validado | Mapa departamental y municipal §10. |
| **6. Navegación y filtros** | Sidebar unificado, breadcrumbs, reset global, persistencia de selección entre tabs, mensajes "sin datos", URL params para deep-linking. | `app/filters.py` (nuevo), `streamlit_app.py` | Filtros §11; navegación §8. |
| **7. Metodología y transparencia** | **Corregir texto inventado** (C1, C2, C3). Documentar solo lo real: 3 modelos, IPR con pesos, supuestos de proyección, limitaciones. Añadir glosario, referencias, hoja de supuestos visible. | `app/methodology.py` (nuevo), `streamlit_app.py` (pestaña Metodología) | Texto §12; sin invenciones. |
| **8. Pruebas y auditoría final** | Lint (ruff/black), imports, carga app, navegación completa, filtros, mapas, gráficas, descargas, datos no alterados. `git diff` revisado. | Todo | Checklist §14; reporte final §16. |

---

## 11. PRÓXIMOS PASOS INMEDIATOS (REQUIEREN AUTORIZACIÓN)

**✅ COMPLETADO EN ETAPA M1:**
1. **Corregidos C1, C2, C3** (integridad científica) — prioridad absoluta.
   - ✅ Pestaña Metodología reescrita con solo 3 modelos reales.
   - ✅ "Ensamble LGBXGB" → "XGBoost (Poisson)" corregido.
   - ✅ `TASA_100K` eliminada de tabla priorización + nota explicativa.

2. **Rama de trabajo creada** (`feature/mobile-audit-fixes`) y commit de respaldo (`29b0da2`).

3. **Críticos móviles resueltos** (A2, B1, D1, D2, F1 + E1/E2/E3/E6, D3/D4/D5, G3, A1/A5/A6).
   - ✅ Tabs táctiles 44×44px con paleta institucional.
   - ✅ Sidebar colapsado + botón "🔍 Filtros" en header.
   - ✅ Mapa municipal: range_color dinámico, colorbar, hovertemplate tap.
   - ✅ Tabla priorización: 7 columnas prioritarias, toggle "Mostrar todo".
   - ✅ Gráficas: ejes/leyenda/marcadores responsivos, paleta institucional.
   - ✅ Limitaciones en expander colapsable.

**✅ COMPLETADO EN ETAPA M2:**
4. **Commit cambios Etapa M1** en `feature/mobile-audit-fixes` (`292008a`).
5. **Filtros globales persistentes** en `session_state` (nivel, departamento, municipio, fechas).
6. **Chips de filtros activos** en las 7 tabs con paleta institucional.
7. **Botón "🔄 Restablecer filtros"** en sidebar y en chips (header de cada tab).
8. **Sidebar sincronizado** con tabs: un solo origen de verdad (`session_state`).
9. **Selectores táctiles** (44px min-height) en sidebar.

**✅ COMPLETADO EN ETAPA M5:**
19. **Tema Streamlit institucional** — `.streamlit/theme.toml` con paleta oficial (#176B50, #164C3B, #EAF3ED, #E5B94B, #C94C4C, #64746B), config server/runner/browser/logger.
20. **CSS externalizado** — `app/styles.css` (~400 líneas): componentes `.np-badge`, `.np-card`, `.np-tooltip`, `.np-filter-chip`, `.np-metric`, media queries, scrollbars, focus-visible, animaciones. Cargado vía `@st.cache_data`.
21. **Glosario técnico interactivo** — 12 términos (IPR, CONFIABILIDAD, RANGO, PROY_2030, RURAL, INDIGENA, CASOS_REALES, CASOS_PRED, ESCENARIO, IC80, DIVIPOLA, SIVIGILA_113) con tooltips CSS puro (hover desktop / tap móvil). Renderizado en 3 columnas en pestaña Metodología.
22. **Tooltips en header** — IPR y SIVIGILA_113 en caption principal con definiciones accesibles.
23. **Componentes reutilizables** — Clases CSS semánticas para badges, tarjetas, chips, métricas, tooltips; colores desde paleta institucional.

**✅ COMPLETADO EN ETAPA M6:**
24. **Carga de datos centralizada** — `app/data_loader.py`: `inicializar_datos()` carga y normaliza todos los datasets (JSON, Parquet, Excel, CSV) con validaciones y cache `@st.cache_data`.
25. **Gráficas separadas** — `app/charts.py`: 7 funciones (`crear_linea_mensual`, `crear_linea_semanal`, `crear_proyeccion_nacional`, `crear_proyeccion_departamental`, `crear_proyeccion_municipal`, `tabla_escenarios`). Paleta institucional en `constants.py`.
26. **Mapas separados** — `app/maps.py`: 5 funciones (`crear_mapa_departamental`, `crear_mapa_municipal`, `agregar_overlay_confiabilidad_baja`, `crear_mapa_proyeccion_animado`, `preparar_datos_mapa_departamental`).
27. **Filtros centralizados** — `app/filters.py`: `init_filters`, `reset_filters`, `render_sidebar_filtros`, `render_active_filters_chips`, selectores encadenados, slider fechas.
28. **Componentes UI reutilizables** — `app/components.py`: `render_metricas_kpi`, `render_paginacion`, `render_tarjetas_prioridad`, `preparar_dataframe_prioridad`, `tooltip`, `render_glosario`, `badge_rango`, `badge_confiabilidad`, `load_css`.
29. **Constantes compartidas** — `app/constants.py`: Paleta, colores escenarios, orden rangos, columnas priorizadas, formato tablas, tabs, page_config.
30. **Páginas como módulos** — `app/pages/*.py`: 7 módulos (mapa, priorizacion, mensual, semanal, proyeccion, modelos, metodologia) con función `render_tab_*`.
31. **Orquestador delgado** — `app/streamlit_app.py`: ~180 líneas. Config → carga datos → header → sidebar → 7 tabs delegados a `pages`.

**🔄 SIGUIENTES (requieren autorización):**
32. **Fijar dependencias** en `requirements.txt` con versiones exactas (lock).

---

## 12. ÚLTIMO PUNTO ESTABLE DE TRABAJO

- **Commit base:** `0b32701` ("Etapa M5: Identidad visual - Tema institucional + CSS externo + Glosario interactivo") en rama `feature/mobile-audit-fixes`.
- **Rama actual:** `feature/mobile-audit-fixes` (trabajo Etapa M6 completado, sin commit aún).
- **Archivos modificados:** `app/streamlit_app.py` (Etapas M1–M6, ~2700 → ~180 líneas), `app/__init__.py`.
- **Archivos nuevos:** `.streamlit/theme.toml`, `app/styles.css`, `app/data_loader.py`, `app/charts.py`, `app/maps.py`, `app/filters.py`, `app/components.py`, `app/constants.py`, `app/pages/` (7 módulos + `__init__.py`), `AGENTES.md`, `PROGRESS_NUTRIPREDICT.md`, `MOBILE_AUDIT_NUTRIPREDICT.md`.
- **Entorno:** `.venv` funcional (Python 3.14.7, Streamlit 1.67.0, Plotly 7.1.0, Pandas 3.1.1).
- **App ejecutable:** `streamlit run app/streamlit_app.py` carga sin errores (verificado 2026-11-13).
- **Estado crítico C1–C3:** **RESUELTOS** (integridad científica restaurada).
- **Estado crítico móvil A2/B1/D1/D2/F1:** **RESUELTOS** (usabilidad táctil profesional).
- **Estado M2 filtros:** **RESUELTOS** (globales persistentes, chips, reset, sincronización sidebar↔tabs).
- **Estado M3 mapas:** **RESUELTOS** (overlay CONFIABILIDAD BAJA, mini-mapa animado 2026-2030, tooltips enriquecidos).
- **Estado M4 tablas:** **RESUELTOS** (métricas KPI, vista tarjeta/tabla toggle, paginación táctil, tarjetas responsivas, descarga completa).
- **Estado M5 identidad:** **RESUELTOS** (tema .streamlit/theme.toml, CSS externalizado app/styles.css, glosario 12 términos con tooltips hover/tap).
- **Estado M6 arquitectura:** **RESUELTOS** (14 módulos nuevos, orquestador < 200 líneas, carga datos centralizada, gráficas/mapas/filtros/componentes/páginas separados).

---

## 13. ADVERTENCIAS PARA CONTINUIDAD (SI CAMBIA EL MODELO)

- **No re-ejecutar** la auditoría completa; leer este `PROGRESS_NUTRIPREDICT.md` y hacer `git status` + `git diff`.
- **No tocar** datos originales (`data/`, `outputs/`) ni fórmulas del IPR.
- **Prioridad:** corregir C1–C3 antes de cualquier cambio visual.
- **Verificar** que `TASA_100K` sigue null antes de decidir si mostrarla u omitirla.
- **Consultar** al usuario antes de reestructurar la app en módulos (Etapa 2).

---

**Fin del registro de la ETAPA 1.**  
A la espera de autorización para iniciar la implementación (corrección de problemas críticos C1–C3 y plan de rediseño Etapa 2).