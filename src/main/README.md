
# Proyecto de Extracción y Análisis Bibliométrico

Este proyecto permite extraer artículos científicos de ScienceDirect, 
Springer y SAGE, deduplicarlos, exportar los resultados en formatos BibTeX y RIS, 
generar estadísticas bibliométricas, analizar variables relevantes en los resúmenes 
y calcular similitudes entre abstracts.

---
## Observación

- Al iniciar el programa solicita correo y contraseña **Institucional**
para poder tener un ingreso exitoso a las bases de datos

- El programa muestra por consola todas las ejecuciones que se van realizando
igualmente abre una pestaña de chrome donde se puede evidenciar de forma ilustrativa
el proceso.

- Al cargar una página, el programa espera por un tiempo prudente para aceptar las 
cookies o continuar con la ejecución, se recomienda no detener la ejecucion

## Requisitos

- Python 3.8 o superior
- Google Chrome instalado
- Chromedriver compatible con tu versión de Chrome y sistema operativo

---

## Instalación

### 1. Clonar el repositorio

### 2. Crear y activar un entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```
### 4. Descargar Chromedriver

- Descarga `chromedriver` desde [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) eligiendo tu versión de Chrome y sistema operativo.
- Extrae el archivo descargado.
- Ubica la carpeta `chromedriver-win64` (o similar) **dos niveles arriba** del archivo principal `Principal.py`
- Dentro de esa carpeta debe estar el archivo ejecutable `chromedriver.exe` (Windows) o `chromedriver` (Linux/Mac).

### 5. Crear el archivo de credenciales

Crea un archivo llamado `credenciales.txt` en la raíz del proyecto o donde lo requiera tu función, con el siguiente formato (una línea para el correo, otra para la contraseña):

credenciales.txt de ejemplo:

usuario@correo.com
contraseña123

---


## Ejecución

Desde la carpeta donde está `Principal.py`:

```bash
python Principal.py
```

---

## Salida

- Archivos BibTeX y RIS generados con resultados únicos y repetidos.
- Carpeta con estadísticas y gráficos bibliométricos.
- Carpeta con análisis de variables en resúmenes y nubes de palabras.
- Carpeta con análisis de similitud de resúmenes y agrupamientos.

---

## Notas importantes

- **No compartas tu archivo `credenciales.txt`.**
- Si obtienes errores relacionados con `chromedriver`, verifica su ubicación y compatibilidad con tu navegador.
- Si ves errores de módulos ausentes, asegúrate de instalar todas las dependencias.
- Si usas otro sistema operativo, cambia las instrucciones de rutas o ejecutables según corresponda.

---
