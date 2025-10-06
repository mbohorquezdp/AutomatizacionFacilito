import time

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.shophub_commerce.registro_web import RegistroWeb

@given('usuario ingresa sus datos al formulario de la inscripción')
def step_impl(context):
    # Crear el driver se ejecutara desde $proyecto/environment.py
    context.registro_web = RegistroWeb(context.driver)
    context.registro_web.load()


@when('el usuario introduce credenciales válidas')
def step_impl(context):
    context.registro_web.ingreso_datos("Test", "QA Calidad", "mibanco.2022.4@gmail.com", "QACalidad", "Clave1234" )

@when('el usuario introduce credenciales inválidas')
def step_impl(context):
    context.registro_web.ingreso_datos("Testaaaa", "QA Calidadbbbb", "mibanco.2022.4000gmail.com", "", "Clave12347777")

@then('debería ver mensaje de registro exitoso')
def step_impl(context):
    assert context.registro_web.verificar_url_page(), "La URL no es la esperada"

@then('debería ver mensaje de registro erroneo')
def step_impl(context):
    assert context.registro_web.verificar_registro_fallido(), "El usuario no debería haber llegado a la página de éxito"






