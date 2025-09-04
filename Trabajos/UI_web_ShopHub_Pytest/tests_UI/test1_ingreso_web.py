import pytest
from Trabajos.UI_web_ShopHub_Pytest.pages.base_page_ui import BasePage

from dotenv import load_dotenv
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Cargar variables del archivo .env desde la raiz
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv()

correo_cliente_antiguo = os.getenv("correo_ant")
password_cliente_antiguo = os.getenv("password_ant")

@pytest.mark.ingresoweb
def test_ingreso_web(driver):
    login = LoginPage(driver)
    login.load()