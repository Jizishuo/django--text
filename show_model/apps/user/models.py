from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from db.base_model import Basemodel


class User(AbstractUser, Basemodel):
    """用户模型类"""
    def ginerate_active_token(self):
        #生成用户签名字符串
        serializer = Serializer(settings.SECRET_KEY, 3600)#加密 过期时间秒
        info = {'confirm': self.id}
        token = serializer.dumps(info)
        return token.decode()

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    #地址模型管理器 改变原有查询集all(), 新增 增删改查操作
    def get_default_address(self, user):
        #获取用户默认收货地址
        try:
            address = self.get(user=user, is_default=True) #self.model=Address
        except self.model.DoesNotExist:
            address = None
        return address


class Address(Basemodel):
    #地址模型
    user = models.ForeignKey('user', verbose_name='所属账户', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20, verbose_name="收件人")
    addr = models.CharField(max_length=256, verbose_name='收货地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    #自定一个模型管理器
    object = AddressManager()
    
    class Mate:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name
