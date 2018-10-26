from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, RequestContext

import time
import os



#启动才有worker 命令celery -A celery_tasks.tasks worker -l info
#worker 端才需要加下边4句 初始化项目

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "show_daily_fresh.settings")
django.setup()

#创建一个celery对象celery_tasks.tasks名字
app = Celery('celery_tasks.tasks', broker='redis://:redis@localhost:6379/2')

#注册了才有
from apps.goods.models import IndexGoodsBanner, GoodsType, IndexPromotionBanner, IndexTypeGoodsBanner

#定义函数
@app.task
def send_register_active_email(to_email, username, token):
    # 发邮件
    suject = '我的商城'
    message = '<h1>%s, 欢迎成为会员</h1>请点击链接激活会员</br>' \
              '<a href="http://127.0.0.1:8000/user/active/%s/">点击</a>' % (username, token)
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [to_email]  # 邮件地址列表
    send_mail(
        suject,
        '',
        sender,
        receiver,
        html_message=message,
        fail_silently=False
    )
    time.sleep(5)


@app.task
def generate_static_index_html():
    #生成首页静态页面
    #获取商品种类信息
    types = GoodsType.objects.all()
    #首页轮播信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')
    #首页促销信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    #获取首页分类商品信息
    for type in types:
        #获取type种类首页分类商品图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
        
        #动态给type增加属性
        type.image_banners = image_banners
        type.title_banners = title_banners
        
    content = {}
    content['types'] = types
    content['goods_banners'] = goods_banners
    content['promotion_banners'] = promotion_banners

    #使用模板加载-定义模板上下文-模板渲染
    temp = loader.get_template('static_index_base.html')
    #context = RequestContext(request, content)
    index_static_html = temp.render(content)

    #生成首页对应的静态页面
    save_path = os.path.join(settings.BASE_DIR, 'templates\\index_celery.html')
    print(index_static_html)
    print(save_path)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(index_static_html)
