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

def test_help_button_functionality(driver):
    # Navigate to the application URL
    driver.get("file:///C:/Users/arc/Desktop/Auto%20Selnium/sample.html#help")

    try:
        # Wait for the login button to be clickable
        help_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='help-button']"))
        )
        
        # Click the 'Help' button
        help_button.click()
        
        # Wait for the help message to appear
        help_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='help-message']"))
        )
        
        # Assert that the help message contains login instructions
        assert "Login Instructions" in help_message.text
        
    except TimeoutException:
        pytest.fail("Timed out waiting for the 'Help' button to be clickable or the help message to appear")
    
    finally:
        driver.quit()