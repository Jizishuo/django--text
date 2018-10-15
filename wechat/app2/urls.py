from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('user/', views.Userview.as_view(), name='uuu'),
    path('django/', views.Djangoview.as_view()),
    path('parser/', views.Parserview.as_view()),
    path('roles/', views.Roleview.as_view()),
    path('userinfo/', views.Userinfoview.as_view()),
    #url(r'^group/(?P<pk>\d+)/$', views.Gruopview.as_view(), name='gid'),#为了生成url去取个名字
    path('group/<int:pk>/', views.Gruopview.as_view(), name='gid'),#为了生成url去取个名字
    path('usergroup/', views.UserGruopview.as_view()),
    path('page1/', views.Pageview.as_view()),
    path('vv1/', views.Veview.as_view()),
    #path('vv1/', views.Veview.as_view()),
    path('vv2/', views.Ve2view.as_view({'get': 'list', 'post': 'list2'})),
    path('vv3/<int:pk>', views.Ve3view.as_view({'get': 'retrieve',\
                                                 'post': 'create',\
                                                 'delete': 'destroy',\
                                                 'put': 'update',\
                                                 'patch': 'partial_update'})),#获取单个，新建，删除，全部更新，局部更新
    path('text/', views.Textview.as_view()),
]