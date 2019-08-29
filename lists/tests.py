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
        
class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
        
class ListViewTest(TestCase):
    
    def testUsesListTemplate(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
        
