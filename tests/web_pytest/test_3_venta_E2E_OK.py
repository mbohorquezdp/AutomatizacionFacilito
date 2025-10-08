# PRUEBA DE VENTA COMPLETA
import pytest
from time import sleep
from pages.categorias_ui_page import CategoryPage
from pages.checkout_ui_page import CheckoutPage
from pages.productos_electronicos_ui_page import Productselectronics
from pages.cart_ui_page import CarPage
from pages.confirmation_ui_page import Confirmation


@pytest.mark.e2e
def test_venta_e2e_OK(driver):
    # con la siguiente línea se vera la url de inicio de la web a probar
    driver.get("https://shophub-commerce.vercel.app/")
    page = CategoryPage(driver)
    page = Productselectronics(driver)
    page = CheckoutPage(driver)
    sleep(1)

    # Escogemos la categoría para nuestra prueba: Electrónica
    cat_electronics_E2E = CategoryPage(driver)
    cat_electronics_E2E.click_category_electronics("//h3[text()='Electronics']")
    sleep(1)
    assert "categories/electronics" in driver.current_url or "Electronics" in driver.title

    # Escogemos el elemento 22 que es una laptop
    detalle_electronics_E2E = Productselectronics(driver)
    detalle_electronics_E2E.click_detalle_electronics("//*[@id='view-details-22']")
    sleep(1)
    assert "product" in driver.current_url or "product" in driver.title

    # añadimos el elemento al carrito
    agregar_producto_E2E = CategoryPage(driver)
    agregar_producto_E2E.click_add_to_card("//button[contains(@id, 'add-to-cart-main')]")
    sleep(1)

    # damos click en la notificación de la parte superior derecha del carrito
    noti_al_checkout_E2E = CategoryPage(driver)
    noti_al_checkout_E2E.click_ir_checkout("div.absolute.h-5.w-5.rounded-full.text-xs")
    sleep(1)

    # iniciamos el proceso de chek confirmando el equipo seleccionado
    iniciar_checkout_E2E = CarPage(driver)
    iniciar_checkout_E2E.confirmar_inicio_pago("// button[text() = 'Proceed to Checkout']")
    sleep(1)

    # llenaremos los datos para el checkout
    check_out_E2E = CheckoutPage(driver)
    check_out_E2E.fill_checkout_form("Jorge", "Rojas", "test@gmail.com", "900900900", "jiron La Fe 777", "Lima", "123456", "Peru")
    sleep(1)

    # damos click en el boton de "Hacer pedido"
    hacer_pedido_E2E = CheckoutPage(driver)
    hacer_pedido_E2E.click_hacer_pedido("//button[text()='Place Order']")
    sleep(1)

    # damos click en el Boton de "return to home"
    retorno_to_home_E2E = Confirmation(driver)
    retorno_to_home_E2E.click_to_home("//button[text()='Return to Home']")
    sleep(1)
    assert driver.current_url == "https://shophub-commerce.vercel.app/", "La URL no es la esperada"



