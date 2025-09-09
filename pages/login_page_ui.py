from .base_page_ui import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    # Esta es la url para que acceder a ingresar a la web.
    URL = "https://shophub-commerce.vercel.app/login"
    # Selectores
    Input_usarname = (By.XPATH, '//*[@id="email"]')
    Input_password = (By.XPATH, '//*[@id="password"]')
    Buton_login = (By.CSS_SELECTOR, '[type="submit"]')

    #Acciones
    def load(self):
        self.visit(self.URL)

    def login_as_user(self, username: str, password: str):
        self.type(self.Input_usarname, username)
        self.type(self.Input_password, password)
        self.click(self.Buton_login)

    #def assert_login_title(self):
    #    assert "Swag Labs" in self.driver.title




