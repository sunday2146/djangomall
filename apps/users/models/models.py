from dadmin.models import BaseModel
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


class UserInfo(BaseModel):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="用户")
    mobile = models.CharField('手机号', unique=True, max_length=11)
    nickname = models.CharField('昵称', max_length=23, blank=True, default='')
    desc = models.TextField('个人简介', max_length=200, blank=True, default='')
    avatar = models.ImageField(upload_to='users/%Y/%m', max_length=100, blank=True, null=True, verbose_name = '用户头像')
    signature = models.CharField('个性签名', max_length=100, blank=True, default='')
    default_address = models.ForeignKey('DmallAddress', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name="默认地址", help_text="默认地址")
    

    class Meta:
        db_table = 'd_user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.owner.username


class DmallAddress(BaseModel):
    """用户地址"""
    province = models.CharField(max_length=100, default="", verbose_name="省份")
    city = models.CharField(max_length=100, default="", verbose_name="城市")
    district = models.CharField(max_length=100, default="", verbose_name="区域")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = models.CharField(
        max_length=100, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, verbose_name="手机号")
    email = models.EmailField(
        max_length=30, blank=True, default='', verbose_name='电子邮箱')
    is_default = models.BooleanField(default=False, verbose_name="是否设为默认收货地址")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name
        db_table = 'd_user_address'

    def __str__(self):
        return f'{self.province}{self.city}{self.district}{self.address}'