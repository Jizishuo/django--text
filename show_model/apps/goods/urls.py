from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'), #部署path('index/',
    path('detail/<int:id>/', views.Goodsdetail.as_view(), name='detail'), #具体
    path('list/<int:type_id>/<int:page_id>/', views.Listview.as_view(), name='list'), #具体
]