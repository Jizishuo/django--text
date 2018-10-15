from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

from .models import Blog
from .tasks import sendmail  # 引用tasks.py文件的中sendmail方法
import json


def home(request):
    # 耗时任务，发送邮件（用delay执行方法）
    sendmail.delay('test@test.com')

    # 其他行为
    data = list(Blog.objects.values('caption'))
    return HttpResponse(json.dumps(data), content_type='application/json')


#缓存实例
from django.core.cache import cache
import time

def get_readed_cache():
    # 判断键是否存在
    key = 'readed'
    if cache.has_key(key):
        data = cache.get(key)
    else:
        # 不存在，则获取数据，并写入缓存
        data = get_readed_data()
        # 写入缓存
        cache.set(key, data, 3600 - int(time.time() % 3600))
    return data


def get_readed_data():
    # 日期处理
    import datetime
    now = datetime.datetime.now()
    date_end = datetime.datetime(now.year, now.month, now.day, 0, 0)
    item_num = 14
    #获取数据
    # 阅读排行
    '''readed_1 = readed_list(date_end, 1, item_num)
    readed_7 = readed_list(date_end, 7, item_num)
    readed_30 = readed_list(date_end, 30, item_num)
    data = [readed_1, readed_7, readed_30]'''
    data = {}
    return data

from django.shortcuts import render_to_response

def test(request):
    data = {}
    data["read_lists"] = get_readed_cache()
    return render_to_response('index.html', data)


#redis装饰器缓存
from django.core.cache import cache


# 获取redis缓存的装饰器
def redis_cache(key, timeout):
    def __redis_cache(func):
        def warpper(*args, **kw):
            # 判断缓存是否存在
            print('check key: %s' % key)
            if cache.has_key(key):
                print('get cache')
                data = cache.get(key)
            else:
                # 若不存在则执行获取数据的方法
                # 注意返回数据的类型(字符串，数字，字典，列表均可)
                print('get data')
                data = func(*args, **kw)
                print('set cache')
                cache.set(key, data, timeout)
            return data
        return warpper
    return __redis_cache
#使用
#键值为test，超时时间为60秒
@redis_cache('test', 60)
def get_test_data():
    # 获取Blog模型随机排序前3条数据
    # (Blog模型是我自己的模型，具体代码根据自己需求获取数据)
    # values执行结果，将返回一个字典。字典可以直接存入redis
    data = Blog.objects.values('id', 'caption').order_by('?')[:3]
    return data