from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.versioning import BaseVersioning, QueryParameterVersioning, URLPathVersioning
from rest_framework.request import Request

from django.http import JsonResponse


#############自定义的版本控制########################
'''class ParaVersion(object):
    def determine_version(self,request, *args, **kwargs):
        #version = request._request.GET.get('version') #url+?version=1111
        version = request.query_params.get('version')
        return version'''

class Userview(APIView):
    #versioning_class = ParaVersion               #自定义的版本控制
    #versioning_class = QueryParameterVersioning    #模板的版本控制
    #setting 设置了全局
    def get(self,request, *args, **kwargs):
        #version = request._request.GET.get('version') #url+?version=1111
        #print(version)
        #print(request.version)    #versioning_class = ParaVersion,获取版本
        #print(request.versioning_scheme)#获取版本处理对象
        #url1 = request.versioning_scheme.reverse(viewname='uuu', request=request) #可以反向生成对应版本号的url
        #print(url1)
        data = {'aaa':'APP2-v1-v2-v3',}
        return JsonResponse(data)


################django解析器######################

class Djangoview(APIView):
    def post(self,request, *args, **kwargs):
        print(request._request.POST)
        print(request._request.body)
        #Content-Type 必须是application/X-WWW-FORM-UXXXXX(固定格式)开头
        #数据格式name=xxx&gen=222  ---   post才有值(form,ajax......),不然就在body里
        data = {'aaa':'app2-django-text，post/body'}
        return JsonResponse(data)

################rest解析器######################
from rest_framework.parsers import JSONParser,FormParser, FileUploadParser

class Parserview(APIView):
    #解析器
    #parser_classes = [JSONParser, FormParser] 放全局setting
    #用户可以发json数据，不像django的解析器
    # JSONParser只能接受json数据  application/json
    # FormParser  能接受 application/X-WWW-FORM-UXXXXX
    #FileUploadParser 上传文件 parser_classes = [FileUploadParser,]
    #Content-Type 必须是application/json开头 、、或直接json字典 {}
    def post(self,request, *args, **kwargs):
        #print(request._request.POST)
        #print(request._request.body)

        print(request.data) #parser_classes之后 发过来的数据在这里
        data = {'aaa':'app2-rest-text，post/body'}
        return JsonResponse(data)


#################序列化#####################

from .models import Role, Userinfomsg, Usertokenmsg, UserGroup
import json
from rest_framework import serializers

class Roleserializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField() #title字段和数据库一致

class Roleview(APIView):

    def get(self,request, *args, **kwargs):
        #django的方法
        roles1 = Role.objects.all().values_list('id', 'title')
        roles = list(roles1)
        ret = json.dumps(roles, ensure_ascii=False)#不给中文编码 就可以输出中文

        #rest的方法  写多一个类
        #对【obj， 多个对象】
        '''role_rest = Role.objects.all()
        ser = Roleserializer(instance=role_rest, many=True)#many表示多条数据----序列化
        ret1 = json.dumps(ser.data, ensure_ascii=False) #ser.data数据在这里 是一个字典'''

        role = Role.objects.all().first()
        ser = Roleserializer(instance=role, many=False)  # many表示单个数据----序列化
        ret1 = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret1)


class Userinfoserializer(serializers.Serializer):
    id = serializers.IntegerField()

    xxx = serializers.CharField(source='get_user_type_display') #user_type数据库查找，显示查找的对象
    group = serializers.CharField(source='group.title') #外键group.id  有点像django的连级查询 一直。。。查询下去
    #ris = serializers.CharField(source='roles.all')#查询多个结果managtomang 一般不用这个
    rls = serializers.SerializerMethodField() #自定义显示--定义一个函数---get_rls
    def get_rls(self, row):
        role_list = row.roles.all()
        ret = []
        for item in role_list:
            ret.append({'id':item.id, 'title':item.title})
        return [ret]

    username = serializers.CharField() #title字段和数据库一致
    password = serializers.CharField()

#-------------rest简化的方法-----------------
class Userinfoserializer1(serializers.ModelSerializer): #ModelSerializer继承不同类

    #为了给group-view生成url-group
    group = serializers.HyperlinkedIdentityField(
        view_name='gid',lookup_field='group_id', lookup_url_kwarg='pk')
    #查询对应的pk-group'    lookup_url_kwarg='pk' pk对应url里的pk

    class Meta:
        model = Userinfomsg
        #fields = "__all__"
        fields = ['id', 'username', 'password', 'group', 'roles']
        #depth = 1  #连级查询的深度 0-345，性能不快

class Userinfoview(APIView):
    def get(self,request, *args, **kwargs):
        userinfo = Userinfomsg.objects.all()
        ser = Userinfoserializer(instance=userinfo, many=True)#many表示多条数据----序列化
        ret = json.dumps(ser.data, ensure_ascii=False) #ser.data数据在这里 是一个字典

        return HttpResponse(ret)

    def put(self,request, *args, **kwargs):
        users = Userinfomsg.objects.all()
        ser = Userinfoserializer1(instance=users, many=True, context={'request': request})
        #many表示多条数据----序列化,context为了生成url
        ret = json.dumps(ser.data, ensure_ascii=False) #ser.data数据在这里 是一个字典
        return HttpResponse(ret)


    def post(self, request, *args, **kwargs):
        data = request.data
        return HttpResponse('2222')


#-------------rest生成 url的方法-----------------
class Groupserializer(serializers.ModelSerializer): #ModelSerializer继承不同类
    class Meta:
        model = UserGroup
        fields = "__all__"
        #depth = 0  #连级查询的深度 0-345，性能不快

class Gruopview(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = UserGroup.objects.filter(pk=pk).first()
        ser = Groupserializer(instance=obj, many=False)#many表示多条数据----序列化
        ret = json.dumps(ser.data, ensure_ascii=False) #ser.data数据在这里 是一个字典
        return HttpResponse(ret)


##############rest---请求校验##################
#自定义验证规则
class XXvalidator(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        #if value != self.base:
        if not value.startswith(self.base):
            message = '必须开头为 %s' % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializers_field):
        pass

class Usergroupview1(serializers.Serializer):
    title = serializers.CharField(error_messages={'request':'不能为空'}, validators=[XXvalidator('爸爸'),])

    def validated_title(self, value):
        print("验证") #类似form表单的验证
        return value

class UserGruopview(APIView):
    def post(self, request, *args, **kwargs):
        ser = Usergroupview1(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            print(ser.errors)
        return HttpResponse('ddd')


####################分页####################3
from UNTIL.pages import PageSerializers #序列化放那边了
from rest_framework.response import Response #rest 返回的请求（好看一点）
from rest_framework.pagination import PageNumberPagination,\
    LimitOffsetPagination, CursorPagination #分页
#自定义分页器
class MyPageNumberPagination(PageNumberPagination):
    page_size = 2 #每页几个
    page_size_query_param = 'size' #url参数名字
    max_page_size = 5 ##url参数每页几个的最大值
    page_query_param = 'page' #http://127.0.0.1:8000/app2/page1/?page=2  page的名字

class MyPageNumberPagination2(LimitOffsetPagination):#第几个位置，向后看几页
    default_limit = 2 #每页几个
    limit_query_param = 'limit' #url参数名字
    offset_query_param = 'offset'#后边第几个
    max_limit = 5 #每页最大

class MyPageNumberPagination3(CursorPagination):#加密分页
    cursor_query_param = 'cursor'
    page_size = 2 #每页几个
    ordering = '-id'#排序规则
    page_size_query_param = None #url参数名字
    max_page_size = 5 #每页最大

class Pageview(APIView):
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()

        #分页
        #pg = PageNumberPagination()
        #pg = MyPageNumberPagination()#自定义
        pg = MyPageNumberPagination2()  # 自定义
        #pg = MyPageNumberPagination3() #只有上下一页的分页（加密分页）
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        #序列化
        ser = PageSerializers(instance=page_roles, many=True)
        #return pg.get_paginated_response(ser.data) #这个返回有总页数 上下一页。。。加密分页返回
        return Response(ser.data)

#####################视图####################
from rest_framework.generics import GenericAPIView #view 不方便 继承django的view

class Veview(GenericAPIView):
    queryset = Role.objects.all()        #指定数据
    serializer_class = PageSerializers   #指定序列化
    pagination_class = PageNumberPagination #指定分页器

    def get(self, request, *args, **kwargs):
        #取数据
        roles = self.get_queryset()#取数据
        page_roles =self.paginate_queryset(queryset=roles) #分页
        # 序列化
        ser = self.get_serializer(instance=page_roles, many=True)
        return Response(ser.data)

from rest_framework.viewsets import GenericViewSet  #as_view 带参数自定义函数名 继承上边的view-GenericAPIView-django-view

class Ve2view(GenericViewSet):

    def list(self, request, *args, **kwargs):
        return Response("我是get-list")

    def list2(self, request, *args, **kwargs):
        return Response("我是post-list2")


from rest_framework.viewsets import ModelViewSet  #as_view 带参数自定义函数名 继承上边的view-GenericViewSet
from rest_framework.mixins import ListModelMixin       #ModelViewSet继承了这些类 增删改查---都有

class Ve3view(ModelViewSet):
    queryset = Role.objects.all()        #指定数据
    serializer_class = PageSerializers   #指定序列化
    pagination_class = PageNumberPagination #指定分页器



########################333####渲染器###############33
from rest_framework.renderers import JSONRenderer,AdminRenderer, BrowsableAPIRenderer   #返回json数据, 不同的界面

class Textview(APIView):
    #renderer_classes = [JSONRenderer, BrowsableAPIRenderer] #可以配全局和自定义

    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        pg = PageNumberPagination()

        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        ser = PageSerializers(instance=page_roles, many=True)
        return Response(ser.data)
