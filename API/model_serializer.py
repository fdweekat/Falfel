from rest_framework import serializers
from models import UserOrders, MenuItem

class menu_item_serializer(serializers.ModelSerializer):
	
	class Meta:
		model = MenuItem
		fields = ('itemId', 'name', 'description', 'price')
	

class user_orders_serializer(serializers.ModelSerializer):
	class Meta:
		model = UserOrders
		exclude = ('user',)
		depth = 2
		

class revenue_serializer(serializers.Serializer):
	total = serializers.IntegerField(required=False)
	month = serializers.CharField(required=False, allow_blank=True, max_length=200)
	

class avg_spent_serializer(serializers.Serializer):
	avg_spent = serializers.FloatField(required=False)
	user = serializers.CharField(required=False, allow_blank=True, max_length=200)
	
	
class TestSerializer(serializers.Serializer):
	log_text = serializers.CharField(required=False, allow_blank=True, max_length=100)