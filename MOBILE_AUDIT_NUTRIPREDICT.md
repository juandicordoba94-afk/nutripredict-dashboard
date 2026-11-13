# MOBILE AUDITORÍA — NUTRIPREDICT Colombia 2030

**Fecha:** 2026-11-12  
**Modelo:** Qwen (FreeLLMAPI Auto)  
**Metodología:** Inspección estática de código (1793 líneas `streamlit_app.py`), análisis de CSS inline (líneas 17-98), revisión de 7 tabs, sidebar, mapas Plotly, gráficas, tablas, y componentes Streamlit.  
**Herramientas de prueba visual:** No disponibles (Playwright/Selenium no instalados). No se afirma verificación visual en dispositivos reales.

---

## RESUMEN EJECUTIVO

| Categoría | Hallazgos | Críticos | Altos | Medios | Bajos |
|-----------|-----------|----------|-------|--------|-------|
| **A. Encabezado y navegación** | 6 | 1 | 2 | 2 | 1 |
| **B. Sidebar y filtros** | 7 | 0 | 3 | 3 | 1 |
| **C. Indicadores y tarjetas** | 3 | 0 | 1 | 2 | 0 |
| **D. Mapas geográficos** | 8 | 2 | 3 | 2 | 1 |
| **E. Gráficas** | 6 | 0 | 3 | 2 | 1 |
| **F. Tablas** | 5 | 1 | 2 | 1 | 1 |
| **G. Metodología y textos** | 4 | 0 | 2 | 1 | 1 |
| **TOTAL** | **39** | **4** | **16** | **13** | **6** |

> **Nota:** La app **funciona** en móvil (Streamlit 1.67.0 tiene responsive nativo), pero la experiencia **no es profesional**: hay desbordamientos, textos ilegibles, tooltips inutilizables en táctil, filtros inaccesibles, y la identidad visual institucional no se aplica.

---

## DETALLE POR CATEGORÍA

### A. ENCABEZADO Y NAVEGACIÓN

| # | Elemento | Problema | Tamaño | Gravedad | Solución propuesta | Archivo |
|---|----------|----------|--------|----------|-------------------|---------|
| A1 | Título principal | `st.title` + `st.caption` con texto provisional "Primera prueba..." — no refleja identidad institucional. | Todos | 🟢 Baja | Cambiar caption por descripción oficial; aplicar tipografía/color institucional. | `streamlit_app.py:100-103` |
| A2 | Pestañas (7 tabs) | En móvil (< 768px): CSS fuerza `overflow-x: auto` pero **tamaño de tab 0.88rem** y `min-height: 2.75rem` — **difícil de tocar** con dedo (objetivo táctil mínimo 44×44px). | ≤ 768px | 🔴 **Crítica** | Aumentar `min-height: 44px`, `padding: 0.75rem 1rem`, `font-size: 1rem`; permitir `flex-wrap: wrap` en móviles muy pequeños. | `streamlit_app.py:65-79` |
| A3 | Desbordamiento horizontal página | CSS `[data-testid="stMainBlockContainer"] max-width: 1600px` + `padding-inline: clamp(1rem, 3vw, 3rem)` — **en móviles muy estrechos (320px) el padding consume demasiado ancho** útil. | ≤ 375px | 🟠 Alta | Reducir `padding-inline: clamp(0.5rem, 2vw, 1.5rem)` en `@media (max-width: 480px)`. | `streamlit_app.py:24-28, 47-50` |
| A4 | Espaciado superior | Sin `margin-top` coherente; el título queda pegado al borde en algunos navegadores móviles. | ≤ 768px | 🟡 Media | Añadir `padding-top: 1rem` al contenedor principal en móvil. | `streamlit_app.py:48-50` |
| A5 | Falta logo/identidad visual | No hay logotipo ni marca visual institucional en header. | Todos | 🟢 Baja | Añadir `st.logo()` (Streamlit 1.34+) o `st.image()` en header con SVG institucional. | `streamlit_app.py:100` |
| A6 | Tabs no comunican estado activo claramente | Color de tab activo usa tema Plotly/Streamlit por defecto, no paleta institucional (#176B50). | Todos | 🟡 Media | Estilizar `[aria-selected="true"]` con `background: #176B50; color: white;`. | `streamlit_app.py:17-98` (nuevo CSS) |

---

### B. SIDEBAR Y FILTROS

| # | Elemento | Problema | Tamaño | Gravedad | Solución propuesta | Archivo |
|---|----------|----------|--------|----------|-------------------|---------|
| B1 | Sidebar siempre expandido en móvil | `initial_sidebar_state="auto"` → en móvil **ocupa ~300px** tapando el contenido; usuario debe cerrarlo manualmente (hamburger menú nativo pequeño). | ≤ 768px | 🔴 **Crítica** | Cambiar a `initial_sidebar_state="collapsed"`; añadir botón "Filtros" visible en header móvil para abrir/cerrar. | `streamlit_app.py:14` |
| B2 | Radio "Nivel territorial" horizontal | `horizontal=True` en `st.radio` → **dos botones lado a lado** en móvil estrecho: texto se trunca o desborda. | ≤ 375px | 🟠 Alta | En `@media (max-width: 480px)` forzar `flex-direction: column` para radios; o usar `st.selectbox` en móvil. | `streamlit_app.py:575-579` |
| B3 | Selectbox "Departamento" (33 opciones) | Lista larga sin búsqueda; en móvil el dropdown nativo es **difícil de navegar con dedo** (altura de opción ~32px). | ≤ 768px | 🟠 Alta | Añadir `placeholder="Seleccione departamento"`; considerar `st.multiselect` con búsqueda o combobox personalizado. | `streamlit_app.py:581-584` |
| B4 | Filtros por pestaña (depto → municipio → fechas) | **No hay "Restablecer filtros"**; usuario debe recargar página. Selectores encadenados sin feedback visual de dependencia. | Todos | 🟠 Alta | Añadir `st.button("🔄 Restablecer", use_container_width=True)` que limpie `st.session_state` claves de filtros. | `streamlit_app.py:770-810, 910-950, 1048-1060` |
| B5 | Slider de fechas (mensual/semanal) | `st.slider` con `format="MM/YYYY"` — **manijas muy pequeñas** en táctil; rango por defecto = todo el período (120 meses / 523 semanas) → difícil reducir. | ≤ 768px | 🟡 Media | Aumentar tamaño de track/thumb via CSS (`::-webkit-slider-thumb { height: 24px; width: 24px; }`); añadir botones "Último año" / "Últimos 6 meses". | `streamlit_app.py:831-840, 969-980` |
| B6 | Filtros proyección: radio horizontal 3 opciones | `st.radio(..., horizontal=True)` con 3 etiquetas → **desborda en 320px**; se corta "Municipal". | ≤ 375px | 🟡 Media | En móvil: `flex-wrap: wrap` + `gap: 0.5rem`; o `st.selectbox` para ≤ 480px. | `streamlit_app.py:1048-1052` |
| B7 | Sin indicador de filtros activos | Usuario no ve qué filtros están aplicados salvo mirar cada control. | Todos | 🟢 Baja | Mostrar "chips" de filtros activos bajo el título de cada tab (ej. "Depto: Antioquia · Mpio: Medellín · 2023-01 a 2025-12"). | `streamlit_app.py` (nuevo componente) |

---

### C. INDICADORES Y TARJETAS

| # | Elemento | Problema | Tamaño | Gravedad | Solución propuesta | Archivo |
|---|----------|----------|--------|----------|-------------------|---------|
| C1 | No hay tarjetas de KPIs (resumen nacional) | La app **carece de dashboard inicial** con indicadores clave (total casos, proyección 2030, municipios críticos, cobertura). Solo tabs. | Todos | 🟠 Alta | Añadir tab "Inicio / Resumen nacional" (Etapa 8 AGENTS.md) con `st.metric` o tarjetas CSS Grid: 1 col móvil, 2 tablet, 4 desktop. | `streamlit_app.py` (nuevo tab) |
| C2 | Tablas usadas como "indicadores" | En tab Priorización, la tabla muestra 12 columnas → **en móvil requiere scroll horizontal**; no hay vista de tarjetas por municipio. | ≤ 768px | 🟡 Media | Para móvil: vista alternativa "Tarjetas" (toggle) mostrando solo IPR, RANGO, CASOS_REALES, PROY_2030, CONFIABILIDAD en layout vertical. | `streamlit_app.py:644-768` |
| C3 | Formato % en RURAL/INDIGENA | `column_config.NumberColumn(format="%.1f%%")` — **en columnas estrechas móviles se trunca** (ej. "98.0..."). | ≤ 480px | 🟡 Media | En móvil: `format="%.0f%%"` (sin decimal) o tooltip con valor completo. | `streamlit_app.py:737-744` |

---

### D. MAPAS GEOGRÁFICOS

| # | Elemento | Problema | Tamaño | Gravedad | Solución propuesta | Archivo |
|---|----------|----------|--------|----------|-------------------|---------|
| D1 | **Mapa municipal: `range_color=(0,100)` fijo** | IPR real 27.9–99.5 → **colores no usan rango real**; municipios con IPR 30 y 90 se ven similares. No hay distinción visual CONFIABILIDAD BAJA. | Todos | 🔴 **Crítica** | `range_color=(df['IPR'].min(), df['IPR'].max())`; añadir capa de patrón/puntos para CONFIABILIDAD BAJA; leyenda numérica visible. | `streamlit_app.py:620` |
| D2 | Tooltips mapa municipal **inutilizables en táctil** | `hover_data` requiere hover (ratón); en móvil **no hay hover** — tap abre tooltip pero **tapa el municipio**; difícil cerrar; no muestra IPR numérico principal. | ≤ 768px | 🔴 **Crítica** | Usar `plotly_chart(..., on_select="rerun")` + `selection_mode="points"` para capturar tap y mostrar info en `st.container()` lateral o modal; o `hoverlabel=dict(bgcolor="white", font_size=12)` + `hovertemplate` rico. | `streamlit_app.py:611-622, 635-636` |
| D3 | Mapa departamental sin leyenda numérica | `color_continuous_scale="YlOrRd"` pero **no se muestra colorbar** con valores; usuario no sabe qué significa cada tono. | Todos | 🟠 Alta | `fig.update_layout(coloraxis_showscale=True, coloraxis_colorbar=dict(title="Casos 2030", len=0.75))`. | `streamlit_app.py:598-608` |
| D4 | Altura fija 550px | `height=550` → **en móvil ocupa > 100vh**; obliga scroll vertical antes de ver contenido inferior. | ≤ 768px | 🟠 Alta | `height=min(550, window.innerHeight * 0.6)` via JS o CSS `max-height: 60vh`; en Streamlit: calcular alto dinámico o usar `use_container_width=True` sin height fijo. | `streamlit_app.py:630-633` |
| D5 | Controles de mapa (zoom/pan) nativos de Plotly | Botones `+/−` y home **muy pequeños** en táctil (16×16px); se superponen al mapa en móviles. | ≤ 768px | 🟡 Media | CSS: `.modebar { display: none; }` en móvil; habilitar `dragmode="pan"` por defecto; zoom con pellizco (pinch) nativo funciona. | `streamlit_app.py:624-628` (config `config=dict(displayModeBar=False)` en móvil) |
| D6 | Mapa sin indicador de municipios sin geometría | 3 municipios tienen geometría pero no resultados (y viceversa) — **usuario no lo sabe** salvo leer caption. | Todos | 🟡 Media | Añadir badge "⚠ 3 municipios sin geometría" clicable que filtre tabla priorización. | `streamlit_app.py:515-523, 638-642` |
| D7 | Proyección departamental/municipal sin mapa | Solo gráficas de líneas — **no hay coropleta de proyección por año/escenario**. | Todos | 🟢 Baja | En tab Proyección, añadir mini-mapa animado (slider año) o small multiples por escenario. | `streamlit_app.py:1039-1348` |
| D8 | GeoJSON municipales 2.5 MB | Carga inicial lenta en móvil (red 3G/4G); **sin loading state** ni progreso. | ≤ 768px | 🟢 Baja | Precargar con `st.cache_data` + `st.spinner`; considerar simplificación adicional (topojson) o tiles vectoriales. | `streamlit_app.py:118-135` |

---

### E. GRÁFICAS (Plotly Express)

| # | Elemento | Problema | Tamaño | Gravedad | Solución propuesta | Archivo |
|---|----------|----------|--------|----------|-------------------|---------|
| E1 | Ejes con texto truncado | `px.line` sin `tickfont.size` ni `tickangle` → **etiquetas de mes/año se solapan** en ancho < 480px. | ≤ 480px | 🟠 Alta | `fig.update_xaxes(tickfont=dict(size=10), tickangle=-45, nticks=8)`; en móvil reducir `nticks=6`. | `streamlit_app.py:854-878, 989-1011, 1074-1121` |
| E2 | Leyenda horizontal en proyecciones | `color_discrete_map` + 3 escenarios → **leyenda horizontal** en móvil se corta o empuja gráfica. | ≤ 480px | 🟠 Alta | `fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)))`; en móvil `orientation="v", x=1.02`. | `streamlit_app.py:1086-1090, 1192-1196, 1323-1327` |
| E3 | Marcadores (markers=True) muy pequeños | `marker=dict(size=5)` → **puntos de 5px imposibles de tocar** en táctil; hover no funciona bien. | ≤ 768px | 🟠 Alta | `marker=dict(size=8)` en móvil (CSS/JS detectar) o `hovertemplate` rico sin depender de marker. | `streamlit_app.py:868-872, 1002-1006, 1079` |
| E4 | Gráficas mensual/semanal: sin contexto de predicción | Solo muestran `CASOS` observados — **no superponen `CASOS_PRED` ni `PROY_2030`** para comparación visual. | Todos | 🟡 Media | Añadir trazas `CASOS_PRED` (línea discontinua) y banda `PROY_2030_P10/P90` como área sombreada. | `streamlit_app.py:854-878, 989-1011` |
| E5 | Altura fija 450px | Igual que mapas: **ocupa demasiado viewport** en móvil. | ≤ 768px | 🟡 Media | `height=min(450, window.innerHeight * 0.5)` o responsive via CSS `max-height: 50vh`. | `streamlit_app.py:874-878, 1007-1011` |
| E6 | Colores hardcoded (verde/azul/rojo) | `#2ca02c`, `#1f77b4`, `#d62728` — **no usan paleta institucional**; daltonismo no considerado. | Todos | 🟡 Media | Migrar a paleta institucional: verde #176B50 (central), amarillo #E5B94B (bajo), rojo #C94C4C (alto); verificar contraste. | `streamlit_app.py:1086-1090, 1192-1196, 1323-1327` |

---

### F. TABLAS

| # | Elemento | Problema | Tamaño | Gravedad | Solución propuesta | Archivo |
|---|----------|----------|--------|----------|-------------------|---------|
| F1 | **Tabla priorización: 12 columnas** | `st.dataframe(use_container_width=True)` → **scroll horizontal obligatorio** en móvil; columnas importantes (IPR, RANGO) pueden quedar fuera de vista. | ≤ 768px | 🔴 **Crítica** | Definir `column_order` prioritario: `["RANGO", "IPR", "MUNICIPIO", "DPTO", "CASOS_REALES", "PROY_2030", "CONFIABILIDAD"]`; ocultar `DIVIPOLA`, `RURAL`, `INDIGENA`, `CASOS_PRED` en móvil (toggle "Mostrar todo"). | `streamlit_app.py:652-756` |
| F2 | Tabla métricas modelos: 16 columnas | Igual problema; filtros frecuencia/nivel ayudan pero **tabla resultante sigue ancha**. | ≤ 768px | 🟠 Alta | En móvil: vista "Tarjetas por modelo" (una fila = una tarjeta vertical con métricas clave); tabla solo en desktop/tablet. | `streamlit_app.py:1411-1535` |
| F3 | Sin paginación nativa visible | `st.dataframe` pagina internamente pero **controles de página** (flechas, página actual) **pequeños en táctil**. | ≤ 768px | 🟡 Media | CSS: `.stDataFrame .stPagination button { min-height: 44px; min-width: 44px; font-size: 1rem; }`. | `streamlit_app.py:17-98` (nuevo CSS) |
| F4 | Descarga CSV botón estándar | `st.download_button` label largo → **se trunca en móvil**; ancho fijo no responsive. | ≤ 480px | 🟢 Baja | `use_container_width=True` en botón; label corto "⬇ CSV" + tooltip. | `streamlit_app.py:758-763, 897-908, 1026-1037, 1123-1129, 1235-1241, 1341-1347, 1537-1545, 1614-1623` |
| F5 | Tabla proyección nacional (expander) | `tabla_escenarios` pivot → **columnas BAJO/CENTRAL/ALTO + IC80** → 7+ columnas; en móvil ilegible. | ≤ 768px | 🟡 Media | En móvil: mostrar solo escenario central + IC80; toggle "Ver todos los escenarios". | `streamlit_app.py:1123-1129, 1235-1241, 1341-1347` |

---

### G. METODOLOGÍA Y TEXTOS

| # | Elemento | Problema | Tamaño | Gravedad | Solución propuesta | Archivo |
|---|----------|----------|--------|----------|-------------------|---------|
| G1 | **Texto inventado (C1, C2, C3 auditoría integral)** | Pestaña Metodología menciona modelos inexistentes (GRU, SARIMA, Ensamble LGBXGB) y TASA_100K inexistente — **violación integridad científica**. | Todos | 🔴 **Crítica** (ya documentada) | Reescribir con solo 3 modelos reales; corregir modelo semanal; quitar TASA_100K. | `streamlit_app.py:1636-1793` |
| G2 | Párrafos anchos sin `max-width` | Markdown en tab Metodología → **líneas de > 80 caracteres** en desktop; en móvil se ajustan pero **tamaño de fuente base 1rem** puede ser pequeño para lectura prolongada. | ≤ 480px | 🟠 Alta | CSS: `.stMarkdown p { max-width: 100%; line-height: 1.6; font-size: clamp(0.95rem, 2.5vw, 1.05rem); }`; añadir `text-align: justify` opcional. | `streamlit_app.py:17-98` (nuevo CSS) |
| G3 | Advertencias (`st.warning`) apiladas | 6 `st.warning` consecutivos → **muro de cajas amarillas**; en móvil ocupan mucho scroll vertical; no son colapsables. | ≤ 768px | 🟠 Alta | Unificar en un `st.expander("⚠ Limitaciones principales", expanded=False)` con lista numerada; mantener 1 `st.warning` resumen visible. | `streamlit_app.py:1725-1775` |
| G4 | Falta glosario / tooltips en términos técnicos | "IPR", "WMAPE", "encogimiento", "amortiguación" — **sin definición contextual** en UI. | Todos | 🟡 Media | Añadir `st.tooltip` o icono `ⓘ` con `st.popover` (Streamlit 1.32+) definiendo cada término. | `streamlit_app.py` (nuevo componente) |

---

## PLAN DE CORRECCIÓN POR ETAPAS (MOBILE-FIRST)

| Etapa | Enfoque | Archivos | Entregable | Validación |
|-------|---------|----------|------------|------------|
| **M1. Críticos móviles + Integridad** | Corregir A2, B1, D1, D2, F1 + C1/C2/C3 (integridad) | `streamlit_app.py`, `.streamlit/config.toml` (nuevo) | App usable en 320px; texto honesto; mapa legible; tabla priorizable. | Checklist 4 críticos móviles + 3 críticos integridad ✅ |
| **M2. Sidebar y filtros móviles** | B2, B3, B4, B5, B6, B7 | `streamlit_app.py`, `app/filters.py` (nuevo) | Sidebar colapsable; selectores táctiles; reset; chips activos. | Navegación fluida en 375px sin zoom. |
| **M3. Mapas y gráficas táctiles** | D3, D4, D5, D6, E1, E2, E3, E4, E5, E6 | `streamlit_app.py`, `app/maps.py`, `app/charts.py` (nuevos) | Mapas con leyenda, tooltips tap, altura responsive; gráficas con ejes legibles, paleta institucional. | Zero horizontal scroll; pinch-zoom funciona; colores accesibles. |
| **M4. Tablas y datos móviles** | F2, F3, F4, F5, C2, C3 | `streamlit_app.py`, `app/components/tables.py` (nuevo) | Vistas tarjeta/tabla toggle; paginación táctil; descargas accesibles. | Top-15 municipios legible en 320px sin scroll horizontal. |
| **M5. Identidad visual + textos** | A1, A3, A5, A6, C1, G2, G3, G4 | `.streamlit/theme.toml`, `app/styles.css`, `streamlit_app.py` | Paleta #176B50 aplicada; tipografía fluida; warnings colapsables; glosario. | Contraste AA; Lighthouse > 90 accesibilidad. |
| **M6. Arquitectura modular + pruebas** | M1–M5 auditoría integral (refactor) | `app/` (nueva estructura), `streamlit_app.py` < 200 líneas | Código mantenible; tests Playwright (si se instala); CI básico. | `git diff` limpio; `streamlit run` < 3s cold start. |

---

## CAPACIDAD DE IMPLEMENTACIÓN

**Sí, soy capaz de hacer los cambios.** 

### Lo que puedo hacer (dentro de restricciones AGENTES.md):
- ✅ Modificar `streamlit_app.py` (CSS, layout, componentes, textos)
- ✅ Crear archivos nuevos: `.streamlit/theme.toml`, `app/*.py` módulos, `app/styles.css`
- ✅ Refactorizar a arquitectura modular (Etapa 2 AGENTS.md)
- ✅ Aplicar paleta institucional en Plotly/Streamlit
- ✅ Corregir textos que inventan modelos/datos (C1, C2, C3)
- ✅ Mejorar responsive con CSS media queries y configuración Plotly
- ✅ Añadir `st.cache_data` donde falte, `st.session_state` para filtros
- ✅ Actualizar `PROGRESS_NUTRIPREDICT.md` y `MOBILE_AUDIT_NUTRIPREDICT.md` tras cada etapa
- ✅ Ejecutar app y verificar sintaxis/imports/carga

### Lo que NO haré (restricciones AGENTES.md §2, §12):
- ❌ Modificar datos originales (`data/`, `outputs/`)
- ❌ Cambiar fórmulas IPR, proyecciones, modelos, validaciones
- ❌ Eliminar funcionalidades existentes para "simplificar" móvil
- ❌ Inventar métricas, indicadores o fuentes
- ❌ Hacer commits/push sin autorización
- ❌ Instalar dependencias pesadas sin justificar (Playwright solo si autorizado para tests visuales)

### Requisitos para empezar:
1. **Autorización** para corregir C1–C3 (integridad) + M1 (críticos móviles).
2. **Confirmación** de rama de trabajo: ¿creo `feature/mobile-audit-fixes` desde `main`?
3. **Decisión** sobre `TASA_100K`: ¿quitar de tabla priorización o mostrar "No disponible" con nota?
4. **Preferencia** sidebar: ¿`initial_sidebar_state="collapsed"` + botón "Filtros" en header, o mantener "auto" con CSS para móvil?

---

## PRÓXIMO PASO

**Esperando tu autorización para iniciar Etapa M1** (críticos móviles + integridad científica). 

Una vez autorizado:
1. Crear rama `feature/mobile-audit-fixes`.
2. Commit de respaldo estado actual.
3. Implementar correcciones C1, C2, C3, A2, B1, D1, D2, F1.
4. Actualizar `PROGRESS_NUTRIPREDICT.md` con sección "ETAPA M1".
5. Presentar `git diff` y resultados de prueba local.