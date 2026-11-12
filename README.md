# NUTRIPREDICT Colombia 2030

Dashboard interactivo para explorar resultados de modelamiento de desnutrición aguda infantil en Colombia, basado en notificaciones del evento 113 de SIVIGILA.

## Qué muestra

- Mapa departamental de la proyección central 2030.
- Mapa municipal del Índice de Priorización Relativa (IPR).
- Filtros por departamento y nivel territorial.
- Resultados municipales de casos reales, predichos y proyecciones.
- Indicadores de ruralidad, población indígena y confiabilidad.

## Archivos principales

- `app/streamlit_app.py`: aplicación Streamlit.
- `data/resultados_nutripredict.json`: resultados municipales.
- `data/panel_mensual.parquet`: panel mensual por municipio.
- `data/panel_semanal.parquet`: panel semanal por municipio.
- `data/col_departamentos_inset_nacional.geojson`: límites departamentales.
- `data/col_municipios_inset_nacional.geojson`: límites municipales.

## Ejecución local

```bash
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
```

## Notas metodológicas

Las cifras corresponden a casos notificados, no a incidencia real ni riesgo individual. El IPR es una prioridad relativa entre municipios y no debe interpretarse como un diagnóstico individual.

Cartografía: Marco Geoestadístico Nacional 2025, DANE.  
Simplificación: github.com/ytolosa/mapas-colombia, CC BY 4.0.