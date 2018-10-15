from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    data = {}
    data["fist"] = "111"
    return JsonResponse(data)


from rest_framework.views import APIView
from rest_framework.response import Response

class CourseView(APIView):
    def get(self, request, *args, **kwargs):
        ret = {
            'code':1000,
            'data':[
                {'id': 1, 'title': 'python全栈'},
                {'id': 2, 'title': 'linux运维'},
                {'id': 3, 'title': 'python分析'},
            ]
        }
        return Response(ret)
