from django.middleware.csrf import CsrfViewMiddleware

#中间件
class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

#自定义中间件 -- 解决跨域
class CORSmiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        #添加响应头 名称xxx 值为bbb 的响应头 response['xxx'] = 'bbb'
        #允许访问 response['Access-Control-Allow-Origin'] = '*' 允许所有 、、、或'http://127.0.0.1:8000/，....'
        #允许你的域名来获取我的数据
        response['Access-Control-Allow-Origin'] = '*'
        response['xxx'] = 'bbb'

        #复杂的请求再加
        #允许你携带Content-Type请求头
        #response['Access-Control-Allow-Headers'] = 'Content-Type,'

        #允许你发送delete,put请求
        #response['Access-Control-Allow-Methods'] = 'DELETE, PUT,'

        return response
