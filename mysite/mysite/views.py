from django.shortcuts import render
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.core.cache import cache, caches

from home.models import ShahuType, Location, Shahu
from home.views import get_shahu_random
from read_statistics.utils import read_statistics_once_read_all, get_seven_days_read_data, get_yesterday_hot_data, get_all_hot_data
from read_statistics.models import ReadNumAll

def get_7_days_hot_shahus():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    shahus = Shahu.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title', 'author') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return shahus[:7]


def home(request):
    context = {}

    read_cookie_key = read_statistics_once_read_all(request)
    #总浏览数量
    context["read_num_all"] = ReadNumAll.objects.get().read_num
    #第一版分类
    shahu_all = Shahu.objects.all()
    context['shahu_all_num'] = shahu_all.count()
    context['shahu_types'] = ShahuType.objects.annotate(shahu_count=Count('shahu'))#对应分类的数量
    context["Locations"] = Location.objects.annotate(shahu_count=Count('shahu'))
    context["Shahu_type_len"] = ShahuType.objects.count()
    context["Location_len"] = Location.objects.count()
    #第二版
    context["shahus_new_list"] = shahu_all[:10]
    #随机推荐
    context["shahu_random"] = get_shahu_random()

    #最后一版
    shahu_content_type = ContentType.objects.get_for_model(Shahu)
    # 获取7天热门博客(数量)的缓存数据
    '''get_seven_days_read_data = cache.get('get_seven_days_read_data')
    if get_seven_days_read_data is None:
        get_seven_days_read_data = get_seven_days_read_data(shahu_content_type)
        cache.set('get_seven_days_read_data', get_seven_days_read_data, 3600)#缓存一个小时'''

    dates, read_nums = get_seven_days_read_data(shahu_content_type)
    context['dates'] = dates
    context['read_nums'] = read_nums

    # 获取7天热门博客的缓存数据
    hot_shahus_for_7_days = cache.get('hot_shahus_for_7_days')
    if hot_shahus_for_7_days is None:
        hot_shahus_for_7_days = get_7_days_hot_shahus()
        cache.set('hot_shahus_for_7_days', hot_shahus_for_7_days, 3600*12)#缓存一个小时*12

    # 获取昨天热门博客的缓存数据
    hot_shahus_for_yestoday_days = cache.get('hot_shahus_for_yestoday_days')
    if hot_shahus_for_yestoday_days is None:
        hot_shahus_for_yestoday_days = get_yesterday_hot_data(shahu_content_type)
        cache.set('hot_shahus_for_yestoday_days', hot_shahus_for_yestoday_days, 3600*12)#缓存一个小时

    # 获取全部热门博客的缓存数据
    '''get_all_hot_data = cache.get('get_all_hot_data')
    if get_all_hot_data is None:
        get_all_hot_data = get_all_hot_data(shahu_content_type)
        cache.set('get_all_hot_data', get_all_hot_data, 3600)#缓存一个小时'''



    context['get_all_hot_data'] = get_all_hot_data(shahu_content_type)
    #缓存
    context['get_7_days_hot_shahus'] = hot_shahus_for_7_days
    context['yesterday_hot_data'] = hot_shahus_for_yestoday_days
    #非缓存
    #context['get_7_days_hot_shahus'] = get_7_days_hot_shahus()
    #context['yesterday_hot_data'] = get_yesterday_hot_data(shahu_content_type)

    response = render(request, "home.html", context)
    response.set_cookie(read_cookie_key, 'true') #阅读cookie标记
    return response

