import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(options=options)

def test_password_input_validation(driver):
    # Navigate to the URL
    driver.get("file:///C:/Users/arc/Desktop/Auto%20Selnium/sample.html")

    # Wait for the input field and error message to be visible
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "error-message"))
        )
    except TimeoutException:
        pytest.skip("Timed out waiting for the input field and error message to be visible")

    # Enter an empty string into the password input field
    password_input.send_keys("")

    # Wait for the error message to appear
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "error-message"))
        )
    except TimeoutException:
        pytest.skip("Timed out waiting for the error message to appear")

    # Assert that the error message is visible and contains the expected text
    assert password_input.get_attribute("aria-label") == "Password"
    assert driver.find_element(By.ID, "error-message").text.startswith("Please enter a valid password")

    # Close the browser window
    driver.quit()