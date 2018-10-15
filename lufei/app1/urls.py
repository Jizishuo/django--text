from django.urls import path, include
from . import views

urlpatterns = [
    #path('course/', views.CourseView.as_view()),
    #path('course/<int:pk>/', views.CourseView.as_view()),

    path('course/', views.xxx.as_view({'get':'list'})),
    path('course/<int:pk>/', views.xxx.as_view({'get':'retrieve'})),
    #登录
    path('login/', views.LoginView.as_view()),
    #登录访问页面控制
    path('micro/', views.MicroView.as_view()),
]