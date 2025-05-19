import os
import sys

from requerimiento1_2.exportacion.exportadores import Exportadores
from requerimiento1_2.extractores.extractores import ExtractorScienceDirect, ExtractorSpringer, ExtractorSage
from requerimiento1_2.util.utils import Utils
from requerimiento1_2.estadisticas_bibtex import main as estadisticas_main
from requerimiento3.analisis_variables_resumenes import main as variables_main
from requerimiento5.similitud_abstracts import (
    cargar_resumenes_desde_bibtex,
    matriz_similitud_coseno,
    matriz_similitud_jaccard,
    agrupar_por_similitud,
    visualizar_similitud,
    guardar_grupos
)

def main():
    print("====== INICIO DEL PROGRAMA DE ANÁLISIS BIBLIOMÉTRICO ======\n")

    # Configuración inicial
    print(">>> Cargando credenciales...")
    correo, contrasena = Utils.cargar_credenciales()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    CHROMEDRIVER_PATH = os.path.join(BASE_DIR, 'chromedriver-win64', 'chromedriver.exe')
    print(f">>> Ruta de chromedriver detectada: {CHROMEDRIVER_PATH}")

    print("\n===== PROCESO DE EXTRACCIÓN =====")
    # Extracción de ScienceDirect
    print("\n[1/3] Extrayendo artículos de ScienceDirect...")
    navegador_sd = None
    perfil_sd = None
    try:
        navegador_sd, espera_sd, perfil_sd = Utils.configurar_navegador(CHROMEDRIVER_PATH)
        extractor_sd = ExtractorScienceDirect(navegador_sd, espera_sd, correo, contrasena)
        entradas_sd = extractor_sd.extraer("computational thinking", max_resultados=40)
        # Verifica si el login realmente fue exitoso (por ejemplo, lista vacía puede indicar error)
        if entradas_sd is None or len(entradas_sd) == 0:
            raise Exception("No se extrajeron artículos, posiblemente el login falló.")
        print(f"ScienceDirect: {len(entradas_sd)} artículos extraídos.")
    except Exception as e:
        print(f"[ERROR] Falló el login o la extracción en ScienceDirect: {e}")
        print("El programa terminará. Por favor verifica tus credenciales e inténtalo de nuevo.")
        if navegador_sd is not None and perfil_sd is not None:
            try:
                Utils.limpiar_recursos(navegador_sd, perfil_sd)
            except Exception:
                pass
        sys.exit(1)
    if navegador_sd is not None and perfil_sd is not None:
        Utils.limpiar_recursos(navegador_sd, perfil_sd)

    # Si llegó aquí, el login fue exitoso en ScienceDirect. Continuar flujo normal:
    # Extracción de Springer
    print("\n[2/3] Extrayendo artículos de Springer...")
    navegador_sp, espera_sp, perfil_sp = Utils.configurar_navegador(CHROMEDRIVER_PATH)
    extractor_sp = ExtractorSpringer(navegador_sp, espera_sp, correo, contrasena)
    entradas_sp = extractor_sp.extraer("computational thinking", max_resultados=50)
    print(f"Springer: {len(entradas_sp)} artículos extraídos.")
    Utils.limpiar_recursos(navegador_sp, perfil_sp)

    # Extracción de SAGE
    print("\n[3/3] Extrayendo artículos de SAGE...")
    navegador_sage, espera_sage, perfil_sage = Utils.configurar_navegador(CHROMEDRIVER_PATH)
    extractor_sage = ExtractorSage(navegador_sage, espera_sage, correo, contrasena)
    entradas_sage = extractor_sage.extraer("computational thinking", max_resultados=40)
    print(f"SAGE: {len(entradas_sage)} artículos extraídos.")
    Utils.limpiar_recursos(navegador_sage, perfil_sage)

    print("\n===== PROCESAMIENTO Y DEDUPLICACIÓN =====")
    todas_entradas = entradas_sd + entradas_sp + entradas_sage
    unicos, repetidos = Utils.deduplicar_entradas(todas_entradas)
    print(f"Total resultados combinados: {len(todas_entradas)}")
    print(f"Resultados únicos: {len(unicos)}")
    print(f"Resultados repetidos: {len(repetidos)}")

    print("\n===== EXPORTACIÓN DE RESULTADOS =====")
    Exportadores.exportar_bibtex(unicos, "resultados_unicos.bib")
    print("Archivo 'resultados_unicos.bib' generado.")
    Exportadores.exportar_ris(unicos, "resultados_unicos.ris")
    print("Archivo 'resultados_unicos.ris' generado.")
    Exportadores.exportar_bibtex(repetidos, "resultados_repetidos.bib")
    print("Archivo 'resultados_repetidos.bib' generado.")
    Exportadores.exportar_ris(repetidos, "resultados_repetidos.ris")
    print("Archivo 'resultados_repetidos.ris' generado.")

    print("\n===== ESTADÍSTICAS BIBLIOMÉTRICAS =====")
    estadisticas_main()
    print("\nEstadísticas generadas y guardadas. Consulta la carpeta de salida de estadísticas.")

    print("\n===== ANÁLISIS DE VARIABLES EN RESÚMENES =====")
    output_dir = "analisis_variables_salida"
    print(f"Ejecutando análisis de variables en resúmenes sobre 'resultados_unicos.bib' y guardando en '{output_dir}'...")
    variables_main("resultados_unicos.bib", output_dir)
    print("Análisis de variables en resúmenes finalizado.")

    print("\n===== ANÁLISIS DE SIMILITUD ENTRE RESÚMENES =====")
    carpeta_entrada = os.path.dirname(os.path.abspath(__file__))
    archivo_bibtex = os.path.join(carpeta_entrada, "resultados_unicos.bib")
    carpeta_salida = os.path.join(carpeta_entrada, "similitud_salida")
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    titulos, resumenes = cargar_resumenes_desde_bibtex(archivo_bibtex)
    print(f"Resúmenes cargados para similitud: {len(resumenes)}")

    # Similitud del coseno
    print("\n--- SIMILITUD DEL COSENO ENTRE RESÚMENES ---")
    sim_cos = matriz_similitud_coseno(resumenes)
    visualizar_similitud(sim_cos, titulos, "coseno", carpeta_salida)
    grupos_cos = agrupar_por_similitud(sim_cos, titulos, umbral=0.5)
    print("\nGrupos por similitud del coseno:")
    for grupo, titulos_grupo in grupos_cos.items():
        print(f"Grupo {grupo}:")
        for titulo in titulos_grupo:
            print(f"  - {titulo}")
    guardar_grupos(grupos_cos, "coseno", carpeta_salida)

    # Similitud de Jaccard
    print("\n--- SIMILITUD DE JACCARD ENTRE RESÚMENES ---")
    sim_jac = matriz_similitud_jaccard(resumenes)
    visualizar_similitud(sim_jac, titulos, "jaccard", carpeta_salida)
    grupos_jac = agrupar_por_similitud(sim_jac, titulos, umbral=0.3)
    print("\nGrupos por similitud de Jaccard:")
    for grupo, titulos_grupo in grupos_jac.items():
        print(f"Grupo {grupo}:")
        for titulo in titulos_grupo:
            print(f"  - {titulo}")
    guardar_grupos(grupos_jac, "jaccard", carpeta_salida)

    print(f"\n[FIN] Resultados de similitud guardados en la carpeta: {carpeta_salida}")
    print("\n====== FIN DEL PROGRAMA ======\n")

if __name__ == "__main__":
    main()