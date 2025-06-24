import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def to_snake_case(name):
    """Converts a string to a valid Python identifier in snake_case."""
    return "".join(c if c.isalnum() else "_" for c in name).lower()

def generate_selenium_code(story, test_steps):
    """
    Generates Python Selenium code from a user story and structured test steps.
    """
    title = story.get("title", "unnamed_story")
    test_func_name = f"test_{to_snake_case(title)}"

    code = [
        "import pytest",
        "from selenium import webdriver",
        "from selenium.webdriver.common.by import By",
        "from selenium.webdriver.support.ui import Select",
        "from selenium.webdriver.support.ui import WebDriverWait",
        "from selenium.webdriver.support import expected_conditions as EC",
        "",
        f"# User Story: {story.get('title')}",
        f"# Description: {story.get('description')}",
        "",
        "@pytest.fixture",
        "def driver():",
        "    driver = webdriver.Chrome()",
        "    yield driver",
        "    driver.quit()",
        "",
        f"def {test_func_name}(driver):",
    ]

    for step in test_steps:
        action = step.get("action")
        details = step.get("details")
        
        code.append(f"    # {action}")

        if action == "navigate":
            code.append(f'    driver.get("{details}")')
        elif action == "click":
            code.append(f'    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "{details}"))).click()')
        elif action == "type":
            selector = details.get("selector")
            text = details.get("text")
            code.append(f'    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "{selector}")))')
            code.append(f'    element.send_keys("{text}")')
        elif action == "select":
            selector = details.get("selector")
            value = details.get("value")
            code.append(f'    select = Select(driver.find_element(By.CSS_SELECTOR, "{selector}"))')
            code.append(f'    select.select_by_value("{value}")')
        elif action == "assert_text":
            code.append(f'    assert "{details}" in driver.page_source')
        elif action == "assert_element":
            code.append(f'    assert driver.find_element(By.CSS_SELECTOR, "{details}").is_displayed()')
        
        code.append("")

    return "\n".join(code)