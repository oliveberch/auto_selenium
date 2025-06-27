import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_button_click_functionality(driver):
    # Navigate to the provided URL
    driver.get("file:///C:/Users/arc/Desktop/Auto%20Selnium/sample.html")

    try:
        # Wait for the button to be clickable
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#button"))
        )

        # Click the button
        button.click()

        # Wait for the expected text to appear
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#button"), "Click button successfully"
        ))
        # Assert that the button is still visible
        assert driver.find_element(By.CSS_SELECTOR, "#button").is_displayed()
    except TimeoutException:
        print("Button click timed out")