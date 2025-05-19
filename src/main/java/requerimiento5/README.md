# Requerimiento 5: Similitud y Agrupamiento de Abstracts

Este módulo analiza la similitud entre los resúmenes de artículos de investigación utilizando dos técnicas, y agrupa artículos similares.

## Técnicas implementadas

**1. Similitud del coseno (TF-IDF)**
- Los resúmenes se representan como vectores en un espacio semántico (TF-IDF).
- La similitud se mide por el coseno del ángulo entre estos vectores.
- Es una técnica ampliamente utilizada en recuperación de información y análisis de textos académicos.

**2. Similitud de Jaccard**
- Se basa en el solapamiento de conjuntos de palabras únicas entre resúmenes.
- Es una métrica clásica y sencilla para medir la similitud entre textos cortos.

Ambas técnicas son válidas y reconocidas en la literatura científica para comparar y agrupar textos.

## Agrupamiento

Se utiliza clustering jerárquico ("Agglomerative Clustering") sobre la matriz de similitud para obtener grupos de artículos similares.

## Estructura

- `similitud_abstracts.py`: módulo con toda la lógica de similitud y agrupamiento.
- `analisis_similitud.py`: script principal para ejecutar el análisis.
- `salida/`: carpeta donde se guardan las matrices de similitud y los archivos de grupos.

## Ejecución

1. Asegúrate de tener el archivo `resultados_unicos.bib` en `../requerimiento1_2/`.
2. Instala las dependencias:
   ```
   pip install numpy pandas scikit-learn matplotlib seaborn
   ```
3. Ejecuta desde la terminal:
   ```
   cd requerimiento5
   python analisis_similitud.py
   ```
4. Verifica los resultados en la carpeta `salida/`.

## Fundamento

La similitud del coseno y la de Jaccard son técnicas bien documentadas y ampliamente usadas para comparar documentos y agrupar textos. El uso de clustering jerárquico permite encontrar grupos de artículos con alta similitud de manera objetiva.

---