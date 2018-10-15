from django.urls import path
from . import views

urlpatterns = [
    path('', views.shahu_list, name='shahu_list'),
    path('<int:shahu_pk>', views.shahu_detail, name="shahu_detail"),
    path('type/<int:shahu_type_pk>', views.shauhus_with_type, name="shahus_with_type"),
    path('location/<int:location_pk>', views.shauhus_location, name="shahus_location"),
    path("update_shahu", views.update_shahu, name="update_shahu" ),
    path("search_profile/<int:user_pk>", views.search_profile, name="search_profile" ),
    #path('date/<int:month>/<int:day>', views.shahus_with_date, name="shahus_with_date"),
    path('shahus_search', views.shahus_search, name='shahus_search'),
]