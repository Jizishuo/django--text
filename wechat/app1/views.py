from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Show,Userinfo, Usertoken




def std(request):
    data = {}
    data["app"] = "111"
    return JsonResponse(data)


class mydispatch(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # 执行get post --之前的判断操作
        print("333")
        if request.method == "GET":
            print("3333")
        ret = super(mydispatch, self).dispatch(request, *args, **kwargs)
        print("3333")
        return ret


class sstd(mydispatch, View):

    def get(self,request, *args, **kwargs):
        data = {}
        show = Show.objects.all()
        data['count'] = show.count()

        for i in show:
            data[i.title] = i.created_time

        return JsonResponse(data)

    def post(self,request, *args, **kwargs):
        return HttpResponse("post")

    def put(self,request, *args, **kwargs):
        return HttpResponse("put")

    def delete(self,request, *args, **kwargs):
        return HttpResponse("delete")



#############################################################
from rest_framework.views import APIView
import json
from rest_framework import exceptions

class MyAuthentication(object):
    #请求前做判断（可以设置登录权限）
    def authenticate(self, request):
        token = request._request.GET.get("token")
        #获取用户名密码去数据库校验
        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败')
        #return ('alxe', None)

    def authenticate_header(self, val):
        pass

class Dogview(APIView):
    #加验证
    authentication_classes = [MyAuthentication]


    def get(self,request, *args, **kwargs):
        data = {}
        show = Show.objects.all()
        data['count'] = show.count()
        data['dog'] = 'dog'

        for i in show:
            data[i.title] = i.created_time

        return HttpResponse(json.dumps(data), status=201)

    def post(self,request, *args, **kwargs):
        return HttpResponse("创建dog")

    def put(self,request, *args, **kwargs):
        return HttpResponse("更新dog")

    def delete(self,request, *args, **kwargs):
        return HttpResponse("删除dog")




############################登录认证#################################3
import hashlib
import time

#生成token
def md5(username):
    ctime = str(time.time())
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

class Authview(APIView):

    def get(self,request, *args, **kwargs):
        data = {
            'aaa':'我是get',
        }
        return JsonResponse(data)

    def post(self,request, *args, **kwargs):
        ret = {}
        try:
            user = request._request.POST.get("username")
            pwd = request._request.POST.get("pwd")
            obj = Userinfo.objects.filter(username=user, password=pwd)
            print(user)
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "用户名或密码错误"
                print('没有样子')
            #为用户创建token
            token = md5(user)
            Usertoken.objects.update_or_create(user=obj, defaults={'token':token})
            print('创建')
            ret['token'] = token

        except Exception as e:
            ret['code'] = 1002


        return JsonResponse(ret)



##################页面权限######################
from rest_framework import exceptions

class MyAuthentication1(object):
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


class Orderview(APIView):

    #加验证
    authentication_classes = [MyAuthentication1]

    def get(self,request, *args, **kwargs):
        a = request.user  #token_obj.user
        b = request.auth  # token_obj
        #可以根据user的user_type 显示不同内容
        data = {}
        try:
            show = Show.objects.all()
            data['count'] = show.count()
            for i in show:
                data[i.title] = str(i.created_time)
        except Exception as e:
            data['code'] = 1002

        return HttpResponse(json.dumps(data), status=201)
        #return JsonResponse(data)

    def post(self,request, *args, **kwargs):
        return HttpResponse("创建dog")



######################权限###############3


class MyPermission(object):
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return True
        return True

class Orderview1(APIView):
    #用户vip， svip可以查看

    #加验证
    authentication_classes = [MyAuthentication1,]
    #加权限
    permission_classes = [MyPermission, ]

    def get(self,request, *args, **kwargs):
        '''if request.user.user_type == 3:
            return HttpResponse('无权访问')'''

        #可以根据user的user_type 显示不同内容
        data = {}
        try:
            show = Show.objects.all()
            data['count'] = show.count()
            for i in show:
                data[i.title] = str(i.created_time)
        except Exception as e:
            data['code'] = 1002

        return HttpResponse(json.dumps(data), status=201)
        #return JsonResponse(data)

    def post(self,request, *args, **kwargs):
        return HttpResponse("创建dog")


######################访问频率设置@@@@@@@@@@@@@@@@@@@@@@@@@@@

#数据可以放缓存
VISIT_RECORD = {}

class VisitThrottle(object):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        #获取用户ip
        remote_addr = request.META.get('REMOTE_ADDR')
        #print(remote_addr)
        #第一次访问
        ntime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ntime,]
            return True
        #传值给wait
        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1] < ntime-10: #10秒
            history.pop()

        if len(history) < 3:
            #加上时间
            history.insert(0, ntime)
            return True
        return False #到达访问上限不能访问

    def wait(self):
        #返回等几秒----10秒一次限制
        return 10-(time.time() - self.history[-1])

class Authview2(APIView):

    #访问次数限制(同理可以放setting全局)
    #throttle_classes = [VisitThrottle,]

    def get(self,request, *args, **kwargs):
        data = {
            'aaa':'我是get2',
        }
        return JsonResponse(data)

    def post(self,request, *args, **kwargs):
        ret = {}
        try:
            user = request._request.POST.get("username")
            pwd = request._request.POST.get("pwd")
            obj = Userinfo.objects.filter(username=user, password=pwd)
            print(user)
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "用户名或密码错误"
                print('没有样子')
            #为用户创建token
            token = md5(user)
            Usertoken.objects.update_or_create(user=obj, defaults={'token':token})
            print('创建')
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
        return JsonResponse(ret)