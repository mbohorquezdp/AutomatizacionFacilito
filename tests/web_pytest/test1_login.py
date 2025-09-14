# PRUEBA DE ACCESO CON CREDENCIALES A LA WEB

from time import sleep
import pytest
from pages.login_page_ui import LoginPage
# dovent es la biblioteca que nos permite trabajar con variables de entorno, del archivo .env
from dotenv import load_dotenv
import os

# IMPORTACIONES NECESARIAS PARA ESPERAS EXPLÍCITAS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cargar variables de entorno
load_dotenv()

correo_cliente_antiguo = os.getenv("correo_ant")
password_cliente_antiguo = os.getenv("password_ant")

@pytest.mark.ingresoweb
# primer ts de acceso con credenciales
def test_ingreso_web(driver):
    login = LoginPage(driver)
    login.load()
    sleep(2)
    login.login_as_user(correo_cliente_antiguo, password_cliente_antiguo)
    sleep(2)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Go to Home']")))







