import time
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
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


#使用内置
class VisitThrottle2(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        #获取用户ip
        #remote_addr = request.META.get('REMOTE_ADDR')
        remote_addr = self.get_ident(request) #内置
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


#使用内置 key在缓存里
#匿名用户访问控制
class VisitThrottle3(SimpleRateThrottle):
    scope = 'zishuo' #随便定义的字符串 以后当key使用 配置在setting里的
    #必须写的方法
    def get_cache_key(self, request, view):
        #获取ip 也可以其他
        return self.get_ident(request)

#登录用户访问控制
class UserThrottle(SimpleRateThrottle):
    scope = 'zishuo-1' #随便定义的字符串 以后当key使用 配置在setting里的
    #必须写的方法
    def get_cache_key(self, request, view):
        #获取username 也可以其他
        return request.user.username