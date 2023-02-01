from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Menu

# Create your tests here.

class MenuTest(TestCase):
    def test_get_menu(self):
        item = str(Menu.objects.create(title='IceCream', price=100, inventory=100))
        self.assertEqual(item, 'IceCream : 100')

class MenuViewSetTest(APITestCase):
    def setUp(self):
        Menu.objects.create(title='menu1', price=100, inventory=100)
        Menu.objects.create(title='menu2', price=200, inventory=40)
        Menu.objects.create(title='menu3', price=140, inventory=70)

        self.list_url = reverse('menu-list')
        
    def test_getall(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)