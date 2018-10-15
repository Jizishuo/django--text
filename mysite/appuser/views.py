import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from pandocfilters import Null

from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm,\
    ChangePasswordForm, ForgotPasswordForm, ChangePersoncontentForm, ChangLocationForm
from .models import Profile, Friends, Fans
from home.models import Shahu
from comment.models import Comment
from read_statistics.models import ReadNum


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'appuser/login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            # request.user.email = email

            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = reg_form.cleaned_data['nickname_new']
            profile.save()
            # 清除session
            del request.session['register_email_code']

            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'appuser/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    try:
        user = Profile.objects.get(user=request.user)
        context = {}
        friend = Friends.objects.filter(user_type=user)
        context["friends_list"] = friend
        context["friends_list_len"] = friend.count()
        fan = Fans.objects.filter(user_type=user)
        context["fans_list"] = fan
        context["fans_list_len"] = fan.count()
        context["ChangePersoncontentForm"] = ChangePersoncontentForm()

        shahu_list = Shahu.objects.filter(author=request.user)
        context['shahu_list'] = shahu_list
        context['shahu_list_len'] = shahu_list.count()
        #改地址
        context['ChangLocationForm'] = ChangLocationForm()
        return render(request, 'appuser/user_info.html', context)
    except:
        return redirect(reverse('home'))


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'appuser/bind_email.html', context)

#发送验证码
def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生产验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))  # 随机4位
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code  # 默认有效期2个星期
            request.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码:%s' % code,
                'jizishuo@qq.com',
                [email],
                fail_silently=False
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)


def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def forgot_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'appuser/forgot_password.html', context)


def add_friends(request):
    if request.method == 'POST':
        friend_get = request.POST['add_friends']
        user_get = request.POST['add_friend_user']
        #获取profile的user
        user = Profile.objects.get(pk=user_get)
        friend = Profile.objects.get(pk=friend_get)
        print(user)
        print(friend)

        #判断是否添加过
        f_has = Friends.objects.filter(user_type=user, friends=friend)
        if f_has:
            return redirect(request.GET.get('from', reverse('home')))
        f = Friends.createfriend(user, friend)
        f.save()
        fa = Fans.createfan(friend, user)
        fa.save()
    return redirect(request.GET.get('from', reverse('home')))


def change_person_content(request):
    data = {}
    if request.method == 'POST':
        form = ChangePersoncontentForm(request.POST, user=request.user)
        if form.is_valid():
            person_content_new = form.cleaned_data['text']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.person_content = person_content_new
            profile.save()
            #data['status'] = "SUCCESS"
            #data['person_content_new'] = person_content_new
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ChangeNicknameForm()
        #data['status'] = 'ERROR'
    #return JsonResponse(data)
    return redirect(request.GET.get('from', reverse('home')))

def remove_friends(request):
    if request.method == 'POST':
        friend_get = request.POST['remove_friends']
        user_get = request.user
        #获取profile的user
        user = Profile.objects.get(user=user_get)
        friend = Profile.objects.get(pk=friend_get)

        #判断是否添加过
        f_has = Friends.objects.filter(user_type=user, friends=friend)
        if f_has:
            fan_has = Fans.objects.filter(user_type=friend, fans=user)
            if fan_has:
                fan_has.delete()
            f_has.delete()
            #return redirect(request.GET.get('from', reverse('home')))
    return redirect(request.GET.get('from', reverse('home')))


def remove_shahu(request):
    if request.method == 'POST':
        shahu_pk = request.POST['remove_shahu']
        user_get = request.user
        shahu = Shahu.objects.filter(author=user_get, pk=shahu_pk)
        shahu_type = ContentType.objects.get_for_model(Shahu)
        comment = Comment.objects.filter(content_type=shahu_type, object_id=shahu_pk)
        readnum = ReadNum.objects.filter(content_type=shahu_type, object_id=shahu_pk)
        readnum.delete()
        comment.delete()
        shahu.delete()

    return redirect(request.GET.get('from', reverse('home')))

def update_location(request):
    if request.method == 'POST':
        form = ChangLocationForm(request.POST, user=request.user)
        if form.is_valid():
            person_location_new = str(form.cleaned_data['location'])
            #print(form.cleaned_data['location'])
            #print(type(form.cleaned_data['location']))
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.location = person_location_new
            profile.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        return ChangLocationForm()
    return redirect(request.GET.get('from', reverse('home')))

def update_sexo(request):
    user_get = request.user
    profile = Profile.objects.get(user=user_get)
    if request.method == 'POST':
        sexo = request.POST['updata-sexo']
        if sexo == "男":
            profile.sexo = True
        elif sexo == "女":
            profile.sexo = False
        else:
            profile.sexo = None
        profile.save()

    return redirect(request.GET.get('from', reverse('home')))