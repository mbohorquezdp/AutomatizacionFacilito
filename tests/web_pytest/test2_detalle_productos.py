# PRUEBA DE VISUALIZACIÓN DE DETALLE DE PRODUCTO EN LA WEB

#from pages.category_page import CategoryPage
from pages import CategoryPage

# IMPORTACIONES NECESARIAS PARA ESPERAS EXPLÍCITAS

def test_hover_and_click_category(driver):
    # con la siguiente línea se verá
    driver.get("https://shophub-commerce.vercel.app/")
    page = CategoryPage(driver)

    page.hover_over_field()
    page.click_category_option()

    assert "categories/electronics" in driver.current_url or "Electronics" in driver.title