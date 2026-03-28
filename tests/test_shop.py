import time
from selenium import webdriver
from pages.shop_page import ShopPage
from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage
from tests.test_login import login_page


def test_shop():
    driver = webdriver.Chrome()
    login_page = LoginPage(driver)
    login_page.go_to_login()
    login_page.login("johndoe@example.com", "admin123")

    shop_page = ShopPage(driver)
    shop_page.go_to_shop()

    age_verification_page = AgeVerificationPage(driver)
    age_verification_page.handle_age_verification("01-01-1990")


    shop_page.add_to_cart("Celery", 1)
    time.sleep(5)


