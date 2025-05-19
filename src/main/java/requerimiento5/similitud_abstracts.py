"""
Módulo para el análisis de similitud entre resúmenes de artículos.

Incluye:
- Similitud del coseno (TF-IDF)
- Similitud de Jaccard
- Clustering para agrupar artículos similares
- Visualización de matrices de similitud y reporte de agrupamientos

"""

import os
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

def cargar_resumenes_desde_bibtex(ruta_bib):
    """
    Lee títulos y resúmenes desde un archivo .bib.
    Retorna dos listas: titulos, resumenes.
    """
    resumenes = []
    titulos = []
    with open(ruta_bib, "r", encoding="utf-8") as f:
        contenido = f.read()
    # Busca title = { ... } y abstract = { ... }
    for match in re.finditer(r'title\s*=\s*\{(.+?)\}.*?abstract\s*=\s*\{(.+?)\}', contenido, re.DOTALL | re.IGNORECASE):
        titulo = match.group(1).replace('\n', ' ').strip()
        resumen = match.group(2).replace('\n', ' ').strip()
        titulos.append(titulo)
        resumenes.append(resumen)
    return titulos, resumenes

def matriz_similitud_coseno(resumenes):
    """
    Calcula la matriz de similitud del coseno usando representación TF-IDF.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(resumenes)
    sim_matrix = cosine_similarity(X)
    return sim_matrix

def matriz_similitud_jaccard(resumenes):
    """
    Calcula la matriz de similitud Jaccard a partir de conjuntos de palabras.
    """
    sets = [set(r.lower().split()) for r in resumenes]
    N = len(sets)
    sim_matrix = np.zeros((N, N))
    for i in range(N):
        for j in range(i, N):
            inter = len(sets[i] & sets[j])
            union = len(sets[i] | sets[j])
            sim = inter / union if union > 0 else 0
            sim_matrix[i, j] = sim_matrix[j, i] = sim
    return sim_matrix

def agrupar_por_similitud(sim_matrix, titulos, umbral=0.5):
    """
    Agrupa artículos usando clustering jerárquico según una matriz de similitud y un umbral.
    Devuelve un diccionario {número de grupo: [lista de títulos]}
    """
    dist_matrix = 1 - sim_matrix
    clustering = AgglomerativeClustering(
        n_clusters=None, distance_threshold=1-umbral, metric="precomputed", linkage="average")
    etiquetas = clustering.fit_predict(dist_matrix)
    grupos = defaultdict(list)
    for idx, grupo in enumerate(etiquetas):
        grupos[grupo].append(titulos[idx])
    return grupos
def visualizar_similitud(sim_matrix, titulos, metodo, carpeta_salida):
    """
    Genera y guarda una matriz de calor de similitud.
    """
    plt.figure(figsize=(12,10))
    sns.heatmap(sim_matrix, xticklabels=False, yticklabels=False, cmap='viridis')
    plt.title(f'Matriz de similitud - {metodo}')
    plt.tight_layout()
    archivo = os.path.join(carpeta_salida, f"matriz_similitud_{metodo}.png")
    plt.savefig(archivo)
    plt.close()
    print(f"[INFO] Matriz de similitud guardada: {archivo}")

def guardar_grupos(grupos, metodo, carpeta_salida):
    """
    Guarda las agrupaciones en un archivo de texto.
    """
    ruta = os.path.join(carpeta_salida, f"grupos_similares_{metodo}.txt")
    with open(ruta, "w", encoding="utf-8") as f:
        for grupo, titulos in grupos.items():
            f.write(f"Grupo {grupo}:\n")
            for titulo in titulos:
                f.write(f"  - {titulo}\n")
            f.write("\n")
    print(f"[INFO] Grupos guardados: {ruta}")