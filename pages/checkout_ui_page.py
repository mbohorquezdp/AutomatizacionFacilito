import pytest
from pages.base_ui_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    NoSuchElementException
)

class CheckoutPage(BasePage):

    INPUT_FIRST_NAME = (By.XPATH, "//input[@placeholder='Enter your first name']")
    INPUT_LAST_NAME  = (By.XPATH, "//input[@placeholder='Enter your last name']")
    INPUT_EMAIL      = (By.XPATH, "//input[@placeholder='Enter your email address']")
    INPUT_PHONE      = (By.XPATH, "//input[@placeholder='Enter your phone number']")
    INPUT_ADDRESS    = (By.XPATH, "//input[@placeholder='Enter your street address']")
    INPUT_CITY       = (By.XPATH, "//input[@placeholder='Enter your city']")
    INPUT_CODIGO     = (By.XPATH, "//input[@placeholder='Enter ZIP code']")
    INPUT_COUNTRY    = (By.XPATH, "//input[@placeholder='Enter your country']")

    def wait_for_form_ready(self):
        """Espera que los campos clave del formulario estén presentes y visibles."""
        try:
            self.wait.until(EC.presence_of_element_located(self.INPUT_FIRST_NAME))
            self.wait.until(EC.presence_of_element_located(self.INPUT_ADDRESS))
            self.wait.until(EC.visibility_of_element_located(self.INPUT_FIRST_NAME))
        except TimeoutException:
            print("[ERROR] El formulario no se cargó completamente. Verifica el flujo de navegación.")
            raise

    def validate_all_fields_visible(self):
        """Valida que todos los campos del formulario estén visibles antes de llenarlos."""
        campos = [
            self.INPUT_FIRST_NAME,
            self.INPUT_LAST_NAME,
            self.INPUT_EMAIL,
            self.INPUT_PHONE,
            self.INPUT_ADDRESS,
            self.INPUT_CITY,
            self.INPUT_CODIGO,
            self.INPUT_COUNTRY
        ]
        for campo in campos:
            try:
                self.wait.until(EC.visibility_of_element_located(campo))
            except TimeoutException:
                print(f"[ERROR] El campo {campo} no está visible. Verifica el renderizado o el selector.")
                raise

    def fill_checkout_form(self, first_name, last_name, email, phone, address, city, zip_code, country):
        self.wait_and_type(self.INPUT_FIRST_NAME, first_name)
        self.wait_and_type(self.INPUT_LAST_NAME, last_name)
        self.wait_and_type(self.INPUT_EMAIL, email)
        self.wait_and_type(self.INPUT_PHONE, phone)
        self.wait_and_type(self.INPUT_ADDRESS, address)
        self.wait_and_type(self.INPUT_CITY, city)
        self.wait_and_type(self.INPUT_CODIGO, zip_code)
        self.wait_and_type(self.INPUT_COUNTRY, country)

    def wait_and_type(self, locator: tuple[By, str], text: str) -> None:
        """Espera que el campo esté visible, lo scrollea y escribe el texto."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            print(f"[ERROR] El campo {locator} no se volvió visible. Verifica el renderizado.")
            raise
        except NoSuchElementException:
            print(f"[ERROR] El campo {locator} no existe en el DOM. Verifica el selector.")
            raise

    def assert_field_value(self, locator: tuple[By, str], expected: str):
        """Valida que el campo tenga el valor esperado después de escribir."""
        actual = self.driver.find_element(*locator).get_attribute("value")
        assert actual == expected, f"[ERROR] El campo {locator} tiene '{actual}' en lugar de '{expected}'"

    def click_hacer_pedido(self, locator: str):
        """Hace clic en el botón de 'Place Order', manejando overlays si es necesario."""
        self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
        try:
            self.driver.find_element(By.XPATH, locator).click()
        except ElementClickInterceptedException:
            print("[INFO] Overlay detectado. Esperando que desaparezca...")
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "fixed")))
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].click();", element)
