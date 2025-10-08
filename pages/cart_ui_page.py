import pytest
from pages.base_ui_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


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

    def remove(self, locator: str):
        """Hace clic en el botón 'Remove' y espera que el producto desaparezca del carrito."""
        try:
            # Esperar a que el overlay desaparezca
            self.wait.until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "div.fixed.inset-0.z-50")
            ))

            # Scroll al botón
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            # Esperar que el botón esté visible y clickeable
            self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
            element.click()

        except (TimeoutException, NoSuchElementException):
            print(f"[ERROR] No se pudo hacer clic en el botón '{locator}'. Verifica el selector.")
            raise

        try:
            # Espera que el contenedor del producto desaparezca
            self.wait.until(EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'cart-item')]")
            ))
        except TimeoutException:
            print("[WARN] El producto no desapareció del carrito. Verifica si el DOM cambia tras el clic.")
            raise


