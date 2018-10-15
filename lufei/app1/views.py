from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

import uuid

from . models import Course, CourseDetail, Chapter, UserToken, UserInfo
from .serializers import CourseDetailSerializer, CourseSerializer
from app1.auth.auth import LoginAuth

class CourseView(APIView):
    def get(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'data': None,
        }
        try:
            pk = kwargs.get('pk')
            if pk:
                obj = CourseDetail.objects.filter(course_id = pk).first()
                ser = CourseDetailSerializer(instance=obj, many=False)
            else:
                couese = Course.objects.all()
                ser = CourseSerializer(instance=couese, many=True)  #序列化
            #print(ser.data)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取课程失败'
        return Response(ret)

class xxx(ViewSetMixin, APIView):

    def list(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'data': None,
        }
        try:
            couese = Course.objects.all()
            ser = CourseSerializer(instance=couese, many=True)  # 序列化
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取课程失败'
        return Response(ret)

    def retrieve(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'data': None,
        }
        try:
            pk = kwargs.get('pk')
            if pk:
                obj = CourseDetail.objects.filter(course_id = pk).first()
                ser = CourseDetailSerializer(instance=obj, many=False)
                ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取课程失败'
        return Response(ret)


#登录
class LoginView(APIView):
    #写在中间件了
    '''def options(self, request, *args, **kwargs):
        #进行预检
        obj = HttpResponse('')
        obj['Access-Control-Allow-Origin'] = '*'
        obj['Access-Control-Allow-Headers'] = 'Content-Type'
        return obj'''
    def post(self, request, *args, **kwargs):
        ret={'code':1000}
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        user = UserInfo.objects.filter(user=username, pwd=password).first()
        if not user:
            ret['code'] = 1001
            ret['error'] = '用户名或密码错误'
        else:
            #登陆成功
            uid = str(uuid.uuid4())#随机字符串
            UserToken.objects.update_or_create(user=user, defaults={'token':uid}) #要么创建要么更新
            ret['token'] = uid
        return Response(ret)

#登录访问页面控制
class MicroView(APIView):
    authentication_classes = [LoginAuth,]

    def get(self, request, *args, **kwargs):
        #放auth。auth认证
        '''token = request.query_params.get('token')
        username = request.query_params.get('username')
        user = UserInfo.objects.filter(user=username).first()

        obj = UserToken.objects.filter(user=user, token=token)
        if not obj:
            return Response('失败')'''
        print(request.user)
        print(request.auth)
        ret={'code': 1000, 'title':"登录才能看到这个访问"}
        return Response(ret)