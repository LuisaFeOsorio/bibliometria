from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class ExtractorBase:
    def __init__(self, navegador, espera, correo, contrasena):
        print("[ExtractorBase] Inicializando extractor base...")
        self.navegador = navegador
        self.espera = espera
        self.correo = correo
        self.contrasena = contrasena

    def limpiar(self, texto):
        """Limpia el texto de caracteres especiales y espacios innecesarios"""
        return texto.replace('\n', ' ').replace('\r', '').strip()

    def _iniciar_sesion_google(self):
        """Método común para login con Google"""
        print("[ExtractorBase] Iniciando sesión con Google...")
        try:
            self.espera.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(self.correo)
            self.espera.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Siguiente")]'))).click()
            time.sleep(2)
            self.espera.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(self.contrasena)
            self.espera.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Siguiente")]'))).click()
            time.sleep(5)
            print("[ExtractorBase] Sesión Google completada.")
            return True
        except Exception as e:
            print(f"[ExtractorBase] Error en login Google: {e}")
            raise Exception("Login fallido con Google") from e

class ExtractorScienceDirect(ExtractorBase):
    def iniciar_sesion(self):
        print("[ScienceDirect] Iniciando sesión en ScienceDirect...")
        try:
            self.navegador.get("https://www-sciencedirect-com.crai.referencistas.com/")
            self.espera.until(EC.element_to_be_clickable((By.ID, "btn-google"))).click()
            self._iniciar_sesion_google()
            self._aceptar_cookies()
            print("[ScienceDirect] Sesión iniciada correctamente.")
            return True
        except Exception as e:
            print(f"[ScienceDirect] Error al iniciar sesión: {e}")
            raise Exception("Login fallido en ScienceDirect") from e

    def _aceptar_cookies(self):
        print("[ScienceDirect] Intentando aceptar cookies...")
        try:
            self.espera.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
            time.sleep(1)
            print("[ScienceDirect] Cookies aceptadas.")
        except Exception:
            print("[ScienceDirect] No se encontró el banner de cookies o ya fue aceptado.")

    def buscar(self, consulta):
        print(f"[ScienceDirect] Buscando: '{consulta}'")
        try:
            search_container = self.espera.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search-input-container"))
            )
            caja_busqueda = search_container.find_element(By.CSS_SELECTOR, "input.search-input-field")
            caja_busqueda.clear()
            time.sleep(1)
            caja_busqueda.send_keys(consulta)
            time.sleep(2)

            boton_buscar = self.espera.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[class*='button-primary'][aria-label*='Submit quick search']")
            ))
            boton_buscar.click()
            time.sleep(3)
            print("[ScienceDirect] Búsqueda ejecutada.")
            return True
        except Exception as e:
            print(f"[ScienceDirect] Error al buscar: {str(e)}")
            self.navegador.save_screenshot("error_busqueda_sciencedirect.png")
            raise Exception("Búsqueda fallida en ScienceDirect") from e

    def extraer_resultados(self, max_resultados):
        print(f"[ScienceDirect] Extrayendo hasta {max_resultados} resultados...")
        try:
            self.espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article, div.result-item-content")))
        except Exception as e:
            print(f"[ScienceDirect] No se encontraron resultados: {e}")
            return []

        resultados = self.navegador.find_elements(By.CSS_SELECTOR, "article")[:max_resultados]
        if not resultados:
            resultados = self.navegador.find_elements(By.CSS_SELECTOR, "div.result-item-content")[:max_resultados]

        entradas = []
        for i, resultado in enumerate(resultados):
            print(f"[ScienceDirect] Extrayendo resultado {i+1}...")
            entrada = {
                "titulo": self._extraer_titulo(resultado),
                "autores": self._extraer_autores(resultado),
                "resumen": self._extraer_resumen(resultado),
                "journal": self._extraer_journal(resultado),
                "year": self._extraer_year(resultado)
            }
            entradas.append(entrada)

        print(f"[ScienceDirect] Total entradas extraídas: {len(entradas)}")
        return entradas

    def _extraer_titulo(self, elemento):
        try:
            titulo_elem = elemento.find_element(By.CSS_SELECTOR, "h2.result-list-title a")
            return self.limpiar(titulo_elem.text)
        except Exception:
            return "Sin título"

    def _extraer_autores(self, elemento):
        try:
            autores_elem = elemento.find_elements(By.CSS_SELECTOR, "span.author, .Authors, .author")
            return [self.limpiar(a.text) for a in autores_elem if self.limpiar(a.text)]
        except Exception:
            return []

    def _extraer_resumen(self, elemento):
        try:
            resumen_elem = elemento.find_element(By.CSS_SELECTOR, "div.result-list-abstract, .Abstract")
            return self.limpiar(resumen_elem.text)
        except Exception:
            return "Sin resumen"

    def _extraer_journal(self, elemento):
        try:
            revista_elem = elemento.find_element(By.CSS_SELECTOR, ".SubType, .publication-title")
            return self.limpiar(revista_elem.text)
        except Exception:
            return "Desconocido"

    def _extraer_year(self, elemento):
        try:
            anio_elem = elemento.find_element(By.CSS_SELECTOR, ".date, .CoverDate")
            return self.limpiar(anio_elem.text)[-4:]
        except Exception:
            return "Desconocido"

    def extraer(self, consulta, max_resultados=20):
        print(f"[ScienceDirect] Iniciando extracción para: '{consulta}'")
        self.iniciar_sesion()  # Lanzará excepción si falla el login
        self.buscar(consulta)  # Lanzará excepción si falla la búsqueda
        resultados = self.extraer_resultados(max_resultados)
        return resultados

class ExtractorSpringer(ExtractorBase):
    def iniciar_sesion(self):
        print("[Springer] Iniciando sesión en Springer...")
        try:
            self.navegador.get("https://link-springer-com.crai.referencistas.com/")
            self.espera.until(EC.element_to_be_clickable((By.ID, "btn-google"))).click()
            self._iniciar_sesion_google()
            self._aceptar_cookies()
            print("[Springer] Sesión iniciada correctamente.")
            return True
        except Exception as e:
            print(f"[Springer] Error al iniciar sesión: {e}")
            raise Exception("Login fallido en Springer") from e

    def _aceptar_cookies(self):
        print("[Springer] Intentando aceptar cookies...")
        try:
            WebDriverWait(self.navegador, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "c-cookie-banner__dismiss"))
            ).click()
            time.sleep(1)
            print("[Springer] Cookies aceptadas.")
        except Exception:
            print("[Springer] No se encontró el banner de cookies de Springer.")

    def buscar(self, consulta):
        print(f"[Springer] Buscando: '{consulta}'")
        try:
            search_box = self.espera.until(EC.presence_of_element_located((By.ID, "homepage-search")))
            search_box.clear()
            search_box.send_keys(consulta)
            search_btn = self.espera.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.app-homepage-hero__button")
            ))
            search_btn.click()
            time.sleep(3)
            print("[Springer] Búsqueda ejecutada.")
            return True
        except Exception as e:
            print(f"[Springer] Error al buscar: {e}")
            raise Exception("Búsqueda fallida en Springer") from e

    def extraer_resultados(self, max_resultados):
        print(f"[Springer] Extrayendo hasta {max_resultados} resultados...")
        entradas = []
        pagina = 1

        while len(entradas) < max_resultados:
            try:
                self.espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".app-card-open")))
                time.sleep(2)
            except Exception as e:
                print(f"[Springer] No se encontraron resultados en la página {pagina}: {e}")
                break

            cards = self.navegador.find_elements(By.CSS_SELECTOR, ".app-card-open")
            for i, card in enumerate(cards):
                if len(entradas) >= max_resultados:
                    break

                print(f"[Springer] Extrayendo resultado página {pagina}, item {i+1}...")
                entrada = {
                    "titulo": self._extraer_titulo(card),
                    "autores": self._extraer_autores(card),
                    "resumen": self._extraer_resumen(card),
                    "journal": self._extraer_journal(card),
                    "year": self._extraer_year(card)
                }
                entradas.append(entrada)

            if len(entradas) < max_resultados:
                if not self._siguiente_pagina():
                    print("[Springer] No hay más páginas.")
                    break
                pagina += 1

        print(f"[Springer] Total entradas extraídas: {len(entradas)}")
        return entradas

    def _extraer_titulo(self, elemento):
        try:
            titulo_elem = elemento.find_element(By.CSS_SELECTOR, "h3.app-card-open__heading a span")
            return self.limpiar(titulo_elem.text)
        except Exception:
            return "Sin título"

    def _extraer_autores(self, elemento):
        try:
            autores_span = elemento.find_element(By.CSS_SELECTOR, "span[data-test='authors']")
            return [self.limpiar(a) for a in autores_span.text.split(",") if self.limpiar(a)]
        except Exception:
            return []

    def _extraer_resumen(self, elemento):
        try:
            descripcion_elem = elemento.find_element(By.CSS_SELECTOR, ".app-card-open__description")
            return self.limpiar(descripcion_elem.text)
        except Exception:
            return "Sin resumen"

    def _extraer_journal(self, elemento):
        try:
            journal_elem = elemento.find_element(By.CSS_SELECTOR, "a[data-test='parent']")
            return self.limpiar(journal_elem.text)
        except Exception:
            return "Desconocido"

    def _extraer_year(self, elemento):
        try:
            fecha_elem = elemento.find_element(By.CSS_SELECTOR, "span[data-test='published']")
            year = "".join(filter(str.isdigit, fecha_elem.text[-4:]))
            return year if year else fecha_elem.text[-4:]
        except Exception:
            return "Desconocido"

    def _siguiente_pagina(self):
        print("[Springer] Intentando ir a la siguiente página de resultados...")
        try:
            next_btn = self.espera.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(),'Next')]] | //a[.//span[contains(text(),'Next')]]")
            ))
            self.navegador.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            time.sleep(1)
            next_btn.click()
            time.sleep(3)
            print("[Springer] Página siguiente cargada.")
            return True
        except Exception:
            print("[Springer] No se encontró botón 'Next' o no se pudo avanzar.")
            return False

    def extraer(self, consulta, max_resultados=50):
        print(f"[Springer] Iniciando extracción para: '{consulta}'")
        self.iniciar_sesion() # Lanzará excepción si falla el login
        self.buscar(consulta) # Lanzará excepción si falla la búsqueda
        return self.extraer_resultados(max_resultados)

class ExtractorSage(ExtractorBase):
    def iniciar_sesion(self):
        print("[SAGE] Iniciando sesión en SAGE...")
        try:
            self.navegador.get("https://search-sagepub-com.crai.referencistas.com/")
            self.espera.until(EC.element_to_be_clickable((By.ID, "btn-google"))).click()
            self._iniciar_sesion_google()
            self._aceptar_cookies()
            print("[SAGE] Sesión iniciada correctamente.")
            return True
        except Exception as e:
            print(f"[SAGE] Error al iniciar sesión en SAGE: {e}")
            raise Exception("Login fallido en SAGE") from e

    def _aceptar_cookies(self):
        print("[SAGE] Intentando aceptar cookies...")
        try:
            WebDriverWait(self.navegador, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
            time.sleep(1)
            print("[SAGE] Cookies aceptadas.")
        except Exception:
            print("[SAGE] No se encontró el banner de cookies de SAGE.")

    def buscar(self, consulta):
        print(f"[SAGE] Buscando: '{consulta}'")
        try:
            search_box = self.espera.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input.sage-autocomplete-input")
            ))
            search_box.clear()
            search_box.send_keys(consulta)
            search_btn = self.espera.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.sage-search-autocomplete__icon")
            ))
            search_btn.click()
            time.sleep(3)
            print("[SAGE] Búsqueda ejecutada.")
            return True
        except Exception as e:
            print(f"[SAGE] Error al buscar: {e}")
            raise Exception("Búsqueda fallida en SAGE") from e

    def extraer_resultados(self, max_resultados):
        print(f"[SAGE] Extrayendo hasta {max_resultados} resultados...")
        try:
            self.espera.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".sage-card.sage-card--search-result")
            ))
        except Exception as e:
            print(f"[SAGE] No se encontraron resultados: {e}")
            return []

        resultados = self.navegador.find_elements(By.CSS_SELECTOR, ".sage-card.sage-card--search-result")[:max_resultados]
        entradas = []

        for i, resultado in enumerate(resultados):
            print(f"[SAGE] Extrayendo resultado {i+1}...")
            entrada = {
                "titulo": self._extraer_titulo(resultado),
                "autores": self._extraer_autores(resultado),
                "resumen": self._extraer_resumen(resultado),
                "journal": self._extraer_journal(resultado),
                "year": self._extraer_year(resultado)
            }
            entradas.append(entrada)

        print(f"[SAGE] Total entradas extraídas: {len(entradas)}")
        return entradas

    def _extraer_titulo(self, elemento):
        try:
            titulo_elem = elemento.find_element(By.CSS_SELECTOR, ".sage-card--search-result__title a")
            return self.limpiar(titulo_elem.text)
        except Exception:
            return "Sin título"

    def _extraer_autores(self, elemento):
        try:
            autores_elem = elemento.find_elements(By.CSS_SELECTOR, ".sage-card__author-list span, .sage-card__author")
            return [self.limpiar(a.text) for a in autores_elem if self.limpiar(a.text)]
        except Exception:
            return []

    def _extraer_resumen(self, elemento):
        try:
            resumen_btn = elemento.find_element(By.XPATH, ".//button[contains(., 'Resumen de vista previa')]")
            resumen_btn.click()
            self.espera.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".issue-item__abstract__content.collapse.show")
            ))
            resumen_elem = elemento.find_element(By.CSS_SELECTOR, ".issue-item__abstract__content.collapse.show")
            return self.limpiar(resumen_elem.text)
        except Exception:
            return "Sin resumen"

    def _extraer_journal(self, elemento):
        try:
            journal_elem = elemento.find_element(By.CSS_SELECTOR, ".sage-card__meta a")
            return self.limpiar(journal_elem.text)
        except Exception:
            return "Desconocido"

    def _extraer_year(self, elemento):
        try:
            year_elem = elemento.find_element(By.CSS_SELECTOR, ".sage-card__meta time")
            return self.limpiar(year_elem.text)[-4:]
        except Exception:
            return "Desconocido"

    def extraer(self, consulta, max_resultados=20):
        print(f"[SAGE] Iniciando extracción para: '{consulta}'")
        self.iniciar_sesion()  # Lanzará excepción si falla el login
        self.buscar(consulta)  # Lanzará excepción si falla la búsqueda
        return self.extraer_resultados(max_resultados)