from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from models import MenuItem, UserOrders
from model_serializer import user_orders_serializer
import dateutil.parser
import json


ITEMS_KEY = u'items'
DELEVIRY_TIME_KEY = u'deleviryTime'
QUANTITY_KEY = u'quantity'
ITEM_KEY = u'item'
ADDRESS_KEY = u'address'
TOTAL_PRICE = "price"

class order_view(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, format=None):
		if (request.content_type.lower() == "application/json"):
			return self.__handle_request_order(request.body, request.user)

		return JsonResponse( {"error" : "wrong content type '%s'" % request.content_type})
	
	def get(self, request, format=None):
		data = UserOrders.objects.filter(user=request.user)
		serializer = user_orders_serializer(data, many=True)
		return JsonResponse(serializer.data, safe = False)

		
	def __handle_request_order(self, data, user):
		try:
			json_data = json.loads(data)
		except:
			return JsonResponse( {"error" : "Couldn't parse body request '%s'" % data})
		
		keys = json_data.keys()

		print(str(keys))
		print(str((ITEMS_KEY, DELEVIRY_TIME_KEY, ADDRESS_KEY)))
		if (any(k not in keys for k in [ITEMS_KEY, DELEVIRY_TIME_KEY, ADDRESS_KEY])):
			return JsonResponse( {"error" : "Bad json object"})

		try:
			deleviry_time = dateutil.parser.parse(json_data[DELEVIRY_TIME_KEY])
		except:
			return JsonResponse( {"error" : "Failed to parse datetime '%s'" % json_data[DELEVIRY_TIME_KEY]})


		items = json_data[ITEMS_KEY]
		sumPrice = 0
		responseItem = []

		for item in items:
			itemkeys = item.keys()
			if (any(k not in itemkeys for k in (QUANTITY_KEY, ITEM_KEY))):
				return JsonResponse( {"error" : "Bad json object"})

			menuItems = MenuItem.objects.filter(itemId = item[ITEM_KEY])
			if menuItems:
				menuItem = menuItems[0]
				price = menuItem.price * item[QUANTITY_KEY]
				responseItem.append({ITEM_KEY: item[ITEM_KEY], TOTAL_PRICE: price}) 
				sumPrice += price
				order = UserOrders(menu_item=menuItem, user=user, deleviry_time=deleviry_time, quantity=item[QUANTITY_KEY], address=json_data[ADDRESS_KEY])
				order.save()

		return JsonResponse({"total": sumPrice, "items": responseItem})         
