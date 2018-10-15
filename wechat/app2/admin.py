from django.contrib import admin
from .models import Userinfomsg, UserGroup, Role, Usertokenmsg

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


@admin.register(Userinfomsg)
class UserinfomsgAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type', 'username', "password", 'created_time','group')

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(Usertokenmsg)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'token',)