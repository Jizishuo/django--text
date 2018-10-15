from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.urls import reverse
import random
from django.contrib.auth.models import User
from .models import ShahuType, Location, Shahu
from .forms import ShahuForm
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm
from appuser.models import Profile, Friends, Fans

#分页
def get_shahu_list_common_date(request,shahus_all_list,):
    paginator = Paginator(shahus_all_list, settings.EACH_PAGE_NUMBER)  # 没几页一次分页
    page_num = request.GET.get('page',1) #获取url的页面参数（GET请求）
    page_of_shahus = paginator.get_page(page_num)
    currentr_page_num = page_of_shahus.number  # 获取当前页吗
    # 获取当前页码前后2页
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)  # 在第一个位置加上1
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取日期分类对应的数量
    '''shahu_dates = Shahu.objects.datetimes('created_time', 'day', order='DESC')
    #print(shahu_dates)
    shahu_dates_dict = {}
    for shahu_date in shahu_dates:
        shahu_count = Shahu.objects.filter(created_time__month=shahu_date.month,\
                                         created_time__day = shahu_date.day).count()
        shahu_dates_dict[shahu_date] = shahu_count
        shahu = Shahu.objects.filter(created_time__month=shahu_date.month,\
                                    created_time__day = shahu_date.day).first()
        #print(shahu.created_time)
        #print(shahu)'''
    context = {}


    context['shahus'] = page_of_shahus.object_list

    context['page_of_shahus'] = page_of_shahus

    context['page_range'] = page_range
    context['shahu_types'] = ShahuType.objects.annotate(shahu_count=Count('shahu'))#对应分类的数量
    context["Locations"] = Location.objects.annotate(shahu_count=Count('shahu'))

    context["Shahu_type_len"] = ShahuType.objects.count()
    context["Location_len"] = Location.objects.count()


    #context['shahu_dates'] = shahu_dates_dict
    return context

#获取随机推荐10条
def get_shahu_random():
    if Shahu.objects.count() <= 10:
        shahu_random_list =Shahu.objects.all()
    else:
        shahu_random = random.sample(list(Shahu.objects.all()), 10)
        #print(shahu_random)
        shahu_random_list = shahu_random
    return shahu_random_list

def shahu_list(request):
    Shahu_list = Shahu.objects.all()
    context = get_shahu_list_common_date(request, Shahu_list)

    #发布傻乎表单
    context['shahu_form'] = ShahuForm()


    return render(request, "home/shahu_list.html", context)


def shahu_detail(request, shahu_pk):
    shahu = get_object_or_404(Shahu, pk=shahu_pk)
    read_cookie_key = read_statistics_once_read(request, shahu)

    context = {}
    context["shahu_random"] = get_shahu_random()
    context['next_shahu'] = Shahu.objects.filter(created_time__lt=shahu.created_time).first()
    context['previous_shahu'] = Shahu.objects.filter(created_time__gt=shahu.created_time).last()
    #评论数量//自定义temlate也可以实现
    shahu_content_type = ContentType.objects.get_for_model(Shahu)
    context["comnent_num"] = Comment.objects.filter(content_type=shahu_content_type, object_id=shahu_pk).count()

    context['shahu'] = shahu
    response = render(request, 'home/shahu_detail.html',context)
    response.set_cookie(read_cookie_key, 'true') #阅读cookie标记
    return response

def shauhus_with_type(request, shahu_type_pk):
    shahu_type = get_object_or_404(ShahuType, pk=shahu_type_pk)
    shahus_all_list = Shahu.objects.filter(shahu_type=shahu_type)
    context = get_shahu_list_common_date(request, shahus_all_list)
    context['shahu_type'] = shahu_type
    #发布傻乎表单
    context['shahu_form'] = ShahuForm()
    return render(request, 'home/shahu_type.html', context)


def shauhus_location(request,location_pk):
    location_type = get_object_or_404(Location, pk=location_pk)
    shahus_all_list = Shahu.objects.filter(location=location_type)
    context = get_shahu_list_common_date(request, shahus_all_list)
    context['location_type'] = location_type
    #发布傻乎表单
    context['shahu_form'] = ShahuForm()
    return render(request, 'home/shahu_location.html', context)


def update_shahu(request):
    #referer = request.META.get('HTTP_REFERER', reverse('home'))
    data = {}
    shahu_form = ShahuForm(request.POST, user=request.user)
    if shahu_form.is_valid():
        # 检查通过，保存数据
        shahu = Shahu()
        shahu.author = shahu_form.cleaned_data['user']
        shahu.title = shahu_form.cleaned_data['title']
        shahu.shahu_type = shahu_form.cleaned_data['shahutype']
        shahu.location = shahu_form.cleaned_data['location']
        shahu.content = shahu_form.cleaned_data['text']
        shahu.save()
        data["success"] = 'SUCCESS'
    else:
        data["error"] = 'ERROR'
    #return JsonResponse(data)
    return redirect(request.GET.get('from', reverse('home')))


def search_profile(request, user_pk):
    #profile = get_object_or_404(Profile, pk=user_pk).user
    #profile1 = Profile.objects.get(user=profile)
    user = get_object_or_404(User, pk=user_pk)
    profile = Profile.objects.get(user=user)

    #shahus_all_list = Shahu.objects.filter(author=profile)
    shahus_all_list = Shahu.objects.filter(author=user)
    context = get_shahu_list_common_date(request, shahus_all_list)

    #发布留言表单
    profile_content_type = ContentType.objects.get_for_model(user)
    data = {}
    data["content_type"] = profile_content_type.model
    data["object_id"] = user_pk
    data['reply_comment_id'] = 0
    #context['comment_form'] = CommentForm(initial=data)
    context['comments'] = Comment.objects.filter\
        (content_type=profile_content_type, object_id=user_pk, parent=None).order_by("-comment_time")

    #获取粉丝和好友
    context["profile"] = profile
    friends = Friends.objects.filter(user_type=profile)
    fans = Fans.objects.filter(user_type=profile)
    context["friends_list_len"] =friends.count()
    context["friends_list"] = friends
    context["fans_list"] = fans
    context["fans_list_len"] = fans.count()
    return render(request, 'home/search_profile.html', context)


def shahus_search(request):
    if request.method == 'POST':
        search_name = request.POST['shahus_search']
        context = {}
        context['search_name'] = search_name
        context['shahus_list_search'] = Shahu.objects.filter(content__contains=search_name)[:20]
        context['type_list_search'] = ShahuType.objects.filter(type_name__contains=search_name)

        nickname_list = Profile.objects.filter(nickname__contains=search_name)
        context["user_list_search"] = nickname_list


        context['shahu_types'] = ShahuType.objects.annotate(shahu_count=Count('shahu'))  # 对应分类的数量
        context["Locations"] = Location.objects.annotate(shahu_count=Count('shahu'))
        context["Shahu_type_len"] = ShahuType.objects.count()
        context["Location_len"] = Location.objects.count()
        # 发布傻乎表单
        context['shahu_form'] = ShahuForm()


    return render(request,'home/shahus_search.html', context)