from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


from app1.models import UserInfo, UserToken


#登录认证的页面
class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        username = request.query_params.get('username')
        user = UserInfo.objects.filter(user=username).first()

        obj = UserToken.objects.filter(user=user, token=token).first()
        if not obj:
            #return Response('失败')
            raise AuthenticationFailed({'code': 1001, 'error':'需要登录才能访问'})
        return (obj.user.user, obj)