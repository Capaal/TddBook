from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
        
    def testCanStartAListAndRetrieveItLater(self):
         # User hears about our app and comes to check it out.
        # They go to our homepage
        self.browser.get('http://localhost:8000')
        # They make sure this is where they want to be by checking
        # that the title mentions to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # Immediately they are invited to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEquals(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
                          
        # They enter "buy peacock feathers" into a text box (strange)
        inputbox.send_keys('buy peacock feathers')
        
        # Upon hitting enter, the page updates and lists
        #  "1: Buy peacock feathers" as a to-do list item
        inputbox.send_keys('Keys.ENTER')
        time.sleep(1)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: buy peacock feathers' for row in rows), "New to-do item did not appear in table")
        
        # There is still a text box inviting more items
        # They enter "Use peacock feathers to make a fly" 
        # (Fly fishing maybe?)
        self.fail('Finish the test more!')
        # The page updates again with both items and still a text box

        # They wonder where the site will remember the list.
        # Which is when they notice the unique URL and some instructions

        # They vist the URL to find their to-do list.

        # Satisfied, they leave.
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')

