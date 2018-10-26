from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.mail import send_mail

from rest_framework.views import APIView
from redis import StrictRedis
from django_redis import get_redis_connection
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired #导入异常

from celery_tasks.tasks import send_register_active_email
from . models import User, Address

from utils.mixin import Loginrequiremixin   #登录控制

from apps.goods.models import GoodsSKU
from apps.order.models import OrderGoods,OrderInfo

#user/register/
class Register(APIView):
    def get(self, request, *args, **kwargs):
        #注册页面显示
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        content = {}
        #注册处理
        username = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        allow = request.POST.get('allow')

        if not all([username, email, password, cpassword, allow]):
            #数据不完整
            content['errormsg'] = '数据不完整'
            return render(request, 'register.html', content)

        #检验数据
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            content['errormsg'] = '邮箱格式不正确'
            return render(request, 'register.html', content)

        if password != cpassword:
            content['errormsg'] = '两次密码不一致不正确'
            return render(request, 'register.html', content)

        if not allow:
            content['errormsg'] = '请同意协议'
            return render(request, 'register.html', content)

        if User.objects.filter(username=username):
            content['errormsg'] = '用户名已存在'
            return render(request, 'register.html', content)



        user = User.objects.create_user(username, email, password)
        #默认激活 改为不激活
        user.is_active = 0
        user.save()

        #发送激活邮件， 包含激活连接, 加密用户的身份信息（激活token） django的SECRET_KEY 过期时间3600秒
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode('utf-8')

        send_register_active_email.delay(email, username, token)


        #发邮件
        '''
        suject = '我的商城'
        message = '<h1>%s, 欢迎成为会员</h1>请点击链接激活会员</br><a href="http://127.0.0.1:8000/user/active/%s/">点击</a>' % (username, token)
        sender = settings.EMAIL_FROM #发件人
        receiver = [email] #邮件地址列表
      
        send_mail(
            suject,
            '',
            sender,
            receiver,
            html_message=message,
            fail_silently=False
        )'''



        #回到首页
        return redirect(reverse('goods:index'))

#user/active/xxxx/
class Activeview(APIView):
    def get(self, request, *args, **kwargs):
        #用户激活
        token = kwargs['token']
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            #获取激活用户id
            user_id = info['confirm']
            #激活
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            #跳转到登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            #激活链接过期
            return HttpResponse('激活链接已过期')


#user/login/
class Login(APIView):
    def get(self, request, *args, **kwargs):
        #判断是否记住用户名cookie
        content = {}
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            content['checked'] = 'checked'
            content['username'] = username
        else:
            content['checked'] = ''
            content['username'] = ''
        return render(request, 'login.html', content)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('user_name')
        pwd = request.POST.get('password')
        remember = request.POST.get('remember')

        content = {}
        if not all([username, pwd]):
            content['errormsg'] = '数据不完整'
            return render(request, 'login.html', content)

        #django自带认证
        user = authenticate(username=username, password=pwd)
        if user is not None:
            #用户已激活
            if user.is_active:
                login(request, user)  # django自带保持登录状态
                #获取登录后要跳转的地址
                next_url = request.GET.get('next', reverse('goods:index')) #没有就是none就是反向解析首页
                
                response = redirect(next_url) #跳到首页
                #判断是否需要记住用户名
                if remember:
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                content['errormsg'] = '用户名未激活'
                return render(request, 'login.html', content)
        else:
            #用户名或密码错误
            content['errormsg'] = '用户名或密码错误'
            return render(request, 'login.html', content)


#user/loginout/
class Loginout(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('goods:index'))
        
#user/        
class Userinfoview(Loginrequiremixin, APIView):
    def get(self, request, *args, **kwargs):
        content ={}
        #用户个人信息
        user = request.user
        address = Address.object.get_default_address(user)
        content['address'] = address
        
        #用户最近浏览页面
        #sr = StrictRedis(host='127.0.0.1', port='6379', password='redis', db=4)
        con = get_redis_connection("default")
        history_key = 'history_%d' % user.id

        if user.is_authenticated:
            #已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%s' % user.id
            cart_count = conn.hlen(cart_key)
        content.update(cart_count=cart_count)

        #获取用户最新浏览的5条
        sku_list = con.lrange(history_key, 0, 4)
        #goods_li = GoodsSKU.objects.filter(id__in=sku_list)木有排序
        goods_li = []
        for i in sku_list:
            goods = GoodsSKU.objects.get(id=i)
            goods_li.append(goods)
        content['goods_li'] = goods_li
        return render(request, 'userinfo.html', content)

    def post(self, request, *args, **kwargs):
        pass

#user/order/1
class Userorderview(Loginrequiremixin, APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        #获取订单信息
        content = {}
        page = kwargs['page_id']

        orders = OrderInfo.objects.filter(user=user)
        for order in orders:
            #具体商品
            order_skus = OrderGoods.objects.filter(order=order)

            #遍历skus计算小计
            for order_sku in order_skus:
                amount = order_sku.price * order_sku.count
                order_sku.amount = amount  #动态绑定
            #绑定
            order.order_skus = order_skus
            #订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]

        #分页
        paginator = Paginator(orders, 3)
        #获取第几页数据
        try:
            page = int(page)
        except Exception as e:
            page = 1
        #大于总页数
        if page > paginator.num_pages:
            page = 1

        #获取内容
        order_page = paginator.page(page)

        num_page = paginator.num_pages #总页数
        #总页数小于5 显示全部
        if num_page <5:
            pages = range(1, num_page+1)
        #当前页是前3页 显示1-5
        elif page <= 3:
            pages = range(1,6)
        #当前页是后3页，显示-5:
        elif num_page - page <= 2:
            pages = range(num_page-4, num_page+1)
        #其他情况 当前的前后2页
        else:
            pages = range(page-2, page+2)

        content['pages'] = pages
        content['order_page'] = order_page
        content['page'] = 'order'


        return render(request, 'user_order.html', content)

#user/address
class Useradress(Loginrequiremixin, APIView):
    def get(self, request, *args, **kwargs):
        content = {}
        #获取收货地址
        user = request.user  # 获取登录用户
        '''
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            address = None
        '''
        address = Address.object.get_default_address(user)

        content['address'] =address
        return render(request, 'user_adress.html', content)

    def post(self, request, *args, **kwargs):
        receiver = request.POST.get('receiver')
        addr = request.POST.get('address')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')


        content = {}
        if not all([receiver, addr, phone]):
            content['errormsg'] = '信息不完整'
            return render(request, 'user_adress.html', content)

        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            content['errormsg'] = '手机格式不正确'
            return render(request, 'user_adress.html', content)

        if len(receiver) > 20:
            content['errormsg'] = '收货人不正确'
            return render(request, 'user_adress.html', content)
        if len(zip_code) > 6:
            content['errormsg'] = '邮编不正确'
            return render(request, 'user_adress.html', content)


        #如果用户已经有默认收货地址,用户没有默认收货地址
        user = request.user #获取登录用户
        '''try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            address = None'''
        address = Address.object.get_default_address(user)
        if address:
            is_default = False
        else:
            is_default = True

        #添加地址print(receiver, address, zip_code, phone)
        Address.objects.create(user=user, addr=addr,
                               receiver=receiver, zip_code=zip_code,
                               phone=phone, is_default=is_default)

        return redirect(reverse('user:address'))

