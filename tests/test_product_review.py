import time

import pytest
from selenium.webdriver.common.by import By
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


def test_onestar_review(driver, login_page, age_verification, shop_page, product_page):
    driver.get(LoginPage.PAGE_URL)
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    shop_page.go_to_shop()
    age_verification.handle_age_verification("03-03-1993")

    product_page.open_product()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/product/")
    )

    if not product_page.is_already_reviewed():
        review_msg = "Poor quality, very disappointed."
        product_page.submit_one_star_review(review_msg)
        assert product_page.is_review_added()


@pytest.mark.parametrize("product, stars, review_text", [
    ("Ginger", 1, "Poor Quality"),
    ("Kale", 2, "Fair quality"),
    ("Nectarines", 5, "Delicious")
])
def test_review(product, stars, review_text, driver, login_page, age_verification, shop_page, product_page):
    driver.get(LoginPage.PAGE_URL)
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    shop_page.go_to_shop()
    age_verification.handle_age_verification("03-03-1993")

    product_page.open_specific_product(product)

    WebDriverWait(driver, 10).until(
        EC.url_contains("/product/")
    )
    time.sleep(2)

    if not product_page.is_already_reviewed():
        product_page.submit_one_star_review(review_text)
        time.sleep(4)
        assert product_page.is_review_added()


@pytest.mark.parametrize("product, review_text, expected_outcome",
                         [('Ginger', 'Nice', 'Invalid input for the field \'Rating\'.')]
                         )
def test_review_invalid(product, review_text, expected_outcome, driver, login_page, age_verification, shop_page,
                        product_page):
    driver.get(LoginPage.PAGE_URL)
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    shop_page.go_to_shop()
    age_verification.handle_age_verification("03-03-1993")

    product_page.open_specific_product(product)

    WebDriverWait(driver, 10).until(
        EC.url_contains("/product/")
    )
    time.sleep(2)
    if not product_page.is_already_reviewed():
        product_page.submit_review(0, review_text)
        assert expected_outcome in product_page.get_invalid_rating_error()


@pytest.mark.parametrize(
    "product_name, updated_number_of_stars, updated_review",
    [("Oranges", '3', 'Just normal ones'),
    ("Loose Pears", '5', 'Very good fresh Pears')]
)
def test_update_rating(driver, product_name, updated_number_of_stars, updated_review, login_page, shop_page,
                       age_verification, product_page):
    driver.get(LoginPage.PAGE_URL)
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    shop_page.go_to_shop()
    age_verification.handle_age_verification("03-03-1993")
    product_page.open_specific_product(product_name)
    if not product_page.is_product_reviewable():
        product_page.update_review(updated_number_of_stars, updated_review)
        assert product_page.is_review_added()
    else:
        pytest.skip("No existing review available")
