from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item

from lists.views import home_page

class HomePageTest(TestCase):
    
    def testUsesHomeTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def testCanSaveAPostRequest(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
    
    def testHomePageReturnsCorrectHtml(self):
        response = self.client.get('/')  
        self.assertTemplateUsed(response, 'home.html')
    
    def testRootUrlResolvesToHomePageView(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
class ItemModelTest(TestCase):
    
    def testSavingAndRetrievingItems(self):
        firstItem = Item()
        firstItem.text = 'The first (ever) list item'
        firstItem.save()
        
        secondItem = Item()
        secondItem.text = 'Item the second'
        secondItem.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        firstSavedItem = saved_items[0]
        secondSavedItem = saved_items[1]
        self.assertEqual(firstSavedItem.text, 'The first (ever) list item')
        self.assertEqual(secondSavedItem.text, 'Item the second')
