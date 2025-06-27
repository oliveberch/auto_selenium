import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def driver():
    # Initialize the WebDriver with Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(options=options)

def test_login_form_validation(driver):
    # Navigate to the login page
    driver.get("file:///C:/Users/arc/Desktop/Auto%20Selnium/sample.html#login")

    # Wait for the username field to be clickable
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
    except TimeoutException:
        assert False, "Username field not found"

    # Fill in empty username and password fields
    username_field.send_keys("")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("")

    # Submit the login form
    driver.find_element(By.ID, "submit").click()

    # Wait for the error message to be displayed
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='error-message']"))
        )
    except TimeoutException:
        assert False, "Error message not found"

    # Assert that the error message contains both username and password fields
    assert "Username is required" in error_message.text
    assert "Password is required" in error_message.text

    # Close the WebDriver
    driver.quit()