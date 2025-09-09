import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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

