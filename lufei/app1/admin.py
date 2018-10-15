from django.contrib import admin
from . models import Course, Chapter, CourseDetail, UserInfo, UserToken

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course_img', 'level')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'num', 'chapter_name', 'course')


admin.site.register(CourseDetail)


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pwd')

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token')