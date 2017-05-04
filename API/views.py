# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import F, Count, Value, Sum, Avg, Max
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from models import MenuItem, UserOrders
from model_serializer import menu_item_serializer, revenue_serializer, avg_spent_serializer
from django.db.models.functions import TruncMonth


# Create your views here.

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_menu_items(request, format=None):
    items = MenuItem.objects.all()
    if (not items):
        return JsonResponse({"error": "empty meny"})
    
    serializer = menu_item_serializer(items, many=True)
    return JsonResponse(serializer.data, safe = False)


@api_view(['GET'])
def get_revenu_report(request, year):
    total = UserOrders.objects.filter(deleviry_time__year = year)\
            .annotate(month=TruncMonth('deleviry_time'))\
            .values('month')\
            .annotate(total=Sum(F('quantity') * F('menu_item__price')))\
            .values('month', 'total')
                        
    print(str(total))
    serializer = revenue_serializer(total, many=True)
    return JsonResponse(serializer.data, safe = False)
    
         
@api_view(['GET'])
def get_avg_spent(request):
    avg_data = UserOrders.objects\
            .values('user')\
            .annotate(avg_spent=Avg(F('quantity') * F('menu_item__price')))\
            .values('user', 'avg_spent')

    
    serializer = avg_spent_serializer(avg_data, many=True)
    return JsonResponse(serializer.data, safe = False)

@api_view(['GET'])
def get_best_user(request,year):
    data = UserOrders.objects\
            .values('user')\
            .annotate(total=Max(F('quantity') * F('menu_item__price')))\
            .values('user', 'user__username', 'total')

    print(str(data[0]['user']))
    if (not data):
        return JsonResponse({"error": "no data history"})

    response = {'username': data[0].get('user__username')}
    return JsonResponse(response, safe = False)
    
          
    
	    
        
    