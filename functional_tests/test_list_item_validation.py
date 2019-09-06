from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
        
class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.getItemInputBox().send_keys(Keys.ENTER)
        
        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))
        
        # She tries again with some text for the item, which now works
        self.getItemInputBox().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'  
        ))
        self.getItemInputBox().send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.getItemInputBox().send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))
        
        # And she can correct it by filling some text in
        self.getItemInputBox().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'  
        ))

        self.getItemInputBox().send_keys(Keys.ENTER)

        self.waitForRowInListTable('1: Buy milk')

        self.waitForRowInListTable('2: Make tea')
