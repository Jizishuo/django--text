from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.Gartaddview.as_view(), name='cartadd'),
    path('', views.Cartinfoview.as_view(), name='cart'), #购物车页面
]