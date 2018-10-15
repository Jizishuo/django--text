from django.contrib import admin

from .models import Wheel, Nav ,Musbuy, Shop, MainShow, FoodTypes, Goods, User, Cart, Order

@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'name', 'trackid')

@admin.register(Nav)
class NavAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'name', 'trackid')

@admin.register(Musbuy)
class MusbuyAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'name', 'trackid')

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'name', 'trackid')

@admin.register(MainShow)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'trackid', 'name', 'img','categoryid','brandname',\
                    'img1','childcid1','productid1','longname1','price1','marketprice1',\
                    'img2', 'childcid2', 'productid2', 'longname2', 'price2', 'marketprice2', \
                    'img3', 'childcid3', 'productid3', 'longname3', 'price3', 'marketprice3')

@admin.register(FoodTypes)
class FoodTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'typeid', 'typename', 'typesort', 'childtypenames')


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'productid', 'productimg', 'productname', 'productlongname', 'isxf',\
                    'pmdesc','specifics', 'price', 'marketprice', 'categoryid', 'childcid',\
                    'childcidname', 'dealerid', 'storenums', 'productnum')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'userPasswd', 'userName', 'userPhone','userAdderss',\
                    'userImg','userRank','userToken')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount','productid','productnum','productprice','isChose',\
                    'productimg','productname','orderid','isDelete')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderid', 'userid', 'progress')