from .base_page_ui import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    # Esta es la url que escogimos para que nuestras pruebas
    URL = "https://shophub-commerce.vercel.app/login"
    # Selectores
    Input_usarname = (By.ID, "//*[@id="email"]")
    Input_password = (By.ID, "//*[@id='password']")
    Buton_login = (By.CSS_SELECTOR, "[type="submit"]")

    #Acciones
    def load




