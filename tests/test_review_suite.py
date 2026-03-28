import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage
from utils.constants import Config


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def age_verification(driver):
    return AgeVerificationPage(driver)


@pytest.fixture
def shop_page(driver):
    return ShopPage(driver)


@pytest.fixture
def product_page(driver):
    return ProductPage(driver)


# --- Test 1: Simple One Star Review ---
def test_onestar_review(driver, login_page, age_verification, shop_page, product_page):
    driver.get(LoginPage.PAGE_URL)
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    shop_page.go_to_shop()
    age_verification.handle_age_verification("03-03-1993")

    product_page.open_product()

    WebDriverWait(driver, 10).until(EC.url_contains("/product/"))

    product_page.submit_one_star_review("Poor quality, very disappointed.")
    assert product_page.is_review_added()


# --- Test 2: Simple Review Update ---
def test_update_rating(driver, login_page, shop_page, age_verification, product_page):
    driver.get(LoginPage.PAGE_URL)
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    shop_page.go_to_shop()
    age_verification.handle_age_verification("03-03-1993")

    product_page.open_specific_product("Oranges")

    WebDriverWait(driver, 10).until(EC.url_contains("/product/"))

    product_page.update_review(1, 'Updated review: Still not good')
    assert product_page.is_review_added()


# --- Test 3: Invalid Rating Check ---
def test_review_invalid(driver, login_page, shop_page, age_verification, product_page):
    driver.get(LoginPage.PAGE_URL)
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    shop_page.go_to_shop()
    age_verification.handle_age_verification("03-03-1993")

    product_page.open_specific_product("Ginger")

    WebDriverWait(driver, 10).until(EC.url_contains("/product/"))

    product_page.submit_review(0, "Nice")
    error_msg = product_page.get_invalid_rating_error()
    assert "Invalid input" in error_msg