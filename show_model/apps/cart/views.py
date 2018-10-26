from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView

from apps.goods.models import GoodsSKU
from django_redis import get_redis_connection

from utils.mixin import Loginrequiremixin

# 购物车记录添加 更新 删除
# 记录 cart_1:{'1':2, '2':4}
# cart/add
class Gartaddview(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            # 没登录
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        sku_id = request.POST.get('sku_id')  # 商品id
        count = request.POST.get('count')  # 商品数量

        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res': 2, 'errmsg': '商品数量类型出错'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 购物车
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # 先尝试获取,拿不到None
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            # 累加购物车对应商品数量
            count += int(cart_count)
        # 设置hash--sku_id对应的数量--存在就更新 不存在就生成
        # 商品库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不住'})
        conn.hset(cart_key, sku_id, count)
        #用户购物车有几条
        total = conn.hlen(cart_key)

        return JsonResponse({'res': 5, 'message': '添加成功', 'total_count':total})

    def put(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            # 没登录
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        sku_id = request.POST.get('sku_id')  # 商品id
        count = request.POST.get('count')  # 商品数量

        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res': 2, 'errmsg': '商品数量类型出错'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        #更新购物车
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        # 商品库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不住'})

        conn.hset(cart_key, sku_id)

        #计算购物车总数量
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        return JsonResponse({'res': 5, 'msg': '更新成功', 'total_count':total_count})

    def delete(self, request, *args, **kwargs):
        #删除
        user = request.user
        if not user.is_authenticated:
            # 没登录
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        sku_id = request.DELETE.get('sku_id')  # 商品id

        if not sku_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的商品id'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        #删除
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        conn.hdel(cart_key, sku_id)

        #计算购物车总数量
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)
        return JsonResponse({'res': 3, 'msg': '删除成功','total_count':total_count})


#登录权限
class Cartinfoview(Loginrequiremixin,APIView):
    def get(self, request, *args, **kwargs):
        content = {}
        user = request.user

        #if user.is_authenticated:
        #已登录
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' % user.id
        cart_count = conn.hlen(cart_key)
        #{'商品id:商品数量,...}
        cart_dict = conn.hgetall(cart_key)

        content.update(cart_count=cart_count)#有几条

        #遍历字典
        skus = []
        total_price = 0  #总件数
        total_count = 0  #总价
        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            #计算商品的小计
            ammout = sku.price*int(count)
            #动态增加属性
            sku.ammout = int(ammout) #小计
            sku.count = int(count)   #数量
            skus.append(sku)

            #累加数量和价格
            total_count += int(count)
            total_price += int(ammout)

        content['total_price'] =total_price
        content['total_count'] = total_count
        content['skus'] = skus

        return render(request, 'cart.html', content)


