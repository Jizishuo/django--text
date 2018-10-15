from django.conf.urls import url
from snippets import views
from django.urls import path

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    path('get/', views.std.as_view()),
]