from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import re


class CheckoutPage(BasePage):
    PRODUCT_TOTAL = (By.XPATH, "//h5[contains(text(), 'Product Total:')]/following-sibling::h5[1]")
    SHIPPING_COST = (By.XPATH, "//h5[contains(text(), 'Shipment:')]/following-sibling::h5[1]")
    GRAND_TOTAL = (By.XPATH, "//h5[normalize-space(text()) = 'Total:']/following-sibling::h5[1]")
    CART_BASKET_ITEMS = (By.XPATH, "//div[@class='basket-items-container']")
    CART_ITEM_REMOVE_ICON = (By.XPATH, "//a[@class='remove-icon']")
    CART_ICON_LOCATOR = (By.XPATH, "//div[@class='headerIcon'][3]")
    def __init__(self, driver):
        super().__init__(driver)

    def _clean_price(self, price_text):
        if not isinstance(price_text, str) or not price_text:
            return 0.0

        cleaned_text = re.sub(r'[^\d.]', '', price_text).strip()

        if not cleaned_text:
            return 0.0

        try:
            return float(cleaned_text)
        except ValueError:
            return 0.0

    def get_product_total(self):
        total_text = self.find_element(self.PRODUCT_TOTAL).text
        return self._clean_price(total_text)

    def get_shipping_cost(self):
        shipping_text = self.find_element(self.SHIPPING_COST).text
        return self._clean_price(shipping_text)

    def get_grand_total(self):
        grand_text = self.find_element(self.GRAND_TOTAL).text
        return self._clean_price(grand_text)

    def is_cart_empty(self):
        try:
            cart_basket = self.find_element(self.CART_BASKET_ITEMS)
            if cart_basket:
                return False
            return True
        except Exception:
            return True

    def remove_cart_items(self):
        if not self.is_cart_empty():
            # Locate and remove items
            remove_icon_list = self.find_elements(self.CART_ITEM_REMOVE_ICON)
            if len(remove_icon_list) > 0:
                for icon in remove_icon_list:
                    icon.click()

    def open(self):
        self.find_element(self.CART_ICON_LOCATOR).click()
