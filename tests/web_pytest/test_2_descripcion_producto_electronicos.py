# PRUEBA DE VISUALIZACIÓN DE DETALLE DE PRODUCTO EN LA WEB

from time import sleep
from pages.categorias_ui_page import CategoryPage
from pages.productos_electronicos_ui_page import Productselectronics

def test_detalle_prod(driver):
    # con la siguiente línea se verá
    driver.get("https://shophub-commerce.vercel.app/")
    page = CategoryPage(driver)
    page = Productselectronics(driver)
    sleep(1)

    cat_electronics = CategoryPage(driver)
    cat_electronics.click_category_electronics("//h3[text()='Electronics']")
    sleep(1)
    assert "categories/electronics" in driver.current_url or "Electronics" in driver.title

    detalle_electronics = Productselectronics(driver)
    detalle_electronics.click_detalle_electronics("//*[@id='view-details-22']")
    sleep(1)
    assert "product" in driver.current_url or "product" in driver.title


    texto_obtenido = page.get_texto()
    assert texto_obtenido == "High-performance laptop for work and gaming", "El texto no coincide con lo esperado"
    sleep(2)