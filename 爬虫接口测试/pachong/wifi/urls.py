
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Userview.as_view()),
    path('a/', views.aaa),
]