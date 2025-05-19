import re
import os
from collections import Counter, defaultdict
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = "estadisticas_salida"  # Cambia esto si quieres otro nombre de carpeta

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def parse_bibtex(file_path):
    entries = []
    entry = {}
    entry_type = None
    key = None
    pattern_entry = re.compile(r"^@(\w+)\{([^,]+),")
    pattern_field = re.compile(r"^\s*(\w+)\s*=\s*[\{|\"](.+?)[\}|\"]\s*,?\s*$")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        m = pattern_entry.match(line)
        if m:
            if entry:
                entries.append(entry)
                entry = {}
            entry_type, key = m.groups()
            entry['type'] = entry_type.lower()
            entry['key'] = key
        else:
            m2 = pattern_field.match(line)
            if m2:
                campo, valor = m2.groups()
                entry[campo.lower()] = valor.strip()
        if line.strip().endswith('}'):
            if entry:
                entries.append(entry)
                entry = {}
    if entry and entry not in entries:
        entries.append(entry)
    final_entries = []
    for e in entries:
        autores = e.get('author', '').replace('\n', ' ').split(' and ')
        autores = [a.strip() for a in autores if a.strip()]
        first_author = autores[0] if autores else 'Unknown'
        title = e.get('title', 'Sin título')
        journal = e.get('journal', e.get('booktitle', 'Desconocido'))
        year = e.get('year', 'Desconocido')
        bibtype = e.get('type', 'article')
        if bibtype in ('article', 'journal'):
            tipo = 'article'
        elif bibtype in ('inproceedings', 'conference'):
            tipo = 'conference'
        elif bibtype == 'book':
            tipo = 'book'
        elif bibtype == 'incollection':
            tipo = 'book chapter'
        else:
            tipo = bibtype
        publisher = e.get('publisher', 'Desconocido')
        final_entries.append({
            'key': e.get('key', ''),
            'authors': autores,
            'first_author': first_author,
            'title': title,
            'journal': journal,
            'year': year,
            'type': tipo,
            'publisher': publisher
        })
    return final_entries

def generate_statistics(entries):
    stats = {}
    all_authors = [author for entry in entries for author in entry['authors']]
    stats['top_authors'] = Counter(all_authors).most_common(15)
    year_type_counts = defaultdict(lambda: defaultdict(int))
    for entry in entries:
        year_type_counts[entry['type']][entry['year']] += 1
    stats['year_by_type'] = year_type_counts
    stats['type_distribution'] = Counter([entry['type'] for entry in entries])
    stats['top_journals'] = Counter([entry['journal'] for entry in entries]).most_common(15)
    stats['top_publishers'] = Counter([entry['publisher'] for entry in entries]).most_common(15)
    return stats

def visualize_statistics(stats):
    # 1. Top autores
    if stats['top_authors']:
        authors, counts = zip(*stats['top_authors'])
        plt.figure(figsize=(10, 6))
        plt.barh(authors[::-1], counts[::-1])
        plt.title('Top 15 autores con más publicaciones')
        plt.xlabel('Número de publicaciones')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'top_authors.png'))
        plt.close()
    # 2. Publicaciones por año y tipo
    if stats['year_by_type']:
        df = pd.DataFrame(stats['year_by_type']).fillna(0).astype(int)
        df.T.plot(kind='bar', stacked=True, figsize=(12, 6))
        plt.title('Publicaciones por año y tipo')
        plt.ylabel('Número de publicaciones')
        plt.xlabel('Año')
        plt.legend(title='Tipo de producto')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'publications_by_year_type.png'))
        plt.close()
    # 3. Distribución de tipos
    if stats['type_distribution']:
        types, counts = zip(*stats['type_distribution'].items())
        plt.figure(figsize=(8, 8))
        plt.pie(counts, labels=types, autopct='%1.1f%%')
        plt.title('Distribución de tipos de productos')
        plt.savefig(os.path.join(OUTPUT_DIR, 'type_distribution.png'))
        plt.close()
    # 4. Top journals
    if stats['top_journals']:
        journals, counts = zip(*stats['top_journals'])
        plt.figure(figsize=(10, 6))
        plt.barh(journals[::-1], counts[::-1])
        plt.title('Top 15 journals con más publicaciones')
        plt.xlabel('Número de publicaciones')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'top_journals.png'))
        plt.close()
    # 5. Top publishers
    if stats['top_publishers']:
        publishers, counts = zip(*stats['top_publishers'])
        plt.figure(figsize=(10, 6))
        plt.barh(publishers[::-1], counts[::-1])
        plt.title('Top 15 publishers con más publicaciones')
        plt.xlabel('Número de publicaciones')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'top_publishers.png'))
        plt.close()

def save_statistics_to_excel(stats, filename='bibliometric_stats.xlsx'):
    with pd.ExcelWriter(os.path.join(OUTPUT_DIR, filename)) as writer:
        pd.DataFrame(stats['top_authors'], columns=['Autor', 'Publicaciones']).to_excel(
            writer, sheet_name='Top Autores', index=False)
        df = pd.DataFrame(stats['year_by_type']).fillna(0).astype(int)
        df.T.to_excel(writer, sheet_name='Publicaciones por año')
        pd.DataFrame(stats['type_distribution'].items(), columns=['Tipo', 'Cantidad']).to_excel(
            writer, sheet_name='Tipos de producto', index=False)
        pd.DataFrame(stats['top_journals'], columns=['Journal', 'Publicaciones']).to_excel(
            writer, sheet_name='Top Journals', index=False)
        pd.DataFrame(stats['top_publishers'], columns=['Publisher', 'Publicaciones']).to_excel(
            writer, sheet_name='Top Publishers', index=False)

def main():
    ensure_output_dir()
    entries = parse_bibtex('resultados_unicos.bib')
    print(f"Entradas leídas: {len(entries)}")
    stats = generate_statistics(entries)
    visualize_statistics(stats)
    save_statistics_to_excel(stats)
    print("¡Estadísticas generadas con éxito!")
    print(f"- Gráficos y Excel guardados en: {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()