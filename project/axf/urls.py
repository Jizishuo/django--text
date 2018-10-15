from django.urls import path
from .import views

urlpatterns = [
    path('home/',views.home, name='home'),


    path('market/<int:categoryid>/<int:cid>/<int:sortid>/', views.market, name='market'),
    path('cart/',views.cart, name='cart'),
    path('changcart/<int:flag>/', views.changcart, name='changcart'),
    path('saveorder/', views.saveorder, name='saveorder'),


    path('mine/',views.mine, name='mine'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('checkuserid/', views.checkuserid, name='checkuserid'),

    path('quit/', views.quit, name='quit'),
    path('order/',views.order, name = 'order')
]