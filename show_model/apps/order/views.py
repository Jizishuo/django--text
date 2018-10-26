from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.db import transaction
from rest_framework.views import APIView
from django_redis import get_redis_connection
from datetime import datetime

from apps.goods.models import GoodsSKU
from apps.user.models import Address
from apps.order.models import OrderInfo, OrderGoods

from utils.mixin import Loginrequiremixin


# /order/place
# 登录权限
class Orderview(Loginrequiremixin, APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'ok': 'ok'})

    def post(self, request, *args, **kwargs):
        # sku_ids = request.POST.getlist('sku_ids') #[1,2]
        sku_ids = request.POST.get('sku_id')  # [1,2]

        if not sku_ids:
            return redirect(reverse("cart:cart"))

        user = request.user

        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        skus = []
        total_count = 0
        total_price = 0
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=int(sku_id))
            count = conn.hget(cart_key, sku_id)
            # 计算商品小计
            amount = sku.price * int(count)
            # 动态增加属性
            sku.count = count
            sku.amount = amount
            skus.append(sku)

            total_count += int(count)
            total_price += amount

        # 运费 直接10块钱
        transit_price = 10

        # 实践付款金额
        total_pay = total_price + transit_price

        # 获取用户地址  object 不是objects 自定义了一个属性
        addrs = Address.object.filter(user=user)

        sku_ids = ','.join(sku_id)

        content = {}
        content['skus'] = skus
        content['transit_price'] = transit_price
        content['total_count'] = total_count
        content['total_price'] = total_price
        content['total_pay'] = total_pay
        content['addrs'] = addrs
        content['sku_ids'] = sku_ids

        return render(request, 'order.html', content)


# 订单的创建(悲观锁)
# 收货地址， 支付方式，商品id，商品数量{'addr_id':addr_id, 'pay_method':pay_method,'sku_ids':sku_ids
class Ordercommitview(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接受参数
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')  # 1,2,3,

        print([addr_id, pay_method, sku_ids])

        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 支付方式
        if int(pay_method) not in OrderInfo.PAY_METHOD.keys():
            return JsonResponse({'res': 2, 'errmsg': '不存在的支付方式'})

        # 地址
        try:
            addr = Address.object.get(id=int(addr_id))  #object不用objets
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '地址没有'})

        # 创建订单
        # 订单id:201810251212+用户id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        transit_price = 10  # 运费
        total_count = 0
        total_price = 0

        #锁
        save_id = transaction.savepoint()
        try:
            order = OrderInfo.objects.create(order_id=order_id, user=user,
                                             addr=addr, pay_method=pay_method,
                                             transit_price=transit_price, total_count=total_count,
                                             total_price=total_price)

            # 从redis中获取
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id

            sku_ids = sku_ids.split(',')
            for sku_id in sku_ids:
                # 获取商品的信息
                try:
                    #加个悲观锁
                    #sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                    sku = GoodsSKU.objects.get(id=sku_id)
                except GoodsSKU.DoesNotExist:
                    return JsonResponse({'res': 4, 'errmsg': '商品不纯在'})

                count = conn.hget(cart_key, sku_id)  # 数量

                #判断库存
                if int(count) > sku.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res':8, 'errmsg':'库存不足'})

                # 加一条记录
                OrderGoods.objects.create(order=order, sku=sku, count=count, price=sku.price)  # 评论默认空

                # 更新商品库存和销量
                sku.stock -= int(count)
                sku.sales += int(count)
                sku.save()

                # 累加计算订单商品的总数量和价格
                ammount = sku.price * int(count)
                total_count += int(count)
                total_price += ammount

            # 更新订单的总数量总价
            order.total_count = total_count
            order.total_price = total_price
            order.save()

        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res':6, 'errmsg':'e'})

        #提交事务
        transaction.savepoint_commit(save_id)
        # 删除用户购物车的数据 *拆包
        conn.hdel(cart_key, *sku_ids)

        return JsonResponse({'res': 5, 'msg': '创建成功'})


class Ordercommitview1(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接受参数
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')  # 1,2,3,

        print([addr_id, pay_method, sku_ids])

        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 支付方式
        if int(pay_method) not in OrderInfo.PAY_METHOD.keys():
            return JsonResponse({'res': 2, 'errmsg': '不存在的支付方式'})

        # 地址
        try:
            addr = Address.object.get(id=int(addr_id))  # object不用objets
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '地址没有'})

        # 创建订单
        # 订单id:201810251212+用户id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        transit_price = 10  # 运费
        total_count = 0
        total_price = 0

        # 锁
        save_id = transaction.savepoint()
        try:
            order = OrderInfo.objects.create(order_id=order_id, user=user,
                                             addr=addr, pay_method=pay_method,
                                             transit_price=transit_price, total_count=total_count,
                                             total_price=total_price)

            # 从redis中获取
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id

            sku_ids = sku_ids.split(',')
            for sku_id in sku_ids:
                for i in range(3):
                    # 获取商品的信息
                    try:
                        # 加个悲观锁
                        # sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except GoodsSKU.DoesNotExist:
                        return JsonResponse({'res': 4, 'errmsg': '商品不纯在'})

                    count = conn.hget(cart_key, sku_id)  # 数量

                    # 判断库存
                    if int(count) > sku.stock:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 8, 'errmsg': '库存不足'})

                    #乐观锁
                    orgin_stock =sku.stock
                    new_stock = orgin_stock - int(count)
                    new_sales = orgin_stock + int(count)
                    #返回受影响的函数 res=0 失败(不一样)
                    #需要改mysql的隔离级别
                    #update df_goods_sku set stock=new)stock, sales=new_sales where id=sku_id and stock=orgin_stock
                    res = GoodsSKU.objects.filter(id=sku_id, stock=orgin_stock).update(stock=new_stock, sales=new_sales)
                    if res == 0 :
                        if i ==2: #第三次了
                            transaction.savepoint_rollback(save_id)
                            return JsonResponse({'res': 7, 'errmsg':'下单失败'})
                        continue  #回去继续判断

                    # 加一条记录
                    OrderGoods.objects.create(order=order, sku=sku, count=count, price=sku.price)  # 评论默认空

                    # 累加计算订单商品的总数量和价格
                    ammount = sku.price * int(count)
                    total_count += int(count)
                    total_price += ammount
                    #执行到这里 跳出循环
                    break

            # 更新订单的总数量总价
            order.total_count = total_count
            order.total_price = total_price
            order.save()

        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 6, 'errmsg': 'e'})

        # 提交事务
        transaction.savepoint_commit(save_id)
        # 删除用户购物车的数据 *拆包
        conn.hdel(cart_key, *sku_ids)

        return JsonResponse({'res': 5, 'msg': '创建成功'})