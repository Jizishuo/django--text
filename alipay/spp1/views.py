from django.shortcuts import render, redirect
from django.http import HttpResponse
from until.pay import AliPay
import time
from django.conf import settings

def aliPay():
    #这些可以写setting里 APP_ID...(都要大写)
    # 发送数据去支付宝接口 数据加密(商品，价格...)拼接成url
    app_id = '2016092200568136'
    # post请求，用于最后的检查
    notify_url = 'http://127.0.0.1:8000/pay_result/'
    # get请求,用于页面的跳转展示
    return_url = ''
    merchant_private_key_path = 'keys/app_private_2048.txt'
    alipay_public_key_path = 'alipay_public_2048.txt'

    obj  = AliPay(
        appid=app_id,
        app_notify_url=notify_url,#支付成功支付宝向这个url发送post请求(校验是否交易完成)
        return_url=return_url,    #支付成功，跳回来的网站地址
        app_private_key_path=merchant_private_key_path,#应用的私钥
        alipay_public_key_path=alipay_public_key_path,#支付宝公钥，验证支付宝回传消息使用
        debug=True
    )
    return obj

def index(request):
    if request.method =="GET":
        return render(request, 'index.html')

    #if request.method =='POST':
    price = float(request.POST.get('price'))#交易金额(必须是2位小数)
    shows = '充气娃娃'
    show_uuid = 'x2' +str(time.time()) #订单单号

    #发送数据去支付宝接口 数据加密(商品，价格...)拼接成url
    app_id = '2016092200568136'
    #post请求，用于最后的检查
    notify_url = 'http://127.0.0.1:8000/pay_result/'

    #get请求,用于页面的跳转展示
    return_url = ''
    merchant_private_key_path = 'keys/app_private_2048.txt'
    alipay_public_key_path = 'keys/alipay_public_2048.txt'

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,#支付成功支付宝向这个url发送post请求(校验是否交易完成)
        return_url=return_url,    #支付成功，跳回来的网站地址
        app_private_key_path=merchant_private_key_path,#应用的私钥
        alipay_public_key_path=alipay_public_key_path,#支付宝公钥，验证支付宝回传消息使用
        debug=True
    )
    #实例化具体对象--加密
    query_params = alipay.direct_pay(
        subject=shows,#商品描述
        out_trade_no=show_uuid, #用户订单
        total_amount=price #交易金额(必须是2位小数)
    )
    #拼接支付地址
    pay_url = 'https://openapi.alipaydev.com/gateway.do?{}'.format(query_params)

    return redirect(pay_url)


def result(request):
    try:
        params = request.GET.dict()
        sign = params.pop('sign', None)

        #发送数据去支付宝接口 数据加密(商品，价格...)拼接成url
        app_id = '2016092200568136'
        #post请求，用于最后的检查
        notify_url = 'http://127.0.0.1:8000/update_order/'

        #get请求,用于页面的跳转展示
        return_url = 'http://127.0.0.1:8000/pay_result/'
        merchant_private_key_path = 'keys/app_private_2048.txt'
        alipay_public_key_path = 'alipay_public_2048.txt'

        alipay = AliPay(
            appid=app_id,
            app_notify_url=notify_url,#支付成功支付宝向这个url发送post请求(校验是否交易完成)
            return_url=return_url,    #支付成功，跳回来的网站地址
            app_private_key_path=merchant_private_key_path,#应用的私钥
            alipay_public_key_path=alipay_public_key_path,#支付宝公钥，验证支付宝回传消息使用
            debug=True
        )

        status =alipay.verify(params, sign)
    except:
        status=None
    print('get验证')
    content ={}

    if status:
        content['title'] = '支付成功'
    else:
        content['title'] = '支付失败'
    return render(request, 'pay_result.html', content)

def page2(request):
    #alipay =ali()
    if request.method == 'POST':
        #检查是否支付成功
        #去请求体中获取所有返回的数据:状态/订单
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print(post_dict)

        sign = post_dict.pop('sign', None)
        #status = alipay.verify(post_dict, sign)
        #print('post验证', status)
        return HttpResponse('post返回')
    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        #status =alipay.verify(params, sign)
        print('get验证')
        return HttpResponse('get支付成功')

from django.views.decorators.csrf import csrf_exempt

#支付成功更新订单状态
@csrf_exempt#去掉csrf
def update_order(request):
    #app_notify_url = notify_url,  # 支付成功支付宝向这个url发送post请求(校验是否交易完成)
    #用修改订单状态
    #alipay =ali()
    if request.method == 'POST':
        #检查是否支付成功
        #去请求体中获取所有返回的数据:状态/订单
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print(post_dict)
        sign = post_dict.pop('sign', None)



        #发送数据去支付宝接口 数据加密(商品，价格...)拼接成url
        app_id = '2016092200568136'
        #post请求，用于最后的检查
        notify_url = 'http://127.0.0.1:8000/update_order/'

        #get请求,用于页面的跳转展示
        return_url = 'http://127.0.0.1:8000/pay_result/'
        merchant_private_key_path = 'keys/app_private_2048.txt'
        alipay_public_key_path = 'alipay_public_2048.txt'

        alipay = AliPay(
            appid=app_id,
            app_notify_url=notify_url,#支付成功支付宝向这个url发送post请求(校验是否交易完成)
            return_url=return_url,    #支付成功，跳回来的网站地址
            app_private_key_path=merchant_private_key_path,#应用的私钥
            alipay_public_key_path=alipay_public_key_path,#支付宝公钥，验证支付宝回传消息使用
            debug=True
        )




        status = alipay.verify(post_dict, sign)
        print('post验证', status)
        if status:
            #加操作-修改订单状态
            print(post_dict.get('out_trade_no'))#返回的订单号
            return HttpResponse('成功')
        else:
            return HttpResponse('失败')
    return HttpResponse('')
