from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pages.base_page import BasePage


class AgeVerificationPage(BasePage):
    AGE_VERIFICATION_DATE_INPUT = (By.XPATH, "//div[@class='modal-content']/input[@placeholder='DD-MM-YYYY']")
    AGE_VERIFICATION_CONFIRM_BUTTON = (By.XPATH, "//div[@class='modal-content']/button[text()='Confirm']")
    ALERT_MESSAGE = (By.XPATH, "//div[@role='status']")
    AGE_VERIFICATION_POPUP = (By.XPATH, "//h2[contains(text(), 'Age Verification')]")

    def __init__(self, driver):
        super().__init__(driver)

    def handle_age_verification(self, birth_date):
        modal = self.find_element(self.AGE_VERIFICATION_POPUP)
        if modal:
            # locate the birthdate input and enter birthdate
            birthdate_input = self.find_element(self.AGE_VERIFICATION_DATE_INPUT)
            birthdate_input.send_keys(birth_date)
            confirm_button = self.find_element(self.AGE_VERIFICATION_CONFIRM_BUTTON)
            confirm_button.click()


    def get_popup_text(self):
        """Return True if the Age Verification popup is visible, False otherwise."""
        try:
            popup = self.find_element(self.ALERT_MESSAGE)
            return popup.text
        except NoSuchElementException:
            return False
