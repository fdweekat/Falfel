# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from models import MenuItem, UserOrders
from model_serializer import menu_item_serializer, user_orders_serializer
from django.utils import timezone
import json

# Create your tests here.

def createTestUser():
	return User.objects.create(username="test", password="123123")

def createMenuItem(itemName, description, price):
	return MenuItem.objects.create(name=itemName, description=description, price=price)

def createOrder(user, item, q):
	return UserOrders.objects.create(menu_item=item, user=user, deleviry_time=timezone.now(), quantity=q, address="aa"), 
		
class ViewTest(APITestCase):
		
	def test_no_menu_item(self):
		createTestUser()
		user = User.objects.get(username='test')
		self.client.force_authenticate(user=user)
		response = self.client.get(reverse('menuitems'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(json.loads(response.content), {"error": "empty meny"})
		
		
	def test_menu_item(self):
		user = createTestUser()
		menuItem = createMenuItem('test', 'aa', 2)
		serializer = menu_item_serializer(menuItem)
		self.client.force_authenticate(user=user)
		response = self.client.get(reverse('menuitems'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(json.loads(response.content)[0], serializer.data)
		
	
	def test_make_order(self):
		user = createTestUser()
		menuItem = createMenuItem('test', 'aa', 2)
		self.client.force_authenticate(user=user)
		response = self.client.post(reverse('order'), {
			"items" : [
					{ "item" : menuItem.itemId, "quantity": 5},
				],
			"deleviryTime": "2017-05-03T23:45:00",
			"address": "aaaa"
		}, CONTENT_TYPE="application/json", format='json')
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(json.loads(response.content), {"total": 10, "items": [{'price': 10, 'item': 1}]}) 
		self.assertEqual(UserOrders.objects.count(), 1)
		
	def test_get_history(self):
		user = createTestUser()
		menuItem = createMenuItem('test', 'aa', 4)
		self.client.force_authenticate(user=user)
		response = self.client.post(reverse('order'), {
			"items" : [
					{ "item" : menuItem.itemId, "quantity": 4},
				],
			"deleviryTime": "2017-05-03T23:45:00",
			"address": "aaaa"
		}, CONTENT_TYPE="application/json", format='json')
		
		self.assertEqual(response.status_code, 200)
		
		ordersResponse = self.client.get(reverse('order'))
		self.assertEqual(json.loads(ordersResponse.content), [{
			"id": 1,
			"deleviry_time": "2017-05-03T23:45:00Z",
			"quantity": 4,
			"address": "aaaa",
			"menu_item": {
			  "itemId": 1,
			  "name": "test",
			  "description": "aa",
			  "price": 4
			}
		}])
		
		
	def test_revenu(self):
		user = createTestUser()
		menuItem = createMenuItem('test', 'aa', 4)
		order = createOrder(user, menuItem, 2)
		datetime = timezone.now();
		response = self.client.get("/apis/revenue/%d" % datetime.year)

		expected_month = datetime.strftime("%Y-%m-01 00:00:00+00:00")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(json.loads(response.content), [{'total': 8, 'month': expected_month}])

		
	def test_best_user(self):
		user = createTestUser()
		menuItem = createMenuItem('test', 'aa', 4)
		order = createOrder(user, menuItem, 2)
		datetime = timezone.now();
		response = self.client.get("/apis/best/%d" % datetime.year)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json.loads(response.content), {'username': 'test'})
		
			
	def test_best_user(self):
		user = createTestUser()
		menuItem = createMenuItem('test', 'aa', 3)
		order = createOrder(user, menuItem, 2)
		datetime = timezone.now();
		response = self.client.get(reverse('average'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json.loads(response.content), [{'avg_spent': 6.0, 'user': '1'}])
