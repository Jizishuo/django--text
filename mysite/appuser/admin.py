from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Friends, Fans

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('pk', 'username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'#显示中文

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", 'user', 'nickname', 'location', 'sexo', 'userImg', 'person_content')

@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type', 'friends')

@admin.register(Fans)
class FansAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type', 'fans')
