from django.contrib import admin
from django.core.cache import cache

from .models import GoodsType, IndexTypeGoodsBanner, IndexGoodsBanner, IndexPromotionBanner, GoodsSKU, Goods, GoodsImage

class Basemodeladmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        #更新表就有操作
        super().save_model(request, obj, form, change)
        #发出任务 重写生成index
        #from celery_tasks.tasks import generate_static_index_html  #要在这里导入 要不然报错
        #generate_static_index_html.delay()

        #删除首页缓存(后面用户访问会有缓存生成)
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        #删除表数据也操作
        super().delete_model(request, obj)
        #from celery_tasks.tasks import generate_static_index_html
        #generate_static_index_html.delay()

        cache.delete('index_page_data')


class IndexPromotionBanneradmin(Basemodeladmin):
    pass

class IndexTypeGoodsBanneradmin(Basemodeladmin):
    pass

class IndexGoodsBanneradmin(Basemodeladmin):
    pass



admin.site.register(GoodsType)
admin.site.register(GoodsSKU)
admin.site.register(Goods)
admin.site.register(GoodsImage)

admin.site.register(IndexPromotionBanner, IndexPromotionBanneradmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBanneradmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBanneradmin)