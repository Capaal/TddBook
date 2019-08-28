from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):
    
    def testHomePageReturnsCorrectHtml(self):
        response = self.client.get('/')  
        self.assertTemplateUsed(response, 'home.html')
    
    def testRootUrlResolvesToHomePageView(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
