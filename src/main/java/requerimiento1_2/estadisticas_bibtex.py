import re
import os
from collections import Counter, defaultdict
import pandas as pd
import matplotlib.pyplot as plt

DIRECTORIO_SALIDA = "estadisticas_salida"

def asegurar_directorio_salida():
    if not os.path.exists(DIRECTORIO_SALIDA):
        os.makedirs(DIRECTORIO_SALIDA)

def parsear_bibtex(ruta_archivo):
    entradas = []
    entrada = {}
    tipo_entrada = None
    clave = None
    patron_entrada = re.compile(r"^@(\w+)\{([^,]+),")
    patron_campo = re.compile(r"^\s*(\w+)\s*=\s*[\{|\"](.+?)[\}|\"]\s*,?\s*$")
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    for linea in lineas:
        m = patron_entrada.match(linea)
        if m:
            if entrada:
                entradas.append(entrada)
                entrada = {}
            tipo_entrada, clave = m.groups()
            entrada['tipo'] = tipo_entrada.lower()
            entrada['clave'] = clave
        else:
            m2 = patron_campo.match(linea)
            if m2:
                campo, valor = m2.groups()
                entrada[campo.lower()] = valor.strip()
        if linea.strip().endswith('}'):
            if entrada:
                entradas.append(entrada)
                entrada = {}
    if entrada and entrada not in entradas:
        entradas.append(entrada)
    entradas_finales = []
    for e in entradas:
        autores = e.get('author', '').replace('\n', ' ').split(' and ')
        autores = [a.strip() for a in autores if a.strip()]
        primer_autor = autores[0] if autores else 'Desconocido'
        titulo = e.get('title', 'Sin título')
        revista = e.get('journal', e.get('booktitle', 'Desconocido'))
        anio = e.get('year', 'Desconocido')
        tipobib = e.get('tipo', 'article')
        if tipobib in ('article', 'journal'):
            tipo = 'artículo'
        elif tipobib in ('inproceedings', 'conference'):
            tipo = 'conferencia'
        elif tipobib == 'book':
            tipo = 'libro'
        elif tipobib == 'incollection':
            tipo = 'capítulo de libro'
        else:
            tipo = tipobib
        editorial = e.get('publisher', 'Desconocido')
        entradas_finales.append({
            'clave': e.get('clave', ''),
            'autores': autores,
            'primer_autor': primer_autor,
            'titulo': titulo,
            'revista': revista,
            'anio': anio,
            'tipo': tipo,
            'editorial': editorial
        })
    return entradas_finales

def generar_estadisticas(entradas):
    estadisticas = {}
    todos_autores = [autor for entrada in entradas for autor in entrada['autores']]
    estadisticas['autores_destacados'] = Counter(todos_autores).most_common(15)
    anio_tipo_conteo = defaultdict(lambda: defaultdict(int))
    for entrada in entradas:
        anio_tipo_conteo[entrada['tipo']][entrada['anio']] += 1
    estadisticas['anio_por_tipo'] = anio_tipo_conteo
    estadisticas['distribucion_tipos'] = Counter([entrada['tipo'] for entrada in entradas])
    estadisticas['revistas_destacadas'] = Counter([entrada['revista'] for entrada in entradas]).most_common(15)
    estadisticas['editoriales_destacadas'] = Counter([entrada['editorial'] for entrada in entradas]).most_common(15)
    return estadisticas

def visualizar_estadisticas(estadisticas):
    # 1. Autores destacados
    if estadisticas['autores_destacados']:
        autores, cantidades = zip(*estadisticas['autores_destacados'])
        plt.figure(figsize=(10, 6))
        plt.barh(autores[::-1], cantidades[::-1])
        plt.title('Top 15 autores con más publicaciones')
        plt.xlabel('Número de publicaciones')
        plt.tight_layout()
        plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'autores_destacados.png'))
        plt.close()
    # 2. Publicaciones por año y tipo
    if estadisticas['anio_por_tipo']:
        df = pd.DataFrame(estadisticas['anio_por_tipo']).fillna(0).astype(int)
        df.T.plot(kind='bar', stacked=True, figsize=(12, 6))
        plt.title('Publicaciones por año y tipo')
        plt.ylabel('Número de publicaciones')
        plt.xlabel('Año')
        plt.legend(title='Tipo de producto')
        plt.tight_layout()
        plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'publicaciones_por_anio_tipo.png'))
        plt.close()
    # 3. Distribución de tipos
    if estadisticas['distribucion_tipos']:
        tipos, cantidades = zip(*estadisticas['distribucion_tipos'].items())
        plt.figure(figsize=(8, 8))
        plt.pie(cantidades, labels=tipos, autopct='%1.1f%%')
        plt.title('Distribución de tipos de productos')
        plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'distribucion_tipos.png'))
        plt.close()
    # 4. Revistas destacadas
    if estadisticas['revistas_destacadas']:
        revistas, cantidades = zip(*estadisticas['revistas_destacadas'])
        plt.figure(figsize=(10, 6))
        plt.barh(revistas[::-1], cantidades[::-1])
        plt.title('Top 15 revistas con más publicaciones')
        plt.xlabel('Número de publicaciones')
        plt.tight_layout()
        plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'revistas_destacadas.png'))
        plt.close()
    # 5. Editoriales destacadas
    if estadisticas['editoriales_destacadas']:
        editoriales, cantidades = zip(*estadisticas['editoriales_destacadas'])
        plt.figure(figsize=(10, 6))
        plt.barh(editoriales[::-1], cantidades[::-1])
        plt.title('Top 15 editoriales con más publicaciones')
        plt.xlabel('Número de publicaciones')
        plt.tight_layout()
        plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'editoriales_destacadas.png'))
        plt.close()

def main():
    asegurar_directorio_salida()
    entradas = parsear_bibtex('resultados_unicos.bib')
    print(f"Entradas leídas: {len(entradas)}")
    estadisticas = generar_estadisticas(entradas)
    visualizar_estadisticas(estadisticas)
    print("¡Estadísticas generadas con éxito!")
    print(f"- Gráficos y archivos guardados en: {DIRECTORIO_SALIDA}/")

if __name__ == '__main__':
    main()