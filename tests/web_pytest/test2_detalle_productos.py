# PRUEBA DE VISUALIZACIÓN DE DETALLE DE PRODUCTO EN LA WEB

from time import sleep
import pytest
from pages.categorias_page_ui import CategoryPage

# IMPORTACIONES NECESARIAS PARA ESPERAS EXPLÍCITAS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def test_hover_and_click_category(driver):
    # con la siguiente línea se verá
    driver.get("https://shophub-commerce.vercel.app/")
    page = CategoryPage(driver)
    page.click_category_option()

    # Si hay más de una ventana, cambiamos al nuevo contexto
    if len(ventanas) > 1:
        driver.switch_to.window(ventanas[1])

    # Espera explícita para asegurar que la nueva página cargó
    WebDriverWait(driver, 10).until(
        EC.url_contains("categories/electronics")
    )

    # Validación final


    assert "categories/electronics" in driver.current_url or "Electronics" in driver.title