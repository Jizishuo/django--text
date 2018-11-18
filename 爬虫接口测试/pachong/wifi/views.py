from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.http import HttpResponse
from rest_framework import exceptions
import base64

class Myauth(BaseAuthentication):

    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'').split()
        print(auth)
        print(type(auth))
        print(auth[1])
        print(type(auth[1]))

        auth_parts = base64.b64decode(auth[1].encode('utf-8')).partition(':')

        userid, password = auth_parts[0], auth_parts[2] #[1]是冒号
        print(userid, password)
        raise exceptions.AuthenticationFailed('认证失败')

    def authenticate_header(self, request):
        return 'Basic realm= "api" '

class Userview(APIView):
    authentication_classes = [Myauth,]

    def get(self, request, *args, **kwargs):
        return Response('用户列表')



def aaa(request):
    # 获取数据
    return HttpResponse('aa')