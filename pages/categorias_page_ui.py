import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CategoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.hover_field = (By.XPATH, "//*[@id='radix-«R2bb»-trigger-radix-«Rebb»']")
        self.category_option = (By.XPATH, "//a[text()='Electronics']")

    def hover_over_field(self):
        element = self.wait.until(EC.visibility_of_element_located(self.hover_field))
        ActionChains(self.driver).move_to_element(element).perform()

    #    time.sleep(2)

    #def click_category_option(self):
    #    option = self.wait.until(EC.element_to_be_clickable(self.category_option))
    #    option.click()


    def click_category_option(self):
        self.wait.until(EC.visibility_of_element_located(self.category_option))
        option = self.driver.find_element(*self.category_option)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", option)
        time.sleep(1)
        try:
            option.click()
        except Exception as e:
            print("Clic normal falló, usando JavaScript:", e)
            self.driver.execute_script("arguments[0].click();", option)