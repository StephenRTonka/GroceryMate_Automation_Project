import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage
from pages.checkout_page import CheckoutPage
from pages.shop_page import ShopPage
from utils.constants import Config


@pytest.fixture
def age_verification(driver):
    return AgeVerificationPage(driver)


@pytest.fixture
def shop_page(driver):
    return ShopPage(driver)


@pytest.mark.parametrize("product_name, quantity, expect_free_shipping",
                         [
                             ("Cherries", 8, True), # product total exactly 20
                             ("Gala Apples", 6, False),
                                 ("Oranges", 1, False),
                             ("Gala Apples", 12, True),
                         ]
                         )
def test_free_shipping(driver, age_verification, product_name, quantity, expect_free_shipping):
    driver.get(LoginPage.PAGE_URL)
    login_page = LoginPage(driver)
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    shop_page = ShopPage(driver)
    shop_page.go_to_shop()

    age_verification.handle_age_verification("03-03-1993")
    checkout = shop_page.go_to_cart()
    checkout.remove_cart_items()
    shop_page.go_to_shop()
    shop_page.add_to_cart(product_name, quantity)
    checkout.open()
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(CheckoutPage.PRODUCT_TOTAL)
        )
    except TimeoutException:
        pytest.fail("Timeout: Product total element did not become visible on the checkout page.")

    product_total = checkout.get_product_total()
    shipping_cost = checkout.get_shipping_cost()
    grand_total = checkout.get_grand_total()

    if expect_free_shipping:
        assert shipping_cost == 0, f"Expected free shipping, got {shipping_cost}€"
    else:
        assert shipping_cost > 0, "Expected shipping cost to be applied"

    assert abs(grand_total - (product_total + shipping_cost)) < 0.01
