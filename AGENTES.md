# AGENTS.md — NUTRIPREDICT COLOMBIA 2030

## 1. IDENTIDAD Y OBJETIVO DEL PROYECTO

NUTRIPREDICT Colombia 2030 es un proyecto de análisis, visualización y predicción relacionado con la desnutrición aguda infantil en Colombia.

El proyecto utiliza Python y Streamlit y contiene datos, procesos analíticos, visualizaciones, componentes geográficos e indicadores de priorización territorial.

El objetivo de los agentes es mantener, mejorar y profesionalizar el proyecto sin comprometer su integridad científica, estadística, epidemiológica ni técnica.

La prioridad es conseguir una aplicación institucional, científica, moderna, intuitiva y confiable.

## 2. REGLA INNEGOCIABLE: PROTEGER LA INTEGRIDAD CIENTÍFICA

Está prohibido modificar sin autorización expresa del usuario:

- Datos originales.
- Fuentes de información.
- Variables analíticas.
- Fórmulas matemáticas y estadísticas.
- Cálculos del IPR.
- Resultados estadísticos.
- Predicciones y proyecciones.
- Parámetros de modelos predictivos.
- Procesos de entrenamiento y validación.
- Procesamiento y transformación de datos.
- Interpretaciones epidemiológicas.
- Asociaciones entre municipios, departamentos y datos geográficos.

No inventar:
- Datos.
- Indicadores.
- Resultados.
- Fuentes.
- Referencias.
- Fórmulas.
- Variables.
- Métricas de validación.
- Funcionalidades que aparenten estar respaldadas por información inexistente.

Diferenciar siempre los casos notificados, las predicciones y las proyecciones.

El IPR debe conservar su definición documentada. No debe presentarse como diagnóstico individual ni como probabilidad clínica si la metodología no lo establece.

Las proyecciones deben presentarse como estimaciones sujetas a incertidumbre.

Si se detecta un error científico o metodológico, documentarlo y solicitar autorización antes de corregirlo.

Se permiten cambios exclusivamente visuales que no alteren los datos, cálculos, resultados ni su interpretación.

## 3. PROTOCOLO OBLIGATORIO ANTES DE MODIFICAR EL PROYECTO

Antes de realizar cualquier modificación:

1. Leer este archivo completo.
2. Leer el README.md.
3. Inspeccionar la estructura del repositorio.
4. Identificar el punto de entrada de Streamlit.
5. Identificar los módulos de procesamiento de datos.
6. Identificar los modelos predictivos.
7. Identificar los cálculos del IPR.
8. Identificar las páginas, gráficas, mapas y filtros.
9. Revisar los archivos de dependencias.
10. Ejecutar git status y revisar los cambios existentes.

No modificar archivos hasta comprender su función.

No asumir que un archivo está obsoleto por su nombre o ubicación.

No eliminar código simplemente porque parece innecesario.

## 4. PROTECCIÓN DE GIT Y DEL TRABAJO EXISTENTE

El trabajo del usuario tiene prioridad sobre cualquier modificación del agente.

Reglas:

- No sobrescribir cambios del usuario.
- No ejecutar git reset --hard.
- No ejecutar git clean -fd.
- No descartar modificaciones con git checkout o git restore sin autorización.
- No eliminar ramas.
- No realizar commits sin autorización.
- No publicar cambios en GitHub sin autorización.
- No cambiar configuraciones de producción sin autorización.

Antes de iniciar una etapa, revisar el estado de Git.

Si no existen modificaciones pendientes y el entorno lo permite, recomendar un commit de respaldo o crear una rama de trabajo.

Si hay cambios sin guardar, conservarlos y trabajar alrededor de ellos.

Al finalizar cada etapa, revisar git diff y explicar los cambios.

## 5. PROTOCOLO PARA CAMBIOS AUTOMÁTICOS DE MODELO DE IA

FreeLLMAPI puede cambiar automáticamente de proveedor o modelo cuando se alcanza un límite de uso.

Todos los agentes deben poder continuar el trabajo de forma segura.

Cuando un nuevo modelo tome el control:

1. Leer AGENTS.md.
2. Leer PROGRESS_NUTRIPREDICT.md, si existe.
3. Revisar git status.
4. Revisar git diff.
5. Inspeccionar los archivos modificados.
6. Identificar las tareas completadas.
7. Identificar las tareas pendientes.
8. Comprobar si existen cambios incompletos.
9. Continuar desde el último estado estable.

Está prohibido:

- Reiniciar el proyecto desde cero.
- Repetir modificaciones ya realizadas.
- Sobrescribir código funcional del agente anterior sin justificación.
- Revertir cambios válidos.
- Suponer que el modelo anterior no realizó ninguna tarea.
- Ejecutar nuevamente procesos costosos sin comprobar su necesidad.

Si no es posible determinar el estado del proyecto, detenerse y solicitar aclaraciones.

## 6. REGISTRO DE CONTINUIDAD

Mantener actualizado el archivo PROGRESS_NUTRIPREDICT.md.

Debe incluir:

- Etapa actual.
- Objetivo de la etapa.
- Tareas completadas.
- Tareas pendientes.
- Archivos modificados.
- Descripción de los cambios.
- Pruebas ejecutadas.
- Errores detectados.
- Problemas pendientes.
- Advertencias sobre posibles efectos científicos.
- Último punto estable de trabajo.

Actualizar el registro al terminar cada etapa y antes de interrumpir una tarea prolongada.

El registro debe ser claro y suficiente para que otro modelo pueda continuar sin depender de la memoria del anterior.

## 7. IDENTIDAD VISUAL

La aplicación debe tener una identidad visual institucional, científica y profesional.

Paleta de referencia:

- Verde institucional: #176B50
- Verde profundo: #164C3B
- Verde suave: #EAF3ED
- Blanco: #FFFFFF
- Fondo general: #F3F6F4
- Gris secundario: #64746B
- Amarillo de alerta: #E5B94B
- Rojo de alerta: #C94C4C

Criterios:

- Diseño limpio y moderno.
- Jerarquía visual consistente.
- Tipografía legible.
- Espaciado equilibrado.
- Tarjetas de indicadores ordenadas.
- Navegación intuitiva.
- Contraste adecuado.
- Diseño adaptable a diferentes pantallas.
- Uso moderado del color.
- Coherencia entre todas las páginas.

Evitar diseños recargados, gradientes excesivos, animaciones innecesarias y elementos decorativos que distraigan de la información.

## 8. ARQUITECTURA Y NAVEGACIÓN

Mejorar la organización de las secciones existentes. Considerar, cuando sea compatible con la arquitectura actual:

1. Inicio y resumen nacional.
2. Panorama territorial.
3. Análisis departamental.
4. Análisis municipal.
5. Proyecciones hacia 2030.
6. Priorización territorial e IPR.
7. Metodología y alcance científico.

No eliminar funcionalidades existentes para conseguir esta estructura.

No duplicar páginas ni crear secciones vacías.

Cada sección debe tener una finalidad clara y aportar información útil.

## 9. GRÁFICAS Y VISUALIZACIONES

Mejorar las gráficas existentes para que sean claras, profesionales y fáciles de interpretar.

Cuando los datos existentes lo permitan, utilizar:

- Tendencias temporales.
- Comparaciones territoriales.
- Casos observados frente a predichos.
- Proyecciones.
- Rankings municipales.
- Indicadores de priorización.
- Visualizaciones de incertidumbre respaldadas por el modelo.

Toda gráfica debe tener títulos descriptivos, ejes identificados, unidades, leyendas y etiquetas legibles.

No modificar valores, escalas ni resultados para mejorar artificialmente la presentación.

No crear gráficas que dependan de datos inexistentes.

## 10. MAPAS GEOGRÁFICOS

Revisar los mapas existentes y mejorar:

- Límites territoriales.
- Colores por indicador.
- Leyendas.
- Tooltips.
- Zoom.
- Navegación.
- Filtros departamentales y municipales.
- Asociación entre geometrías y datos.
- Lectura de territorios prioritarios.

No inventar geometrías, coordenadas ni correspondencias territoriales.

Verificar la compatibilidad entre las fuentes cartográficas y los datos utilizados.

Si hay inconsistencias, documentarlas antes de corregirlas.

## 11. FILTROS E INTERACTIVIDAD

Mejorar los filtros existentes para facilitar el análisis.

Considerar:

- Departamento.
- Municipio.
- Periodo temporal.
- Indicadores disponibles.
- Restablecimiento de filtros.
- Mensajes de ausencia de resultados.

Comprobar que mapas, tablas y gráficas respondan coherentemente a los filtros.

Los filtros no deben alterar los datos originales ni las fórmulas.

## 12. METODOLOGÍA Y TRANSPARENCIA

La aplicación debe explicar con claridad los elementos metodológicos respaldados por el proyecto:

- Objetivo.
- Fuentes de información.
- Preparación de datos.
- Metodología predictiva.
- Definición del IPR.
- Interpretación de indicadores.
- Limitaciones.
- Alcance de las proyecciones.
- Referencias.

No inventar explicaciones metodológicas.

Mantener visibles las limitaciones y advertencias necesarias para interpretar correctamente los resultados.

## 13. CALIDAD DEL CÓDIGO

- Mantener Python y Streamlit, salvo autorización expresa.
- Respetar la arquitectura existente.
- Reutilizar componentes cuando sea razonable.
- Evitar duplicación de código.
- Mantener nombres y convenciones coherentes.
- Manejar errores de forma controlada.
- No instalar dependencias innecesarias.
- No introducir incompatibilidades con el despliegue.
- No guardar credenciales ni API keys en el repositorio.
- No exponer información sensible en registros.
- No modificar archivos de configuración sin justificación.

## 14. PRUEBAS OBLIGATORIAS

Después de cada etapa, ejecutar las pruebas disponibles y apropiadas.

Comprobar:

- Sintaxis de Python.
- Imports.
- Dependencias.
- Carga de la aplicación.
- Navegación.
- Filtros.
- Gráficas.
- Mapas.
- Lectura de datos.
- Funcionamiento de los módulos afectados.

Si una prueba no puede ejecutarse, informar la razón. No afirmar que algo funciona si no se ha comprobado.

No modificar datos reales para hacer que una prueba pase.

## 15. FLUJO DE TRABAJO

Trabajar por etapas:

ETAPA 1. Auditoría del proyecto.

ETAPA 2. Plan de rediseño y arquitectura visual.

ETAPA 3. Identidad visual y estilos.

ETAPA 4. Gráficas y visualizaciones.

ETAPA 5. Mapas geográficos.

ETAPA 6. Navegación y filtros.

ETAPA 7. Metodología y transparencia.

ETAPA 8. Pruebas y auditoría final.

No realizar una transformación masiva de una sola vez.

Antes de una modificación importante, explicar su alcance y los archivos afectados.

Si la modificación puede alterar cálculos, datos o resultados, solicitar autorización.

## 16. INFORME AL USUARIO

Al terminar cada etapa, informar:

- Qué se hizo.
- Qué archivos se modificaron.
- Qué problemas se encontraron.
- Qué pruebas se realizaron.
- Qué resultados tuvieron las pruebas.
- Qué queda pendiente.

Diferenciar claramente entre cambios realizados, cambios propuestos y cambios que no pudieron verificarse.

## 17. OBJETIVO FINAL

Convertir NUTRIPREDICT Colombia 2030 en un dashboard profesional de salud pública, con identidad institucional, visualizaciones de alta calidad, mapas territoriales claros, navegación intuitiva, filtros funcionales y transparencia metodológica.

La integridad científica, estadística y epidemiológica tiene prioridad absoluta sobre cualquier mejora visual.

Comienza siempre leyendo estas instrucciones y revisando el estado actual del proyecto. No modifiques archivos antes de comprender su funcionamiento.

La continuidad del trabajo debe mantenerse incluso si FreeLLMAPI cambia de modelo o proveedor.