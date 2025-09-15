import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.devtools.v137.overlay import set_show_flex_overlays
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CategoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.category_option = (By.XPATH, "//button[text()='View Details']")

    # función que nos permite esoger desde el home la opción de categoría de "Electronicos"
    def click_category_electronics(self, xpath):
        # se usa self.driver para encontrar el elemento mediante xpath
        boton_click = self.driver.find_element("xpath", xpath)
        # a continuación se buscará el argumento (arguments[0]) usando el scroll hasta ubicarlo
        self.driver.execute_script("arguments[0].scrollIntoView();", boton_click)
        boton_click.click()

    def click_detalle_electronics(self, xpath):
        option = self.wait.until(EC.element_to_be_clickable(self.category_option))
        option.click()

    def click_category_option(self):
        option = self.wait.until(EC.element_to_be_clickable(self.category_option))
        option.click()

    def click_add_to_card(self, locator):
        # Esperar a que el overlay desaparezca
        self.wait.until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "div.fixed.inset-0.z-50")
        ))
        # Scroll al botón
        element = self.driver.find_element(By.XPATH, locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # Esperar que sea clickeable y hacer clic
        self.wait.until(EC.element_to_be_clickable((By.XPATH, locator))).click()

    def click_ir_checkout(self, locator):
        option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        option.click()


