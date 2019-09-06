from django.test import TestCase
from lists.models import Item, List
        
class ListAndItemModelsTest(TestCase):
    
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
        

        
