from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('el usuario ingresa a la página de login')
def step_impl(context):
    # Crear el driver se ejecutara dese $proyecto/environment.py
    context.driver = webdriver.Chrome()
    context.driver.get("https://shophub-commerce.vercel.app/signup")

@when('el usuario introduce credenciales válidas')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, "input-firstName-144").send_keys("Test")
    context.driver.find_element(By.CLASS_NAME, "input-lastName-837").send_keys("QA Calidad")
    context.driver.find_element(By.CLASS_NAME, "input-email-623").send_keys("mibanco.2022.4@gmail.com")
    context.driver.find_element(By.CLASS_NAME, "input-zipCode-544").send_keys("QA Calidad")
    context.driver.find_element(By.CLASS_NAME, "input-password-11").send_keys("Clave1234")
    context.driver.find_element(By.CLASS_NAME, "py-2 w-full").click()

@when('el usuario introduce credenciales inválidas')
def step_impl(context):
    context.driver.find_element(By.ID, "username").send_keys("invalid")
    context.driver.find_element(By.ID, "password").send_keys("invalid")
    context.driver.find_element(By.CSS_SELECTOR, "button.radius").click()

@then('debería ver la página segura')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(EC.url_contains("/success"))
    assert driver.current_url == "https://shophub-commerce.vercel.app/signup/success", "La URL no es la esperada"


