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

def test_successful_login(driver):
    # Navigate to the login page
    driver.get("file:///C:/Users/arc/Desktop/Auto%20Selnium/sample.html#login")

    try:
        # Wait for the username input field to be clickable
        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#username"))
        )

        # Enter correct username and password
        username_input.send_keys("your_username")
        password_input = driver.find_element(By.CSS_SELECTOR, "#password")
        password_input.send_keys("your_password")

        # Click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#login"))
        )
        login_button.click()

        # Wait for the login success message to be displayed
        login_success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".login-success-message"))
        )

        # Assert that the login success message is displayed
        assert login_success_message.text == "Login successful"

    except TimeoutException:
        pytest.fail("Timed out waiting for elements to be clickable")

    finally:
        driver.quit()