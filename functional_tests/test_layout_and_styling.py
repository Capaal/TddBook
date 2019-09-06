from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
      
class LayoutAndStylingTest(FunctionalTest):   
        
    def testLayoutAndStyling(self):
        # User vists the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # And notices the input box is nicely centered
        inputbox = self.getItemInputBox()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] /2, 512, delta=10)
        
        # Next, they start a new list, and find it centered nicely here as well
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: testing')
        inputbox = self.getItemInputBox()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] /2, 512, delta=10)
