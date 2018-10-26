from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name="register"), #注册
    path('active/<path:token>/', views.Activeview.as_view(), name='active'), #激活
    path('login/', views.Login.as_view(), name='login'), #登录
    path('logout/', views.Loginout.as_view(), name='logout'), #注销

    path('', views.Userinfoview.as_view(), name='user'), #用户信息页面 类似装饰器登录控制
    path('order/<int:page_id>/', views.Userorderview.as_view(), name='order'),#用户中心订单页
    path('address/', views.Useradress.as_view(), name='address'),#用户中心地址页
]