import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class Utils:
    @staticmethod
    def pedir_y_guardar_credenciales(ruta='credenciales.txt'):
        print("Por favor, ingresa tus credenciales para continuar.")
        correo = input("Correo: ").strip()
        contrasena = input("Contraseña: ").strip()
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(correo + '\n')
            f.write(contrasena + '\n')
        print("Credenciales guardadas en credenciales.txt")
        return correo, contrasena

    @staticmethod
    def cargar_credenciales(ruta='credenciales.txt'):
        # Siempre pide y sobreescribe las credenciales
        return Utils.pedir_y_guardar_credenciales(ruta)

    @staticmethod
    def configurar_navegador(ruta_chromedriver):
        opciones = Options()
        opciones.add_argument("--start-maximized")
        opciones.add_argument("--disable-infobars")
        opciones.add_argument("--disable-notifications")
        opciones.add_argument("--disable-save-password-bubble")
        opciones.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        perfil = tempfile.mkdtemp()
        opciones.add_argument(f"--user-data-dir={perfil}")
        opciones.add_argument("--guest")
        servicio = Service(ruta_chromedriver)
        navegador = webdriver.Chrome(service=servicio, options=opciones)
        espera = WebDriverWait(navegador, 30)
        return navegador, espera, perfil

    @staticmethod
    def limpiar_recursos(navegador, perfil):
        try:
            navegador.quit()
        except Exception as e:
            print(f"Error al cerrar el navegador: {e}")
        finally:
            shutil.rmtree(perfil, ignore_errors=True)

    @staticmethod
    def deduplicar_entradas(entradas):
        unicos = []
        repetidos = []
        vistos = set()
        def clave(entry):
            return (entry['titulo'].lower(), tuple([a.lower() for a in entry.get('autores', [])]))
        for e in entradas:
            k = clave(e)
            if k in vistos:
                repetidos.append(e)
            else:
                unicos.append(e)
                vistos.add(k)
        return unicos, repetidos