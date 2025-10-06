# PRUEBA DE INTENTO DE VENTA QUE SE CANCELA ANTES DE HACER EL PEDIDO (HEADLESS)

import pytest
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_factory import create_driver
from pages.categorias_ui_page import CategoryPage
from pages.checkout_ui_page import CheckoutPage
from pages.productos_electronicos_ui_page import Productselectronics
from pages.cart_ui_page import CarPage
from pages.confirmation_ui_page import Confirmation

@pytest.fixture
def driver():
    driver = create_driver(headless=True)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

def test_venta_cancelada_OK(driver):
    driver.get("https://shophub-commerce.vercel.app/")
    wait = WebDriverWait(driver, 10)
    sleep(1)

    # Clic en categoría Electronics
    xpath_categoria = "//h3[text()='Electronics']"
    categoria = wait.until(EC.presence_of_element_located((By.XPATH, xpath_categoria)))
    driver.execute_script("arguments[0].scrollIntoView(true);", categoria)
    sleep(0.5)
    driver.execute_script("arguments[0].click();", categoria)
    sleep(1)
    assert "categories/electronics" in driver.current_url or "Electronics" in driver.title

    # Clic en detalle del producto
    xpath_detalle = "//*[@id='view-details-22']"
    detalle = wait.until(EC.presence_of_element_located((By.XPATH, xpath_detalle)))
    driver.execute_script("arguments[0].scrollIntoView(true);", detalle)
    sleep(0.5)
    driver.execute_script("arguments[0].click();", detalle)
    sleep(1)
    assert "product" in driver.current_url or "product" in driver.title

    # Clic en botón "Add to cart"
    xpath_add = "//button[contains(@id, 'add-to-cart-main')]"
    add_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpath_add)))
    driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
    sleep(0.5)
    driver.execute_script("arguments[0].click();", add_btn)
    sleep(1)

    # Clic en ícono del carrito (notificación superior)
    xpath_checkout = "div.absolute.h-5.w-5.rounded-full.text-xs"
    checkout_icon = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, xpath_checkout)))
    driver.execute_script("arguments[0].scrollIntoView(true);", checkout_icon)
    sleep(0.5)
    driver.execute_script("arguments[0].click();", checkout_icon)
    sleep(1)

    # Clic en botón "Remove"
    xpath_remove = "//button[text()='Remove']"
    remove_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpath_remove)))
    driver.execute_script("arguments[0].scrollIntoView(true);", remove_btn)
    sleep(0.5)
    driver.execute_script("arguments[0].click();", remove_btn)
    sleep(1)

    assert driver.current_url == "https://shophub-commerce.vercel.app/cart", "La URL no es la esperada"