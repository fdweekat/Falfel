# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
	itemId = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=1000)
	price = models.IntegerField()
	
class UserOrders(models.Model):
	menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	deleviry_time = models.DateTimeField('date order')
	quantity = models.IntegerField()
	address = models.CharField(max_length=200)
	
	
	
