import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('headless')  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_verify_login_form_submission(driver):
    # Navigate to the URL
    driver.get("file:///C:/Users/arc/Desktop/Auto%20Selnium/sample.html")

    # Wait for the login form to be visible
    login_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#login-form"))
    )

    # Fill in the login credentials
    username_input = login_form.find_element(By.CSS_SELECTOR, "[name='username']")
    username_input.send_keys("valid_username")

    password_input = login_form.find_element(By.CSS_SELECTOR, "[name='password']")
    password_input.send_keys("valid_password")

    # Submit the form
    submit_button = login_form.find_element(By.CSS_SELECTOR, "[type='submit']")
    submit_button.click()

    # Wait for the success message to be visible
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".success-message"))
    )

    # Assert that the form submitted successfully
    assert "Form submitted successfully" in success_message.text

    # Close the browser window
    driver.quit()