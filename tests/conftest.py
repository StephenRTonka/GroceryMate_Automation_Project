import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage

@pytest.fixture(scope='function')
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

'''@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)'''

"""@pytest.fixture(scope='function')
def handle_age_verification(driver):
    #Reusable age verification handler
        def _verify(dob="03-03-1993"):
        driver.get("https://grocerymate.masterschool.com/store")
        age_verification_page = AgeVerificationPage(driver)
        age_verification_page.handle_age_verification(dob)
    return _verify"""


