from .base_ui_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Productselectronics(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.texto_localizador = (By.XPATH, "//*[@id='product-desc-text-22']")  # Ajusta según tu HTML

    TITLE = (By.CSS_SELECTOR, "title")
    CART_BADGE = (By.CSS_SELECTOR, "shopping_cart_badge")
    CART_LINK = (By.ID, "shopping_cart_container")

    def click_detalle_electronics(self, xpath):
        # Esperar a que desaparezca el overlay si existe
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "fixed")))
        except:
            pass  # Si no existe, continúa

        # Buscar el botón
        boton = self.driver.find_element(By.XPATH, xpath)

        # Hacer scroll hasta el botón
        self.driver.execute_script("arguments[0].scrollIntoView();", boton)

        # Intentar clic normal
        try:
            boton.click()
        except:
            # Si el clic es interceptado, usar JavaScript como último recurso
            self.driver.execute_script("arguments[0].click();", boton)



    #    self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #    boton = self.driver.find_element(By.XPATH, xpath)
    #    self.driver.execute_script("arguments[0].scrollIntoView();", boton)
    #    boton.click()

    def get_texto(self):
        desc_product = self.wait.until(EC.visibility_of_element_located(self.texto_localizador))
        return desc_product.text

    def add_product_by_name(self, product_name: str):
        add_button = (By.XPATH, f"//button[@id='add-to-cart-{product_name}']")
        self.click(add_button)

    def add_product_by_name(self, product_name: str):
        add_button = (By.XPATH, f"//button[@id='add-to-cart-{product_name}']")
        self.click(add_button)

    def remove_product_by_name(self, product_name: str):
        remove_button = (By.XPATH, f"//button[@id='remove-{product_name}']")
        self.click(remove_button)

    def go_to_shopping_cart(self):
        self.click(self.CART_LINK)