from selenium import webdriver
import time
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        stagingServer = os.environ.get('STAGINGSERVER')
        if stagingServer:
           self.live_server_url = 'http://' + stagingServer 
        
    def tearDown(self):
        self.browser.quit()
        
    def waitForRowInListTable(self, row_text):
        startTime = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - startTime > MAX_WAIT:
                    raise e
                time.sleep(0.5)

