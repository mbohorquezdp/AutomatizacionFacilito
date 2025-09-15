import pytest
from pages.base_ui_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CarPage(BasePage):

    def confirmar_inicio_pago(self, locator):
        # Esperar a que el overlay desaparezca
        self.wait.until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "div.fixed.inset-0.z-50")
        ))
        # Scroll al botón
        element = self.driver.find_element(By.XPATH, locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # Esperar que sea clickeable y hacer clic
        self.wait.until(EC.element_to_be_clickable((By.XPATH, locator))).click()