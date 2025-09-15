from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def visit(self, url: str) -> None:
        self.driver.get(url)

    def click(self, locator: tuple[By, str]) -> None:
        self.wait.until(EC.element_to_be_clickable(locator))
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()

    def safe_click(self, locator: tuple[By, str]) -> None:
        # Esperar que desaparezca cualquier overlay común
        self.wait.until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "div[class*='fixed'][class*='inset-0'][class*='z-50']")
        ))
        self.click(locator)

    def type(self, locator: tuple[By, str], text: str) -> None:
        self.wait.until(EC.visibility_of_element_located(locator))
        element = self.driver.find_element(*locator)
        if not element.is_displayed() or not element.is_enabled():
            raise Exception(f"Elemento no interactuable: {locator}")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.clear()
        element.send_keys(text)

    def get_visible_element(self, locator: tuple[By, str]):
        elements = self.driver.find_elements(*locator)
        for el in elements:
            if el.is_displayed() and el.is_enabled():
                return el
        raise Exception(f"No hay elementos visibles y habilitados para: {locator}")

    def text_of_element(self, locator: tuple[By, str]) -> str:
        self.wait.until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(*locator).text

    def element_is_visible(self, locator: tuple[By, str]) -> bool:
        try:
            return self.driver.find_element(*locator).is_displayed()
        except:
            return False

