from rest_framework import serializers
from django.http import JsonResponse

from . models import Course, CourseDetail, Chapter

class CourseSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='get_level_display')
    class Meta:
        model = Course
        fields = ["id","title", "course_img", "level"]
        #depth = 1

class CourseDetailSerializer(serializers.ModelSerializer):
    #一对一 、、外键、、chioce
    title = serializers.CharField(source='course.title')
    img = serializers.CharField(source='course.course_img')
    level = serializers.CharField(source='course.get_level_display') #跨表
    #多对多
    recommends = serializers.SerializerMethodField()#get_recommends
    #跨多个表
    chapter = serializers.SerializerMethodField()
    class Meta:
        model = CourseDetail
        fields = ['title', 'img', 'level', 'chapter','course_slogan', 'recommends', 'why_study']
        #depth = 1

    def get_recommends(self, obj):
        #获取多个对象(所有课程)
        queryset = obj.recommend_course.all()
        return [{'id': row.id, 'title': row.title} for row in queryset]

    def get_chapter(self, obj):
        queryset = obj.course.chapter_set.all()
        return [{'id': row.id, 'name': row.chapter_name} for row in queryset]