# PRUEBA DE VISUALIZACIÓN DE DETALLE DE PRODUCTO EN LA WEB

#from pages.category_page import CategoryPage
from tests.web_pytest.pages.categorias_page_ui import CategoryPage

def test_hover_and_click_category(driver):
    driver.get("https://shophub-commerce.vercel.app/")  # Reemplaza con la URL real
    page = CategoryPage(driver)

    page.hover_over_field()
    page.click_category_option()

    assert "categories/electronics" in driver.current_url or "Electronics" in driver.title