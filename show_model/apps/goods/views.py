from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.cache import cache
from django_redis import get_redis_connection
from django.core.paginator import Paginator

from .models import IndexGoodsBanner, GoodsType, IndexPromotionBanner, IndexTypeGoodsBanner, GoodsSKU
from apps.order.models import OrderGoods
from rest_framework.views import APIView

#index/
class index(APIView):
    def get(self, request, *args, **kwargs):
        #尝试获取缓存数据
        content = cache.get('index_page_data')
        if content is None:  #没有数据
            print('缓存______________________')
            # 获取商品种类信息
            types = GoodsType.objects.all()
            # 首页轮播信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')
            # 首页促销信息
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

            # 获取首页分类商品信息
            for type in types:
                # 获取type种类首页分类商品图片展示信息
                image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                # 获取type种类首页分类商品文字展示信息
                title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

                # 动态给type增加属性 首页分类图片文字信息
                type.image_banners = image_banners
                type.title_banners = title_banners

            content = {}
            content['types'] = types
            content['goods_banners'] = goods_banners
            content['promotion_banners'] = promotion_banners

            #设置缓存key, value, time
            cache.set('index_page_data', content, 60*60)

        #获取用户购物商品
        user = request.user
        cart_count = 0

        if user.is_authenticated:
            #已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%s' % user.id
            cart_count = conn.hlen(cart_key)

        content.update(cart_count=cart_count)

        return render(request, 'index.html', content)

#detail/<int:id>
class Goodsdetail(APIView):
    def get(self, request, *args, **kwargs):
        content = {}
        goods_id = kwargs['id']
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index'))
        #获取商品分类信息
        types = GoodsType.objects.all()

        #获取商品评论信息
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        new_sku = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        #获取用户购物商品
        user = request.user
        cart_count = 0

        if user.is_authenticated:
            #已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%s' % user.id
            cart_count = conn.hlen(cart_key)

            #添加进浏览记录
            conn = get_redis_connection('default')
            history_key = 'history_%d' % user.id
            conn.lrem(history_key, 0, goods_id) #移除列表里的id
            conn.lpush(history_key, goods_id)   #从左侧插入
            #只保存用户最新浏览的5条
            conn.ltrim(history_key, 0, 4)

        content.update(cart_count=cart_count)

        content['goods'] = sku
        content['types'] = types
        content['sku_orders'] = sku_orders
        content['new_sku'] = new_sku
        return render(request, 'detail.html',content)
    



#list/种类id/页码/排序方式
#list?type=x&id=xx...
class Listview(APIView):
    def get(self, request, *args, **kwargs):
        type_id = kwargs['type_id']
        page_id = kwargs['page_id']
        content = {}
        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            return redirect(reverse("goods:index"))

        #购物车

        user = request.user
        cart_count = 0
        if user.is_authenticated:
            #已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%s' % user.id
            cart_count = conn.hlen(cart_key)
        content.update(cart_count=cart_count)

        #获取商品分类信息
        types = GoodsType.objects.all()
        #新品推荐
        new_sku = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]
        
        #排序方式
        #sort=default 默认id排序
        #price 价格, hot 销量排序
        sort = request.GET.get('sort')
        if sort == 'price':
            goods_by = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == 'hot':
            goods_by = GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:   #sort == 'default':
            sort = 'default'
            goods_by = GoodsSKU.objects.filter(type=type).order_by('-id')

        #分页
        paginator = Paginator(goods_by, 1) #分一页

        #获取第几页数据
        try:
            page = int(page_id)
        except Exception as e:
            page = 1
        #大于总页数
        if page > paginator.num_pages:
            page = 1

        goods_page = paginator.page(page)

        content['goods_page'] = goods_page
        content['new_sku'] = new_sku
        content['types'] = types #所有type
        content['type'] = type #当前页面type
        content['sort'] = sort


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
        
        return render(request, 'list.html', content)