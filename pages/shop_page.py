from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ShopPage(BasePage):
    SHOP_LOCATOR = (By.XPATH, "//ul[@class='anim-nav']//a[@href='/store'][1]")
    CART_ICON_LOCATOR = (By.XPATH, "//div[@class='headerIcon'][3]")


    def __init__(self, driver):
        super().__init__(driver)

    def go_to_shop(self):
        self.click(self.SHOP_LOCATOR)

    @staticmethod
    def quantity_input_product(product_name):
        return (By.XPATH,
                f"//div[@class='product-card']//img[@alt='{product_name}']/ancestor::div[contains(@class,'card')]//input[@class='quantity']")

    @staticmethod
    def add_to_cart_xpath(product_name):
        return (By.XPATH,
                f"//div[@class='product-card']//img[@alt='{product_name}']/ancestor::div[contains(@class,'card')]//button[contains(text(), 'Add to Cart')]")

    def set_quantity(self, product_name, quantity):
        quantity_input_element = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable(self.quantity_input_product(product_name)))
        quantity_input_element.click()
        quantity_input_element.clear()
        quantity_input_element.send_keys(str(quantity))

    def add_to_cart(self, product_name, quantity = 1):
        add_to_cart_button = self.find_element(self.add_to_cart_xpath(product_name))
        self.set_quantity(product_name, quantity)
        add_to_cart_button.click()

    def go_to_cart(self):
        self.click(self.CART_ICON_LOCATOR)
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)