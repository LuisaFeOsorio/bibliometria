#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Módulo para el análisis de frecuencia de variables por categorías en resúmenes de artículos,
nube de palabras por categoría y total, y grafo de co-ocurrencia de palabras clave.

Uso:
    from analisis_variables_resumenes import main
    main("ruta/al/archivo.bib", "ruta/carpeta_salida")
"""

import os
import re
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx

# -----------------------------
# 1. DEFINICIÓN DE CATEGORÍAS Y VARIABLES (con sinónimos)
# -----------------------------

CATEGORIAS = {
    "Habilidades": [
        "Abstracción-Abstraction", "Algoritmo-Algorithm", "Pensamiento algorítmico-Algorithmic thinking",
        "Codificación-Coding", "Colaboración-Collaboration", "Cooperación-Cooperation", "Creatividad-Creativity",
        "Pensamiento crítico-Critical thinking", "Depuración-Debug", "Descomposición-Decomposition", "Evaluación-Evaluation",
        "Generalización-Generalization", "Lógica-Logic", "Pensamiento lógico-Logical thinking", "Modularidad-Modularity",
        "Reconocimiento de patrones-Patterns recognition", "Resolución de problemas-Problem solving", "Programación-Programming"
    ],
    "Conceptos Computacionales": [
        "Condicionales-Conditionals", "Estructuras de control-Control structures", "Direcciones-Directions",
        "Eventos-Events", "Funciones-Funtions", "Bucles-Loops", "Estructura modular-Modular structure",
        "Paralelismo-Parallelism", "Secuencias-Sequences", "Software/hardware", "Variables"
    ],
    "Actitudes": [
        "Emocional-Emotional", "Compromiso-Engagement", "Motivación-Motivation", "Percepción-Perceptions",
        "Persistencia-Persistence", "Autoeficacia-Self-efficacy", "Autopercepción-Self-perceived"
    ],
    "Propiedades psicométricas": [
        "Teoría clásica de los tests-Classical Test Theory-CTT",
        "Análisis factorial confirmatorio-Confirmatory Factor Analysis-CFA",
        "Análisis factorial exploratorio-Exploratory Factor Analysis-EFA",
        "Teoría de respuesta al ítem-Item Response Theory-IRT", "Confiabilidad-Reliability",
        "Modelo de ecuaciones estructurales-Structural Equation Model-SEM", "Validez-Validity"
    ],
    "Herramienta de evaluación": [
        "BCTt-Beginners Computational Thinking test", "ESCAS-Coding Attitudes Survey",
        "Collaborative Computing Observation Instrument",
        "cCTt-Competent Computational Thinking test", "CTST-Computational thinking skills test",
        "Computational concepts", "CTA-CES-Computational Thinking Assessment for Chinese Elementary Students",
        "CTC-Computational Thinking Challenge", "CTLS-Computational Thinking Levels Scale",
        "CTS-Computational Thinking Scale", "CTS-Computational Thinking Skill Levels Scale",
        "CTt-Computational Thinking Test", "Computational Thinking Test",
        "Computational Thinking Test for Elementary School Students",
        "CTtLP-Computational Thinking Test for Lower Primary",
        "Computational thinking-skill tasks on numbers and arithmetic",
        "CAPCT-Computerized Adaptive Programming Concepts Test",
        "CTS-CT Scale", "ESCAS-Elementary Student Coding Attitudes Survey",
        "General self-efficacy scale", "ICT competency test", "Instrument of computational identity",
        "KBIT fluid intelligence subtest",
        "Mastery of computational concepts Test and an Algorithmic Test",
        "Multidimensional 21st Century Skills Scale", "Self-efficacy scale",
        "STEM learning attitude scale", "The computational thinking scale"
    ],
    "Diseño de investigación": [
        "No experimental", "Experimental", "Investigación longitudinal-Longitudinal research",
        "Métodos mixtos-Mixed methods", "Post-test", "Pre-test", "Cuasi-experimentos-Quasi-experiments"
    ],
    "Nivel de escolaridad": [
        "Educación primaria-Primary school-Primary education-Elementary school",
        "Educación infantil-Early childhood education-Kindergarten-Preschool",
        "Educación secundaria-Secondary school-Secondary education",
        "Educación superior-University-College-higher education",
        "Educación media-high school", "Educación básica-Lower primary"
    ],
    "Medio": [
        "Programación en bloques-Block programming", "Aplicación móvil-Mobile application",
        "Programación en pareja-Pair programming", "Actividades con tecnología-Plugged activities",
        "Programación-Programming", "Robótica-Robotics", "Hoja de cálculo-Spreadsheet",
        "STEM", "Actividades sin tecnología-Unplugged activities"
    ],
    "Estrategia": [
        "Mapa mental auto-construido-Construct-by-self mind mapping",
        "Mapa mental en andamiaje-Construct-on-scaffold mind mapping", "Aprendizaje basado en diseño-Design-based learning",
        "Enfoque de diseño centrado en la evidencia-Evidence-centred design approach", "Gamificación-Gamification",
        "Pedagogía de ingeniería inversa-Reverse engineering pedagogy",
        "Aprendizaje mejorado con tecnología-Technology-enhanced learning",
        "Aprendizaje colaborativo-Collaborative learning", "Aprendizaje cooperativo-Cooperative learning",
        "Clase invertida-Flipped classroom", "Aprendizaje basado en juegos-Game-based learning",
        "Aprendizaje basado en indagación-Inquiry-based learning", "Aprendizaje personalizado-Personalized learning",
        "Aprendizaje basado en problemas-Problem-based  learning",
        "Aprendizaje basado en proyectos-Project-based learning",
        "Diseño universal para el aprendizaje-Universal design for learning"
    ],
    "Herramienta": [
        "Alice", "Arduino", "Scratch", "ScratchJr", "Blockly Games", "Code.org", "Codecombat",
        "CSUnplugged", "Robot Turtles", "Hello Ruby", "Kodable", "LightbotJr", "KIBO robots",
        "BEE BOT", "CUBETTO", "Minecraft", "Agent Sheets", "Mimo", "Py– Learn", "SpaceChem"
    ]
}

# -----------------------------
# 2. UTILIDADES PARA SINÓNIMOS Y MAPEO
# -----------------------------

def construir_mapa_sinonimos(categorias):
    """
    Construye un diccionario que mapea cada sinónimo a su variable principal.
    """
    mapa = {}
    for categoria, variables in categorias.items():
        for variable in variables:
            sinonimos = variable.split('-')
            principal = sinonimos[0].strip().lower()
            for sin in sinonimos:
                mapa[sin.strip().lower()] = principal
    return mapa

def variables_por_categoria(categorias):
    """
    Devuelve un diccionario {categoria: [lista de variables principales]}
    """
    resultado = {}
    for cat, vars in categorias.items():
        resultado[cat] = [v.split('-')[0].strip().lower() for v in vars]
    return resultado

# -----------------------------
# 3. FUNCIONES DE ANÁLISIS DE FRECUENCIA
# -----------------------------

def contar_frecuencias(abstracts, categorias):
    """
    Cuenta la frecuencia de aparición de cada variable (unificando sinónimos) por categoría.
    Devuelve un diccionario por categoría y un contador total.
    """
    mapa_sinonimos = construir_mapa_sinonimos(categorias)
    freq_por_categoria = {cat: Counter() for cat in categorias}
    freq_total = Counter()
    for abstract in abstracts:
        abstract_low = abstract.lower()
        for cat, vars in categorias.items():
            for var in vars:
                principal = var.split('-')[0].strip().lower()
                for sinonimo in var.split('-'):
                    patron = r'\b' + re.escape(sinonimo.strip().lower()) + r'\b'
                    ocurrencias = len(re.findall(patron, abstract_low))
                    if ocurrencias > 0:
                        freq_por_categoria[cat][principal] += ocurrencias
                        freq_total[principal] += ocurrencias
    return freq_por_categoria, freq_total

def imprimir_frecuencias(freq_por_categoria):
    """
    Imprime las frecuencias por categoría en la terminal.
    """
    print("\n===== Frecuencias por Categoría =====")
    for cat, counter in freq_por_categoria.items():
        print(f"\nCategoría: {cat}")
        for var, count in counter.most_common():
            print(f"  {var}: {count}")

# -----------------------------
# 4. NUBE DE PALABRAS
# -----------------------------

def generar_nube_palabras(counter, titulo, filename):
    """
    Genera y guarda una nube de palabras desde un Counter.
    """
    if not counter:
        print(f"[AVISO] No hay palabras para la nube de: {titulo}")
        return
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(counter)
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"[INFO] Nube de palabras guardada: {filename}")

# -----------------------------
# 5. GRAFO DE CO-OCURRENCIA
# -----------------------------

def construir_grafo_coocurrencia(abstracts, categorias):
    """
    Construye un grafo de co-ocurrencia de variables en los resúmenes.
    """
    variables = list({v.split('-')[0].strip().lower() for l in categorias.values() for v in l})
    pares = Counter()
    for abstract in abstracts:
        encontrados = set()
        texto = abstract.lower()
        for var in variables:
            patron = r'\b' + re.escape(var) + r'\b'
            if re.search(patron, texto):
                encontrados.add(var)
        for v1 in encontrados:
            for v2 in encontrados:
                if v1 < v2:
                    pares[(v1, v2)] += 1
    G = nx.Graph()
    for (v1, v2), peso in pares.items():
        if peso > 0:
            G.add_edge(v1, v2, weight=peso)
    return G

def graficar_grafo_coocurrencia(G, filename):
    """
    Dibuja y guarda el grafo de co-ocurrencia.
    """
    if len(G) == 0:
        print("[AVISO] No hay co-ocurrencias para graficar.")
        return
    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(G, k=0.3)
    edges = G.edges()
    weights = [G[u][v]['weight'] for u,v in edges]
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1300)
    nx.draw_networkx_edges(G, pos, width=weights, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.title("Grafo de co-ocurrencia de palabras clave")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"[INFO] Grafo de co-ocurrencia guardado: {filename}")

# -----------------------------
# 6. LECTURA DE RESÚMENES DESDE .BIB
# -----------------------------

def cargar_resumenes_desde_bibtex(ruta_bib):
    """
    Carga los resúmenes desde un archivo .bib generado por tu scraper.
    Retorna una lista de strings.
    """
    resumenes = []
    with open(ruta_bib, "r", encoding="utf-8") as f:
        contenido = f.read()
    # Busca abstract = { ... }
    for match in re.finditer(r'abstract\s*=\s*\{(.+?)\}', contenido, re.DOTALL | re.IGNORECASE):
        resumen = match.group(1).replace('\n', ' ').strip()
        resumenes.append(resumen)
    return resumenes

# -----------------------------
# 7. FUNCIÓN PRINCIPAL DEL MÓDULO
# -----------------------------

def main(ruta_bibtex, carpeta_salida):
    """
    Ejecuta todo el análisis de frecuencia, nubes de palabras y grafo de co-ocurrencia.
    Guarda los resultados en la carpeta indicada y muestra los resultados en terminal.
    """
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    # 1. Extraer resúmenes
    resumenes = cargar_resumenes_desde_bibtex(ruta_bibtex)
    print(f"Se cargaron {len(resumenes)} resúmenes desde {ruta_bibtex}")
    # 2. Contar frecuencias
    freq_cat, freq_total = contar_frecuencias(resumenes, CATEGORIAS)
    imprimir_frecuencias(freq_cat)
    # 3. Nube de palabras por categoría y total
    for cat, counter in freq_cat.items():
        generar_nube_palabras(counter, f"Nube de palabras: {cat}", os.path.join(carpeta_salida, f"nube_{cat.replace(' ','_')}.png"))
    generar_nube_palabras(freq_total, "Nube de palabras global", os.path.join(carpeta_salida, "nube_total.png"))
    # 4. Grafo de co-ocurrencia global
    G = construir_grafo_coocurrencia(resumenes, CATEGORIAS)
    graficar_grafo_coocurrencia(G, os.path.join(carpeta_salida, "grafo_coocurrencia.png"))
    print(f"\n[FIN] Resultados guardados en la carpeta: {carpeta_salida}")

# Si quieres probar este módulo de forma independiente:
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Uso: python analisis_variables_resumenes.py archivo.bib carpeta_salida")
    else:
        main(sys.argv[1], sys.argv[2])