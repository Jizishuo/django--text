from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import logout
import os
import time
import random
from . models import Wheel, Nav, Musbuy, Shop, MainShow, FoodTypes, Goods, User, Cart, Order
from.forms.login import LoginForm

def home(request):
    content = {}
    content['wheelsList'] = Wheel.objects.all()
    content['title'] = '首页'
    content['navList'] = Nav.objects.all()
    content['musbuyList'] = Musbuy.objects.all()

    shopList = Shop.objects.all()
    content['shop1'] = shopList[4]
    content['shop2'] = shopList[5:]
    content['shop3'] = shopList[:4]

    content['mainList'] = MainShow.objects.all()


    return render(request, 'axf/home.html', content)

def market(request, categoryid, cid, sortid):
    content = {}

    leftSoider = FoodTypes.objects.all()
    content['leftSoider'] = leftSoider
    childNamelist = []
    group = leftSoider.get(typeid=categoryid)
    arr = group.childtypenames.split('#') #用#切typeid-childtypenames 全部分类
    for str in arr:
        arr2 = str.split(':') #用 ：切 str
        obj = {'childName' : arr2[0],'childId' : arr2[1]}
        childNamelist.append(obj)
    content['childNamelist'] = childNamelist

    content['title'] = '闪送'

    #本项目子组id只有0 没有子组分类 暂不考虑
    if cid == 0:
        goodsList = Goods.objects.filter(categoryid = categoryid)
    else:
        goodsList = Goods.objects.filter(categoryid = categoryid, childcid=cid)

    #排序
    if sortid == '1':
        goodsList = goodsList.order_by('productnum')
    elif sortid =='2':
        goodsList = goodsList.order_by('price')
    elif sortid =='3':
        goodsList = goodsList.order_by('-price')


    #判断有木有登陆
    token = request.session.get("token")
    if token:
        user = User.objects.get(userToken=token)
        cartList = Cart.objects.filter(userAccount=user.userAccount)

        for p in goodsList:
            for c in cartList:
                p.num = c.productnum
                continue


    content['goodsList'] = goodsList
    content['categoryid'] = categoryid
    content['cid'] = cid
    return render(request, 'axf/market.html',content)


def cart(request):
    content = {}
    content["title"] = '购物车'
    #验证登录
    token = request.session.get("token")
    if token != None:
        user = User.objects.get(userToken=token)
        content["user"] = user

        cartslist = Cart.objects.filter(userAccount=user.userAccount)
        #print(cartslist)
        content["cartslist"] = cartslist



    return render(request, 'axf/cart.html',content)

def changcart(request, flag):
    #print(flag)
    token = request.session.get("token")
    if token == None:
        #没登陆 -1表示未登录
        return JsonResponse({"data": "-1", "status": "error"})
    #商品id
    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    #用户id
    user = User.objects.get(userToken=token)

    #判断增减删购物车操作
    if flag == 0:
        #判断库存
        if product.storenums == 0:
            return JsonResponse({"data": -2, "status": "error"})


        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            #userAccount,productid,productnum,productprice,isChose,productimg,productname,isDelete
            c = Cart.createcart(user.userAccount, productid, 1, product.price, True, \
                                product.productimg, product.productlongname, False)
            c.save()
        else:
            try:
                c = carts.get(productid=productid)
                c.productnum +=1
                c.productprice = "%.2f" %(float(product.price) * c.productnum)#保留2个小数
                c.save()
            except Cart.DoesNotExist as e:
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True,\
                                    product.productimg, product.productlongname, False)
                c.save()
        #库存减1
        product.storenums -= 1
        product.save()
        return JsonResponse({"data":c.productnum,"price":c.productprice, "status": "success"})

    elif flag == 1:
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            return JsonResponse({"data":0, "status": "success"})
        else:
            try:
                c = carts.get(productid=productid)
                c.productnum -= 1
                if c.productnum == 0:
                    c.delete()
                else:
                    c.productprice = "%.2f" % (float(product.price) * c.productnum)  # 保留2个小数
                    c.save()

            except Cart.DoesNotExist as e:
                return JsonResponse({"data": -2, "status": "success"})

        #库存减1
        product.storenums += 1
        product.save()
        return JsonResponse({"data":c.productnum,"price":c.productprice, "status": "success"})


    #有木有选中
    elif flag == 2:
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        str = ""
        if c.isChose:
            str = "√"
        return JsonResponse({"data": str, "status":"success"})
    else:
        return None


def saveorder(request):
    token = request.session.get("token")
    if token == None:
        #没登陆 -1表示未登录
        return JsonResponse({"data": "-1", "status": "error"})
    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(isChose=True)
    if carts.count() == 0:
        return JsonResponse({"data": "-1", "status": "error"})
    #创建订单
    #订单号， 用户, 进度
    oid = time.time() + random.randrange(1, 999999)#随机订单号
    oid = "%d"%oid
    o = Order.createorder(oid, user.userAccount, 0)
    o.save()
    #下单成功删除订单#木有连击删除（保留订单原始数据）
    for item in carts:
        #连击删除
        item.isDelete = True
        #保存进user
        item.ordering = oid
        item.save()
    return JsonResponse({"status": "success"})

def mine(request):
    content ={}
    content['title'] = '我的信息'
    #'userName', 'userPhone','userAdderss',\'userImg'
    username = request.session.get("username", "未登录")
    content["username"] = username
    if username != "未登录":
        user = User.objects.get(userName=username)
        content["user"] = user

    return render(request, 'axf/mine.html',content)


def login(request):
    content = {}
    content['title'] = '登录'
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            #信息没错,验证账户密码正确性
            print('&&&&&&&&&&&&&')
            nameid = forms.cleaned_data['username']
            pswd = forms.cleaned_data['passwork']
            try:
                user = User.objects.get(userAccount=nameid)
                if user.userPasswd != pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                return redirect('/login/')

            #登录成功
            user.userToken = str(time.time() + random.randrange(1, 9999999))
            user.save()

            request.session["username"] = user.userName
            request.session["token"] = user.userToken

            return redirect('/mine/')
        else:
            content['errors'] = forms.errors
    else:
        forms = LoginForm()
        content['form'] = forms
    return render(request, 'axf/login.html',content)

# 'userAccount', 'userPasswd', 'userName', 'userPhone','userAdderss',\'userImg','userRank','userToken'
def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPass")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userAccount")
        userAdderss = request.POST.get("userAdderss")
        userRank = 0 #等级一开始默认0
        #确保唯一
        userToken = str(time.time() + random.randrange(1,9999999))
        f = request.FILES["userImg"]
        userImg = os.path.join(settings.MEDIA_ROOT, userAccount + ".png")
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()

        request.session["username"] = userName
        request.session["token"] = userToken

        return redirect("/mine/")


    else:
        content = {}
        content['title'] = '注册'
        return render(request, 'axf/register.html',content)


def checkuserid(request):
    userid = request.POST.get('userid')
    try:
        user = User.objects.get(userAccount=userid)
        return JsonResponse({"data":"该用户已经被注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"可以注册","status":"success"})

#退出登录
def quit(request):
    logout(request)
    return redirect("/mine/")

def order(request):
    content = {}
    token = request.session.get("token")
    if token == None:
        #没登陆 -1表示未登录
        content["user_in"] = "error"
    else:
        user = User.objects.get(userToken=token)
        orderList = Cart.object2.filter(userAccount=user.userAccount)
        content['orderList'] = orderList
        print("33333333333333")
        print(orderList)
        print("##################")


    return render(request, 'axf/order.html',content)