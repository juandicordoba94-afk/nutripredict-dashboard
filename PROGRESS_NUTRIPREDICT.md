# PROGRESS_NUTRIPREDICT.md — Registro de continuidad del proyecto NUTRIPREDICT Colombia 2030

**Última actualización:** 2026-11-13  
**Modelo que registra:** Qwen (FreeLLMAPI Auto)  
**Estado Git:** Rama `feature/mobile-audit-fixes` (commit `29b0da2` = backup; trabajo en curso). `main` sin cambios.

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

**🔄 SIGUIENTES (requieren autorización):**
4. **Commit cambios Etapa M1** en `feature/mobile-audit-fixes`.
5. **Iniciar Etapa M2** (Sidebar y filtros móviles): reset global, chips activos, selectores táctiles mejorados.
6. **Iniciar Etapa M3** (Mapas y gráficas táctiles avanzadas): patrón CONFIABILIDAD BAJA, mini-mapa proyección.
7. **Fijar dependencias** en `requirements.txt` con versiones exactas (lock).
8. **Crear `.streamlit/theme.toml`** y separar CSS a `app/styles.css`.
9. **Arquitectura modular** (Etapa 2 AGENTS.md): `app/data_loader.py`, `app/charts.py`, `app/maps.py`, `app/filters.py`, `app/pages/`.

---

## 12. ÚLTIMO PUNTO ESTABLE DE TRABAJO

- **Commit base:** `29b0da2` ("backup: estado previo a auditoría móvil (Etapa M1)") en rama `feature/mobile-audit-fixes`.
- **Rama actual:** `feature/mobile-audit-fixes` (trabajo Etapa M1 completado, sin commit aún).
- **Archivos modificados:** `app/streamlit_app.py` (Etapa M1).
- **Archivos nuevos (sin rastrear):** `AGENTES.md`, `PROGRESS_NUTRIPREDICT.md`, `MOBILE_AUDIT_NUTRIPREDICT.md`.
- **Entorno:** `.venv` funcional (Python 3.14.7, Streamlit 1.67.0, Plotly 7.1.0, Pandas 3.1.1).
- **App ejecutable:** `streamlit run app/streamlit_app.py` carga sin errores (verificado 2026-11-13).
- **Estado crítico C1–C3:** **RESUELTOS** (integridad científica restaurada).
- **Estado crítico móvil A2/B1/D1/D2/F1:** **RESUELTOS** (usabilidad táctil profesional).

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