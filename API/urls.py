"""falafel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views
from order_view import order_view

urlpatterns = [
    url(r'^test/', views.example_view, name="test"),
    url(r'^menuitems/', views.get_menu_items, name="menuitems"),
    url(r'^order/', order_view.as_view(), name="order"),
    url(r'^revenue/(\d+)', views.get_revenu_report, name="revenue"),
    url(r'^best/(\d+)', views.get_best_user, name="best"),
    url(r'^avg/', views.get_avg_spent, name="average"),
]