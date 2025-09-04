from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  # ✅ Import correcto

def create_driver(headless: bool = False):
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument('--headless=new')

    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),  # ✅ Uso correcto
        options=options,
    )

    driver.implicitly_wait(5)
    return driver