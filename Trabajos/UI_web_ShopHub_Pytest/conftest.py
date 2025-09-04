from time import sleep
import pytest
from Trabajos.Utils.driver_factory_p import create_driver

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run in headless mode (sin interfaz grafica de usuario)",
    )

@pytest.fixture
def headless(request):
    headless = request.config.getoption("--headless")
    driver = create_driver(headless=headless)
    yield driver
    driver.quit()