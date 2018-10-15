from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt#免除csrf验证
from django.views.decorators.csrf import csrf_protect #如果全局去除csrf 这个就是单独加上csrf
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

#免除csrf验证（post，。。。。）
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

#免除csrf验证
@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

#加上csrf
@csrf_protect
def ssstf(requset):
    return HttpResponse("nnn")


from django.views import View

#给下边2个继承
class mydispatch(object):
    def dispatch(self, request, *args, **kwargs):
        # 执行get post --之前的判断操作
        #print("333")
        if request.method == "GET":
            #print("3333")
            pass
        ret = super(mydispatch, self).dispatch(request, *args, **kwargs)
        #print("3333")
        return ret

class std(mydispatch,View):
    #dispath不写也可以(父类写好了)
    '''def dispatch(self, request, *args, **kwargs):
        #return HttpResponse("dispath")
        #f返回fet，post。。。。。。
        func = getattr(self, request.method.lower())
        ret = func(request, *args, **kwargs)
        return ret'''

    '''def dispatch(self, request, *args, **kwargs):
        #执行get post --之前的判断操作
        print("333")
        if request.method =="GET":
            print("3333")
        ret = super(std,self).dispatch(request, *args, **kwargs)
        print("3333")
        return ret'''

    def get(self,request, *args, **kwargs):
        return HttpResponse('GET')

    def post(self,request, *args, **kwargs):
        return HttpResponse("post")

    def put(self,request, *args, **kwargs):
        return HttpResponse("put")

    def delete(self,request, *args, **kwargs):
        return HttpResponse("delete")

class sstd(mydispatch, View):
    #dispath不写也可以(父类写好了)
    '''def dispatch(self, request, *args, **kwargs):
        #return HttpResponse("dispath")
        #f返回fet，post。。。。。。
        func = getattr(self, request.method.lower())
        ret = func(request, *args, **kwargs)
        return ret'''
    #这个请求方向单独解除csrf
    '''@method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        #执行get post --之前的判断操作
        print("333")
        if request.method =="GET":
            print("3333")
        ret = super(std,self).dispatch(request, *args, **kwargs)
        print("3333")
        return ret'''

    def get(self,request, *args, **kwargs):
        return HttpResponse('GET')


    def post(self,request, *args, **kwargs):
        return HttpResponse("post")

    def put(self,request, *args, **kwargs):
        return HttpResponse("put")

    def delete(self,request, *args, **kwargs):
        return HttpResponse("delete")

@method_decorator(csrf_exempt, name="dispath")#也行
class sssstd(mydispatch, View):

    def get(self,request, *args, **kwargs):
        return HttpResponse('GET')


    def post(self,request, *args, **kwargs):
        return HttpResponse("post")

    def put(self,request, *args, **kwargs):
        return HttpResponse("put")

    def delete(self,request, *args, **kwargs):
        return HttpResponse("delete")