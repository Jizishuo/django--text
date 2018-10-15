from django.contrib import admin
from .models import ShahuType, Location, Shahu

@admin.register(ShahuType)
class ShahuTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'Location')

@admin.register(Shahu)
class ShahuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'shahu_type', 'location', 'author', 'get_read_num', 'created_time', 'last_updated_time')

    #筛选器
    list_filter = ('shahu_type', 'location') #过滤器
    search_fields = ('title', )          #搜索字段
    date_hierarchy = 'created_time'        #详细时间分层筛选