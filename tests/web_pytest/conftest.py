from time import sleep
import pytest
from utils.driver_factory import create_driver

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run in headless mode (sin interfaz grafica de usuario)",
    )

@pytest.fixture
def driver(request):
    headless = request.config.getoption("--headless")
    driver = create_driver(headless=headless)
    driver.maximize_window()
    yield driver
    sleep(3)
    driver.quit()
