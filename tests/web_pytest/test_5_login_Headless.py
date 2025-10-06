# PRUEBA DE ACCESO CON CREDENCIALES A LA WEB (MODO HEADLESS)

from time import sleep
import pytest
from pages.login_ui_page import LoginPage
from dotenv import load_dotenv
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cargar variables de entorno
load_dotenv()

correo_cliente_antiguo = os.getenv("correo_ant")
password_cliente_antiguo = os.getenv("password_ant")

# Fixture local forzado a headless
from utils.driver_factory import create_driver

@pytest.fixture
def driver():
    # la siguiente línea nos dará el modo headless (sin interfaz gráfica)
    driver = create_driver(headless=True)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.ingresoweb
def test_ingreso_web(driver):
    login = LoginPage(driver)
    login.load()
    sleep(2)
    login.login_as_user(correo_cliente_antiguo, password_cliente_antiguo)
    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Go to Home']"))
    )