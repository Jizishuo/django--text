from django.urls import path
from . import views


urlpatterns = [
    path('', views.std, name='std'),
    path('std/', views.sstd.as_view()),
    path('dog/', views.Dogview.as_view()),
    path('auth/', views.Authview.as_view()),
    path('order/', views.Orderview.as_view()),
    path('order1/', views.Orderview1.as_view()),
    path('auth2/', views.Authview2.as_view()),
]
