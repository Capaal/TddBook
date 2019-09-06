from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List

class ItemFormTest(TestCase):
    
    def testFormItemInputHasPlaceholderAndCssClasses(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        
    def testFormValidationForBlankItems(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
        
    def testFormSaveHandlesSavingToAList(self):
        aList = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        newItem = form.save(for_list=aList)
        self.assertEqual(newItem, Item.objects.first())
        self.assertEqual(newItem.text, 'do me')
        self.assertEqual(newItem.list, aList)
