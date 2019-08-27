from django.test import TestCase

class SmokeTest(TestCase):
    def testBadMaths(self):
        self.assertEqual(1 + 1, 3)
