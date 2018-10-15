from django.contrib import admin
from .models import Show, Userinfo,Usertoken

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', "created_time", 'last_updated_time')


@admin.register(Userinfo)
class UserinfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type', 'username', "password", 'created_time')

@admin.register(Usertoken)
class UsertokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token')