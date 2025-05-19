import os
from similitud_abstracts import (
    cargar_resumenes_desde_bibtex,
    matriz_similitud_coseno,
    matriz_similitud_jaccard,
    agrupar_por_similitud,
    visualizar_similitud,
    guardar_grupos
)

def main():
    carpeta_entrada = os.path.join("..", "requerimiento1_2")
    archivo_bibtex = os.path.join(carpeta_entrada, "resultados_unicos.bib")
    carpeta_salida = os.path.join(os.path.dirname(__file__), "salida")
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    titulos, resumenes = cargar_resumenes_desde_bibtex(archivo_bibtex)
    print(f"Resúmenes cargados: {len(resumenes)}")

    # 1. Similitud del coseno
    sim_cos = matriz_similitud_coseno(resumenes)
    visualizar_similitud(sim_cos, titulos, "coseno", carpeta_salida)
    grupos_cos = agrupar_por_similitud(sim_cos, titulos, umbral=0.5)
    print("\nGrupos por similitud del coseno:")
    for grupo, titulos_grupo in grupos_cos.items():
        print(f"Grupo {grupo}:")
        for titulo in titulos_grupo:
            print(f"  - {titulo}")
    guardar_grupos(grupos_cos, "coseno", carpeta_salida)

    # 2. Similitud de Jaccard
    sim_jac = matriz_similitud_jaccard(resumenes)
    visualizar_similitud(sim_jac, titulos, "jaccard", carpeta_salida)
    grupos_jac = agrupar_por_similitud(sim_jac, titulos, umbral=0.3)
    print("\nGrupos por similitud de Jaccard:")
    for grupo, titulos_grupo in grupos_jac.items():
        print(f"Grupo {grupo}:")
        for titulo in titulos_grupo:
            print(f"  - {titulo}")
    guardar_grupos(grupos_jac, "jaccard", carpeta_salida)

    print(f"\n[FIN] Resultados guardados en la carpeta: {carpeta_salida}")

if __name__ == "__main__":
    main()