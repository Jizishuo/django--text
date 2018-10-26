from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    #path('place', views.Orderview.as_view(), name='place'),
    url(r'^place$', views.Orderview.as_view(), name='place'),
    path('commit/', views.Ordercommitview.as_view(), name='commit') #订单创建
]