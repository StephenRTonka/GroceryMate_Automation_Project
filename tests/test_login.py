import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.constants import Config
from pages.login_page import LoginPage


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


def test_login_valid(driver, login_page):
    # Navigate to login page
    driver.get(login_page.PAGE_URL)

    # Arrange
    username = Config.VALID_USERNAME
    password = Config.VALID_PASSWORD

    # Act
    login_page.login(username, password)

    # Give the page a short moment to redirect/render
    time.sleep(2)

    # Assert — wait for visibility of logout link
    logout_link = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Log Out']"))
    )

    assert logout_link.is_displayed()
