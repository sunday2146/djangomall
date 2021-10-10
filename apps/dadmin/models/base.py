'''
@File    :   models.py
@Time    :   2021/08/09 16:07:11
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   models基类
'''
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BaseModel(models.Model):
    """模型基类"""
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="用户", help_text="用户")
    add_date = models.DateTimeField("添加时间", auto_now_add=True)
    pub_date = models.DateTimeField("更新时间", auto_now=True)
    is_del = models.BooleanField(
        default=False, verbose_name="是否删除", help_text="删除标记")
    is_show = models.BooleanField(
        default=True, verbose_name="是否显示", help_text="是否显示")

    # TODO: Define fields here

    class Meta:
        abstract = True


class Banner(BaseModel):
    img = models.ImageField(
        max_length=200, upload_to="banners/", null=True, blank=True, verbose_name="轮播图")
    url = models.CharField('跳转链接', max_length=100,
                           help_text="轮播图跳转地址，请以'http://'  或 'https://' 开头")
    desc = models.CharField('banner说明', max_length=100, blank=True, default="")
    sort = models.PositiveIntegerField(default=0, verbose_name="排序")

    class Meta:
        ordering = ['-sort']
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        db_table = 'd_banner'

    def __str__(self) -> str:
        return f'{self.desc}=>{self.url}'

    @classmethod
    def get_banners_json(cls):
        banners = cls.objects.filter(is_del=False, is_show=True)
        import json
        from django.core import serializers
        json_data = serializers.serialize("json", banners)
        json_data = json.loads(json_data)
        # from django.http import JsonResponse
        # return JsonResponse(json_data, safe=False)
        navs = [nav.get('fields', None) for nav in json_data]
        for nav in json_data:
            fields = nav.get('fields', None)
            if fields:
                fields['img'] = '/media/{}'.format(fields['img'])
        return json.dumps(navs, ensure_ascii=False) 


class ADSpace(BaseModel):
    """广告位

    Args:
        BaseModel ([model]): [模型基类]

    Returns:
        [str]: [name]
    """
    name = models.CharField('广告位名称', max_length=50)
    desc = models.CharField('广告位置说明', max_length=100, blank=True, default="")

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        db_table = 'd_ad_space'

    def __str__(self) -> str:
        return self.name


class ADContent(BaseModel):
    """广告内容
    """
    class ADTextChoices(models.TextChoices):
        TEXT = 'TXT', _('文字广告')
        IMAGE = 'IMG', _('图片广告')
        HTML = 'HTML', _('富文本广告')

    ad_choices = models.CharField(
        max_length=5,
        choices=ADTextChoices.choices,
        default=ADTextChoices.IMAGE,
        verbose_name="广告类型"
    )
    ad_space = models.ForeignKey(
        ADSpace, 
        null=True, 
        blank=True,
        on_delete=models.CASCADE, 
        verbose_name="广告位", 
        help_text="广告归属于某个广告位"
    )
    text = models.CharField('文字广告', max_length=100, blank=True, default='')
    image = models.ImageField(
        max_length=200, upload_to="ad/", null=True, blank=True, verbose_name="图片广告")
    content = models.TextField('富文本广告', blank=True, default='')
    url = models.URLField('广告链接', max_length=200, blank=True,
                          default='', help_text="广告类型为文字或图片时的链接跳转地址")
    sort = models.PositiveIntegerField(default=0, verbose_name="排序")

    class Meta:
        ordering = ['-sort']
        verbose_name = '广告内容'
        verbose_name_plural = verbose_name
        db_table = 'd_ad_content'

    def __str__(self) -> str:
        return self.text
