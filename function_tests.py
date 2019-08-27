from selenium import webdriver
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
        self.fail('Finish the Test!')
        # Immediately they are invited to enter a to-do item

        # They enter "buy peacock feathers" into a text box (strange)

        # Upon hitting enter, the page updates and lists
        #  "1: Buy peacock feathers" as a to-do list item

        # There is still a text box inviting more items
        # They enter "Use peacock feathers to make a fly" 
        # (Fly fishing maybe?)

        # The page updates again with both items and still a text box

        # They wonder where the site will remember the list.
        # Which is when they notice the unique URL and some instructions

        # They vist the URL to find their to-do list.

        # Satisfied, they leave.
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')

