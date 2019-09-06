from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
    
    def testCanStartAListAndRetrieveItLater(self):
         # User hears about our app and comes to check it out.
        # They go to our homepage
        self.browser.get(self.live_server_url)
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
        inputbox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: buy peacock feathers')
        
        # There is still a text box inviting more items
        # They enter "Use peacock feathers to make a fly" 
        # (Fly fishing maybe?)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        # The page updates again with both items and still a text box
        self.waitForRowInListTable('1: buy peacock feathers')
        self.waitForRowInListTable('2: Use peacock feathers to make a fly')
        # They wonder where the site will remember the list.
        # Which is when they notice the unique URL and some instructions
        # They vist the URL to find their to-do list.

        # Satisfied, they leave.
        
    def testMultipleUsersCanStartListsAtDifferentUrls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: buy peacock feathers')
        
        uniqueListUrl = self.browser.current_url
        self.assertRegex(uniqueListUrl, '/lists/.+')    
        
        # A second user comes along to create their own list
        # First user leaves, and a second user starts their browsing
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        self.browser.get(self.live_server_url)
        # User 2 should not see any of the first user's data.
        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy peacock feathers', pageText)
        self.assertNotIn('make a fly', pageText)
        # User 2 should have their own unique URL and can add and view their own entries
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: Buy milk')
        
        secondUserListUrl = self.browser.current_url
        self.assertRegex(secondUserListUrl, '/lists/.+')
        self.assertNotEqual(secondUserListUrl, uniqueListUrl)
        
        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy peacock feathers', pageText)
        self.assertIn('Buy milk', pageText)  
