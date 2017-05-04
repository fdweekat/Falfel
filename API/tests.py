# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from models import MenuItem, UserOrders
# Create your tests here.

def createMenuItems(itemName, description, price):
	return MenuItem.objects.create(name=itemName, description=description, price=price)

class ViewTest(TestCase):
	def test_no_menu_item(self):
		a = reverse('/apis/menuitems', ('method' , 'GET'))
		response = self.client.get(a)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response, "[]")
		