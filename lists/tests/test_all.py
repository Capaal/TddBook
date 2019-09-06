from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item, List

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
        itemsList = List()
        itemsList.save()
        
        firstItem = Item()
        firstItem.text = 'The first (ever) list item'
        firstItem.list = itemsList
        firstItem.save()
        
        secondItem = Item()
        secondItem.text = 'Item the second'
        secondItem.list = itemsList
        secondItem.save()
        
        savedList = List.objects.first()
        self.assertEqual(savedList, itemsList)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        firstSavedItem = saved_items[0]
        secondSavedItem = saved_items[1]
        self.assertEqual(firstSavedItem.text, 'The first (ever) list item')
        self.assertEqual(firstSavedItem.list, itemsList)
        self.assertEqual(secondSavedItem.text, 'Item the second')
        self.assertEqual(secondSavedItem.list, itemsList)
        
class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        aList = List.objects.first()
        self.assertRedirects(response, f'/lists/{aList.id}/')
        
class ListViewTest(TestCase):
    
    def testPassesCorrectListToTemplate(self):
        otherList = List.objects.create()
        correctList = List.objects.create()
        response = self.client.get(f'/lists/{correctList.id}/')
        self.assertEqual(response.context['list'], correctList)
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
    
    def testUsesListTemplate(self):
        aList = List.objects.create()
        response = self.client.get(f'/lists/{aList.id}/')
        self.assertTemplateUsed(response, 'list.html')
        
class NewItemTest(TestCase):
    
    def testCanSaveAPOSTRequestToAnExistingList(self):
        otherList = List.objects.create()
        correctList = List.objects.create()
        
        self.client.post(f'/lists/{correctList.id}/add_item', data={'item_text': 'A new item for an existing list'})
        
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new item for an existing list')
        self.assertEqual(newItem.list, correctList)
        
    def testRedirectsToListView(self):
        otherList = List.objects.create()
        correctList = List.objects.create()
        
        response = self.client.post(f'/lists/{correctList.id}/add_item', data = {'item_text': 'A new item for an existing list'})
        
        self.assertRedirects(response, f'/lists/{correctList.id}/')
