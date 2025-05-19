# Requerimiento 3: Análisis de Variables y Palabras Clave en Resúmenes

Este paquete realiza un análisis de contenido sobre los resúmenes de los artículos extraídos previamente.

## Funcionalidades

- **Cálculo de la frecuencia de aparición** de variables agrupadas por categorías, considerando sinónimos.
- **Tablas de frecuencia** impresas en terminal por categoría.
- **Nube de palabras** por categoría y global, generadas automáticamente (sin plataformas externas).
- **Visualización de grafo de co-ocurrencia** (co-word network) de variables presentes en los resúmenes.

## Flujo de trabajo

1. Lee el archivo `resultados_unicos.bib` de la carpeta `../requerimiento1_2/`.
2. Extrae los campos de resumen (`abstract`) de cada artículo.
3. Analiza la frecuencia de aparición de variables (considerando sinónimos) por categoría.
4. Genera visualizaciones y archivos de salida en la carpeta `salida/`.

## Estructura

- `analisis_variables_resumenes.py`: módulo principal con toda la lógica.
- `analisis_variables.py`: script de entrada/salida.
- `salida/`: carpeta donde se guardan los gráficos y resultados.

## Ejecución

1. Instala las dependencias:
   ```
   pip install matplotlib wordcloud networkx
   ```
2. Ejecuta:
   ```
   cd requerimiento3
   python analisis_variables.py
   ```
3. Consulta los archivos y gráficos generados en `salida/`.

## Notas

- El análisis es totalmente reproducible en Python y no requiere herramientas externas.
- El flujo está pensado para ser modular y fácil de integrar con los otros requerimientos.

---