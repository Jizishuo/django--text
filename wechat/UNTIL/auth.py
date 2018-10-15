
from app1.models import Usertoken
from rest_framework import exceptions

#######################认证#############################

#内置的认证类
from rest_framework.authentication import BaseAuthentication
'''
BaseAuthentication
class BaseAuthentication(object):
    #认证前
    def authenticate(self, request):
        raise exceptions.AuthenticationFailed('要改 不然会报错')
    #认证错误后返回的头部
    def authenticate_header(self, val):
        pass
'''

class MyAuthentication2(BaseAuthentication):
    #请求前做判断（可以设置登录权限）
    def authenticate(self, request):
        token = request._request.GET.get("token")
        token_obj = Usertoken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        #在fest feamework内部会将2个字段赋值给request,以供后续操作
        return (token_obj.user, token_obj)

    def authenticate_header(self, val):
        pass







