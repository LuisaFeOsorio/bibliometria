class Exportadores:
    @staticmethod
    def construir_bibtex(entry, idx=0):
        print(f"[BibTeX] Construyendo entrada {idx+1}...")
        autores = ' and '.join(entry.get('autores', [])) or "Unknown"
        titulo = entry.get('titulo', "Sin título")
        resumen = entry.get('resumen', "Sin resumen")
        journal = entry.get('journal', "Desconocido")
        year = entry.get('year', "Desconocido")
        key = f"{titulo[:15].replace(' ', '').lower()}{year}{idx}"
        bibtex = f"""@article{{{key},
  author = {{{autores}}},
  title = {{{titulo}}},
  journal = {{{journal}}},
  year = {{{year}}},
  abstract = {{{resumen}}}
}}"""
        return bibtex

    @staticmethod
    def construir_ris(entry):
        print(f"[RIS] Construyendo entrada para: {entry.get('titulo', 'Sin título')}")
        autores = ''.join([f"AU  - {a}\n" for a in entry.get('autores', [])]) or "AU  - Unknown\n"
        titulo = entry.get('titulo', "Sin título")
        resumen = entry.get('resumen', "Sin resumen")
        journal = entry.get('journal', "Desconocido")
        year = entry.get('year', "Desconocido")
        ris = f"""TY  - JOUR
{autores}TI  - {titulo}
T2  - {journal}
PY  - {year}
AB  - {resumen}
ER  -
"""
        return ris

    @staticmethod
    def exportar_bibtex(entradas, archivo_salida):
        print(f"Iniciando exportación BibTeX a '{archivo_salida}'...")
        with open(archivo_salida, "w", encoding="utf-8") as f:
            for idx, entry in enumerate(entradas):
                f.write(Exportadores.construir_bibtex(entry, idx))
                f.write("\n\n")
        print(f"Archivo BibTeX '{archivo_salida}' generado con {len(entradas)} entradas.")

    @staticmethod
    def exportar_ris(entradas, archivo_salida):
        print(f"Iniciando exportación RIS a '{archivo_salida}'...")
        with open(archivo_salida, "w", encoding="utf-8") as f:
            for entry in entradas:
                f.write(Exportadores.construir_ris(entry))
                f.write("\n")
        print(f"Archivo RIS '{archivo_salida}' generado con {len(entradas)} entradas.")