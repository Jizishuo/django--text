from django.db import models
from db.base_model import Basemodel
from tinymce.models import HTMLField

class GoodsType(Basemodel):
    #商品模型
    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='商品类型名称')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsSKU(Basemodel):
    #商品sku模型
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品种类')
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='商品SPU')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='是否上线')

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品sku'
        verbose_name_plural = verbose_name

class Goods(Basemodel):
    #商品spu模型
    name = models.CharField(max_length=20, verbose_name='商品SPU名称')
    #富文本编辑
    detail = HTMLField(blank=True, verbose_name='商品详情')

    class Meta:
        db_table = 'df_goods_spu'
        verbose_name = '商品spu'
        verbose_name_plural = verbose_name

class GoodsImage(Basemodel):
    #商品图片模型
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='goods', verbose_name='图片路径')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(Basemodel):
    #首页轮播图
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name

class IndexTypeGoodsBanner(Basemodel):
    #首页分类商品展示模型
    DISPLAY_TYPE_CHOICES = (
        (0, '标题'),
        (1, '图片'),
    )
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品类别')
    sku = models.ForeignKey('GoodsSKU',on_delete=models.CASCADE, verbose_name='商品SKU')
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES)
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_tyep_goods'
        verbose_name = '主页分类展示商品'
        verbose_name_plural = verbose_name

class IndexPromotionBanner(Basemodel):
    #首页促销活动模型
    name = models.CharField(max_length=20, verbose_name='活动名称')
    #url = models.URLField(verbose_name='活动链接')
    url = models.CharField(max_length=256, verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = '主页促销活动'
        verbose_name_plural = verbose_name

