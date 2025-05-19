import time
import tempfile
import shutil
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def limpiar(texto):
    return texto.replace('\n', ' ').replace('\r', '').strip()

def construir_bibtex(entry, idx=0):
    # Garantiza todos los campos
    autores = ' and '.join(entry.get('autores', [])) or "Unknown"
    titulo = entry.get('titulo', "Sin título")
    resumen = entry.get('resumen', "Sin resumen")
    journal = entry.get('journal', "Desconocido")
    year = entry.get('year', "Desconocido")
    # Clave única por título y año
    key = f"{titulo[:15].replace(' ', '').lower()}{year}{idx}"
    bibtex = f"""@article{{{key},
  author = {{{autores}}},
  title = {{{titulo}}},
  journal = {{{journal}}},
  year = {{{year}}},
  abstract = {{{resumen}}}
}}"""
    return bibtex

def construir_ris(entry):
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

def extraer_sciencedirect(driver, wait, correo, contrasena):
    driver.get("https://www-sciencedirect-com.crai.referencistas.com/")
    # Login con Google
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "btn-google"))).click()
    except Exception:
        pass
    try:
        wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(correo)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Siguiente")]'))).click()
    except Exception:
        pass
    time.sleep(5)
    try:
        wait.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(contrasena)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Siguiente")]'))).click()
    except Exception:
        pass
    time.sleep(10)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
    except Exception:
        pass
    try:
        search_box = wait.until(EC.presence_of_element_located((By.ID, "qs")))
        search_box.clear()
        search_box.send_keys("computational thinking")
    except Exception:
        raise
    try:
        search_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'button-primary') and contains(@aria-label, 'Submit quick search')]")
        ))
        search_btn.click()
    except Exception:
        try:
            driver.execute_script("arguments[0].click();", search_btn)
        except Exception:
            pass
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article, div.result-item-content")))
    except Exception:
        raise
    resultados = driver.find_elements(By.CSS_SELECTOR, "article")[:20]
    if not resultados:
        resultados = driver.find_elements(By.CSS_SELECTOR, "div.result-item-content")[:20]
    print(f"Resultados encontrados ScienceDirect: {len(resultados)}")
    entradas = []
    for resultado in resultados:
        try:
            titulo_elem = resultado.find_element(By.CSS_SELECTOR, "h2, h3")
            titulo = limpiar(titulo_elem.text)
        except:
            titulo = "Sin título"
        try:
            autores_elem = resultado.find_elements(By.CSS_SELECTOR, "span.author, .Authors, .author")
            autores = [limpiar(a.text) for a in autores_elem if limpiar(a.text)]
        except:
            autores = []
        try:
            resumen_elem = resultado.find_element(By.CSS_SELECTOR, "div.result-list-abstract, .Abstract")
            resumen = limpiar(resumen_elem.text)
        except:
            resumen = "Sin resumen"
        # Intenta journal y año si existen...
        try:
            journal_elem = resultado.find_element(By.CSS_SELECTOR, ".SubType, .publication-title")
            journal = limpiar(journal_elem.text)
        except:
            journal = "Desconocido"
        try:
            year_elem = resultado.find_element(By.CSS_SELECTOR, ".date, .CoverDate")
            year = limpiar(year_elem.text)[-4:]
        except:
            year = "Desconocido"
        entradas.append({
            "titulo": titulo,
            "autores": autores,
            "resumen": resumen,
            "journal": journal if journal else "Desconocido",
            "year": year if year else "Desconocido"
        })
    return entradas

def extraer_springer(driver, wait, correo, contrasena, max_resultados=50):
    driver.get("https://link-springer-com.crai.referencistas.com/")
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "c-cookie-banner__dismiss"))
        ).click()
    except Exception:
        pass
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "btn-google"))).click()
    except Exception:
        pass
    try:
        wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(correo)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Siguiente")]'))).click()
    except Exception:
        pass
    time.sleep(5)
    try:
        wait.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(contrasena)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Siguiente")]'))).click()
    except Exception:
        pass
    time.sleep(10)
    try:
        search_box = wait.until(EC.presence_of_element_located((By.ID, "homepage-search")))
        search_box.clear()
        search_box.send_keys("computational thinking")
        search_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.app-homepage-hero__button")
        ))
        search_btn.click()
    except Exception as e:
        raise
    entradas = []
    pagina = 1
    while len(entradas) < max_resultados:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".app-card-open__description")))
            time.sleep(2)
        except Exception:
            break
        descripciones = driver.find_elements(By.CSS_SELECTOR, ".app-card-open__description")
        for descripcion in descripciones:
            if len(entradas) >= max_resultados:
                break
            try:
                titulo_elem = descripcion.find_element(By.XPATH, "preceding-sibling::span[1]")
                titulo = limpiar(titulo_elem.text)
            except:
                titulo = "Sin título"
            try:
                resumen = limpiar(descripcion.text)
            except:
                resumen = "Sin resumen"
            try:
                autores_journal_container = descripcion.find_element(By.XPATH, "following-sibling::div[contains(@class, 'app-card-open__authors')]")
                autores_span = autores_journal_container.find_element(By.CSS_SELECTOR, "span[data-test='authors']")
                autores = [limpiar(a) for a in autores_span.text.split(",") if limpiar(a)]
                try:
                    journal_elem = autores_journal_container.find_element(By.CSS_SELECTOR, "a[data-test='parent']")
                    journal = limpiar(journal_elem.text)
                except:
                    journal = "Desconocido"
            except:
                autores = []
                journal = "Desconocido"
            try:
                meta_container = descripcion.find_element(By.XPATH, "following-sibling::div[contains(@class, 'app-card-open__meta')]")
                fecha_elem = meta_container.find_element(By.CSS_SELECTOR, "span[data-test='published']")
                year = "".join(filter(str.isdigit, fecha_elem.text[-4:]))
                if not year:
                    year = fecha_elem.text[-4:]
            except:
                year = "Desconocido"
            entradas.append({
                "titulo": titulo,
                "autores": autores,
                "resumen": resumen,
                "journal": journal if journal else "Desconocido",
                "year": year if year else "Desconocido"
            })
        if len(entradas) < max_resultados:
            try:
                next_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[contains(text(),'Next')]] | //a[.//span[contains(text(),'Next')]]")
                ))
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                time.sleep(1)
                next_btn.click()
                pagina += 1
                time.sleep(3)
            except Exception:
                break
        else:
            break
    print(f"Total de resultados extraídos: {len(entradas)}")
    return entradas

def extraer_sage(driver, wait, correo, contrasena):
    driver.get("https://search-sagepub-com.crai.referencistas.com/")
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "btn-google"))).click()
    except Exception:
        pass
    try:
        wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(correo)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Siguiente")]'))).click()
    except Exception:
        pass
    time.sleep(5)
    try:
        wait.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(contrasena)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Siguiente")]'))).click()
        time.sleep(10)
    except Exception:
        pass
    time.sleep(5)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
    except Exception:
        pass
    try:
        search_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input.sage-autocomplete-input")
        ))
        search_box.clear()
        search_box.send_keys("computational thinking")
        search_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.sage-search-autocomplete__icon")
        ))
        search_btn.click()
    except Exception:
        raise
    try:
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".sage-card.sage-card--search-result")
        ))
    except Exception:
        raise
    resultados = driver.find_elements(By.CSS_SELECTOR, ".sage-card.sage-card--search-result")[:20]
    print(f"Resultados encontrados SAGE: {len(resultados)}")
    entradas = []
    for resultado in resultados:
        try:
            titulo_elem = resultado.find_element(By.CSS_SELECTOR, ".sage-card--search-result__title a")
            titulo = limpiar(titulo_elem.text)
        except:
            titulo = "Sin título"
        try:
            autores_elem = resultado.find_elements(By.CSS_SELECTOR, ".sage-card__author-list span, .sage-card__author")
            autores = [limpiar(a.text) for a in autores_elem if limpiar(a.text)]
        except:
            autores = []
        try:
            resumen_elem = resultado.find_element(By.CSS_SELECTOR, ".sage-card__abstract, .sage-card--search-result__description")
            resumen = limpiar(resumen_elem.text)
        except:
            resumen = "Sin resumen"
        try:
            journal_elem = resultado.find_element(By.CSS_SELECTOR, ".sage-card__meta a")
            journal = limpiar(journal_elem.text)
        except:
            journal = "Desconocido"
        try:
            year_elem = resultado.find_element(By.CSS_SELECTOR, ".sage-card__meta time")
            year = limpiar(year_elem.text)[-4:]
        except:
            year = "Desconocido"
        entradas.append({
            "titulo": titulo,
            "autores": autores,
            "resumen": resumen,
            "journal": journal if journal else "Desconocido",
            "year": year if year else "Desconocido"
        })
    return entradas

def deduplicar_entradas(entradas1, entradas2):
    unicos = []
    repetidos = []
    vistos = set()
    def clave(entry):
        return (entry['titulo'].lower(), tuple([a.lower() for a in entry['autores']]))
    for e in entradas1:
        k = clave(e)
        vistos.add(k)
        unicos.append(e)
    for e in entradas2:
        k = clave(e)
        if k in vistos:
            repetidos.append(e)
        else:
            unicos.append(e)
            vistos.add(k)
    return unicos, repetidos

# Leer credenciales
with open('credenciales.txt', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()
    correo = lines[0].strip()
    contrasena = lines[1].strip()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMEDRIVER_PATH = os.path.join(BASE_DIR, 'chromedriver-win64', 'chromedriver.exe')
if not os.path.isfile(CHROMEDRIVER_PATH):
    raise FileNotFoundError(f"El archivo chromedriver.exe no se encontró en: {CHROMEDRIVER_PATH}")

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-save-password-bubble")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--disable-features=EnableEphemeralFlashPermission,PasswordManagerOnboarding,ProfilePicker")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
chrome_options.add_experimental_option("useAutomationExtension", False)

profile_dir = tempfile.mkdtemp()
chrome_options.add_argument(f"--user-data-dir={profile_dir}")
chrome_options.add_argument("--guest")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 40)

try:
    # Springer
    entradas_springer = extraer_springer(driver, wait, correo, contrasena)
    driver.quit()
    shutil.rmtree(profile_dir, ignore_errors=True)

    # Nuevo perfil temporal para SAGE
    profile_dir = tempfile.mkdtemp()
    chrome_options.arguments[:] = [arg for arg in chrome_options.arguments if not arg.startswith("--user-data-dir")]
    chrome_options.add_argument(f"--user-data-dir={profile_dir}")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 40)
    entradas_sage = extraer_sage(driver, wait, correo, contrasena)
    driver.quit()
    shutil.rmtree(profile_dir, ignore_errors=True)

    # Nuevo perfil temporal para ScienceDirect
    profile_dir = tempfile.mkdtemp()
    chrome_options.arguments[:] = [arg for arg in chrome_options.arguments if not arg.startswith("--user-data-dir")]
    chrome_options.add_argument(f"--user-data-dir={profile_dir}")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 40)
    entradas_sciencedirect = extraer_sciencedirect(driver, wait, correo, contrasena)

    # Unir y deduplicar
    entradas_unicas, entradas_repetidas = deduplicar_entradas(entradas_sciencedirect, entradas_sage + entradas_springer)

    # Guardar únicos
    with open("resultados_unicos.bib", "w", encoding="utf-8") as f:
        for idx, entry in enumerate(entradas_unicas):
            f.write(construir_bibtex(entry, idx))
            f.write("\n\n")
    with open("resultados_unicos.ris", "w", encoding="utf-8") as f:
        for entry in entradas_unicas:
            f.write(construir_ris(entry))
            f.write("\n")

    # Guardar repetidos
    with open("resultados_repetidos.bib", "w", encoding="utf-8") as f:
        for idx, entry in enumerate(entradas_repetidas):
            f.write(construir_bibtex(entry, idx))
            f.write("\n\n")
    with open("resultados_repetidos.ris", "w", encoding="utf-8") as f:
        for entry in entradas_repetidas:
            f.write(construir_ris(entry))
            f.write("\n")

    print(f"¡Exportados {len(entradas_unicas)} únicos y {len(entradas_repetidas)} repetidos!")
except Exception as e:
    print(f"Error durante la automatización: {e}")
finally:
    try:
        driver.quit()
    except:
        pass
    shutil.rmtree(profile_dir, ignore_errors=True)