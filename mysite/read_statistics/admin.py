from django.contrib import admin
from .models import ReadNum, ReadDetail, ReadNumAll

@admin.register(ReadNumAll)
class ReadNumAllAdmin(admin.ModelAdmin):
    list_display = ('read_num',)

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')
