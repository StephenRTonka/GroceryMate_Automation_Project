import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.constants import Config


class ProductPage(BasePage):
    PRODUCT_XPATH = (
    By.XPATH, "(//div[contains(@class,'product-card')])[1]//*[self::a or self::img or self::div[@class='card']]")
    REVIEW_CARD_XPATH = (By.XPATH, "//div[@class='new-review-card']")
    REVIEW_TEXTAREA = (By.XPATH, "//textarea[@class='new-review-form-control ']")
    SEND_BUTTON = (By.XPATH, "//button[contains(@class, 'new-review-btn-send') and contains(text(), 'Send')]")
    REVIEW_RESTRICTION_XPATH = (By.XPATH, "//div[@class='reviewRestriction']")
    MENU_ICON = (By.XPATH, "//div[@class='menu-icon']")
    EDIT_BUTTON = (By.XPATH, "//div[@class='dropdown-menu']/button[text()='Edit']")
    PRODUCT_REVIEWED_MESSAGE = (By.XPATH, "//p[contains(text(), 'You have already reviewed')]")
    INVALID_RATING = (By.XPATH, "//div[@role='status' and contains(text(), 'Invalid input for the field')]")
    EDIT_RATING_XPATH = (By.XPATH, "//div[@class='modal']//input[@type='number']")
    EDIT_COMMENT_XPATH = (By.XPATH, "//div[@class='modal']//textarea")
    SAVE_CHANGES_XPATH = (By.XPATH, "//div[@class='modal-buttons']//button[text()='Save Changes']")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_xpath(self, product):
        return (
        By.XPATH, f"//div[@class='product-card']//img[@alt='{product}']/ancestor::div[contains(@class,'product-card')]")

    def open_product(self, locator=None):
        target = locator if locator else self.PRODUCT_XPATH
        self.click(target)

    def open_specific_product(self, product):
        product_xpath = self.get_product_xpath(product)
        print(product_xpath)
        self.click(product_xpath)

    def is_already_reviewed(self):
        try:
            review_restriction = self.find_element(self.MENU_ICON)
            if review_restriction:
                return True
            else:
                return False
        except Exception:
            print("Element not found")
            return False

    def is_review_added(self):
        try:
            review_text = self.find_element(self.PRODUCT_REVIEWED_MESSAGE)
            if review_text:
                return True
        except Exception:
            print("No review found by this user")
            return False

    def is_product_reviewable(self):
        try:
            review_card = self.find_element(self.REVIEW_CARD_XPATH)
            if review_card:
                return True
            else:
                return False
        except Exception:
            return False

    def mark_stars(self, n):
        star_locator = self.get_star_xpath(n)
        self.click(star_locator)

    def get_star_xpath(self, n):
        return (By.XPATH, f"//div[@class='interactive-rating']/span[{n}]")

    def submit_one_star_review(self, review_text):
        self.mark_stars(1)
        self.enter_text(self.REVIEW_TEXTAREA, review_text)
        self.click(self.SEND_BUTTON)

    def submit_review(self, number_of_stars, review_text):
        if number_of_stars != 0:
            self.mark_stars(number_of_stars)
        self.enter_text(self.REVIEW_TEXTAREA, review_text)
        self.click(self.SEND_BUTTON)

    def get_invalid_rating_error(self):
        invalid_rating_element = self.find_element(self.INVALID_RATING)
        return invalid_rating_element.text

    def update_review(self, rating, comment=''):
        self.find_element(self.MENU_ICON).click()
        self.click(self.EDIT_BUTTON)
        rating_input = self.find_element(self.EDIT_RATING_XPATH)
        comment_input = self.find_element(self.EDIT_COMMENT_XPATH)
        save_changes_button = self.find_element(self.SAVE_CHANGES_XPATH)
        time.sleep(3)
        rating_input.clear()
        rating_input.send_keys(rating)
        comment_input.clear()
        comment_input.send_keys(comment)
        save_changes_button.click()
        time.sleep(2)
