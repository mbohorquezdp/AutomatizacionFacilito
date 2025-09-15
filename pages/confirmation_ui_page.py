import pytest
from pages.base_ui_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    NoSuchElementException
)

class Confirmation(BasePage):

    def click_to_home(self, locator: str):
        """Hace clic en el botón 'Return to Home', manejando overlays y forzando el clic si es necesario."""
        try:
            # Espera que el botón esté presente, visible y clickeable
            self.wait.until(EC.presence_of_element_located((By.XPATH, locator)))
            self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))

            try:
                # Intenta clic normal
                self.driver.find_element(By.XPATH, locator).click()
            except ElementClickInterceptedException:
                print("[INFO] Overlay detectado. Esperando que desaparezca...")
                try:
                    self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "fixed")))
                except TimeoutException:
                    print("[WARN] El overlay no desapareció a tiempo. Forzando el clic igual.")
                element = self.driver.find_element(By.XPATH, locator)
                self.driver.execute_script("arguments[0].click();", element)

        except (TimeoutException, NoSuchElementException):
            print(f"[ERROR] El botón '{locator}' no está disponible o visible. Verifica el flujo.")
            raise


