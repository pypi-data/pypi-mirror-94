import pytest
from seleniumwire import webdriver


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    options.add_argument("disable-extensions")
    options.add_argument("incognito")
    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()


@pytest.mark.asyncio
async def test_selenium(driver) -> None:
    driver.get("https://www.google.com/")
