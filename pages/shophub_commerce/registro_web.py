from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistroWeb:

    URL = "https://shophub-commerce.vercel.app/signup"

    def __init__(self, driver):
        self.driver = driver
        self.firstname = (By.CSS_SELECTOR, "input[id='firstName']")
        self.lastname = (By.CSS_SELECTOR, "input[id='lastName']")
        self.email = (By.CSS_SELECTOR, "input[id='email']")
        self.zipcode = (By.CSS_SELECTOR, "input[id='zipCode']")
        self.password = (By.CSS_SELECTOR, "input[id='password']")
        self.submit = (By.CSS_SELECTOR, "button[type='submit']")

    def load(self):
        # con esto vamos a ir a la url de la web
        self.driver.get(self.URL)

    def ingreso_datos(self, firstname, lastname, email, zipcode, password):
        self.driver.find_element(*self.firstname).send_keys(firstname)
        self.driver.find_element(*self.lastname).send_keys(lastname)
        self.driver.find_element(*self.email).send_keys(email)
        self.driver.find_element(*self.zipcode).send_keys(zipcode)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.submit).click()

    def verificar_url_page(self):
        WebDriverWait(self.driver, 10).until(EC.url_contains("/success"))
        return self.driver.current_url == "https://shophub-commerce.vercel.app/signup/success"

    def verificar_registro_fallido(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url != "https://shophub-commerce.vercel.app/signup/success"
        )
        return "/success" not in self.driver.current_url



