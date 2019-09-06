from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError
        
class ListAndItemModelsTest(TestCase):
    
    def testGetAbsoluteUrl(self):
        aList = List.objects.create()
        self.assertEqual(aList.get_absolute_url(), f'/lists/{aList.id}/')
    
    def testCannotSaveEmptyListItems(self):
        aList = List.objects.create()
        item = Item(list=aList, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
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
        

        
