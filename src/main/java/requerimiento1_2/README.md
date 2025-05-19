# Requerimiento 1 y 2: Extracción y Deduplificación de Artículos

## Descripción

Este paquete está diseñado para:
- **Requerimiento 1:** Extraer datos de artículos científicos de diferentes fuentes (por ejemplo: Springer, ScienceDirect) usando web scraping automatizado.
- **Requerimiento 2:** Unificar los resultados, eliminar duplicados y generar un archivo único en formato `.bib` con todos los artículos recopilados.

## Flujo de trabajo

1. **Scraping:** Se automatiza la búsqueda y descarga de metadatos (título, autores, resumen, año, journal, etc.) usando scripts personalizados por fuente.
2. **Unificación:** Se combinan los resultados extraídos de todas las fuentes en una lista única.
3. **Eliminación de duplicados:** Se implementan heurísticas (por ejemplo, comparar títulos normalizados y años) para filtrar artículos repetidos.
4. **Exportación:** Los resultados únicos se guardan en el archivo `resultados_unicos.bib` en formato BibTeX.

# Clases y paquetes 

**Paquetes**
- exportacion
- extractores
- util

**Clases**
- exportadores: Inluye los metodos para construir los archivos .ris y .bib
- extractores:  Cuenta con las funciones para obtener la información de las bases de datos
- utils: cuenta con metodos usados en varias ocasiones

## Ejecución

1. Instala las dependencias necesarias (`selenium`, `pandas`, etc.).
2. Ejecuta los scripts de scraping para cada fuente.
3. Ejecuta el script de deduplicación.
4. Revisa el archivo `resultados_unicos.bib` en esta misma carpeta.

## Observaciones

- El archivo `.bib` generado es la base para los análisis posteriores (frecuencias, similitud, etc.).
- Si necesitas modificar criterios de duplicidad, edita el script de deduplicación.

---