'''
@File    :   models.py
@Time    :   2021/08/11 19:13:24
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   内容模型数据
'''

from django.db import models
from django.utils.functional import cached_property
from dadmin.models import BaseModel
# Create your models here.


class CategoryModel(BaseModel):
    """文章分类"""
    name = models.CharField(
        max_length=30, verbose_name="分类名称", unique=True, help_text="分类名称")
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE,
        verbose_name="父级分类", help_text="父级分类，允许为空")
    icon = models.ImageField(
        max_length=200, upload_to="cate/icon/",
        null=True, blank=True, verbose_name="分类图标", help_text="大小为48 x 48")
    sort = models.PositiveIntegerField(default=0, verbose_name="排序")

    # TODO: Define fields here

    class Meta:
        ordering = ['-sort']
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        db_table = 'd_category'

    def __str__(self):
        return self.name


class ArticleModel(BaseModel):
    """文章内容"""
    title = models.CharField(
        max_length=60, verbose_name="标题", help_text="文章标题")
    desc = models.CharField(default="", blank=True, max_length=120,
                            verbose_name="文章描述", help_text="若为空将默认截取正文开头120个字符，请叫我贴心大哥哥！")
    cover = models.ImageField(
        max_length=200, upload_to="article/cover/", null=True, blank=True, verbose_name="图文封面")
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, verbose_name="文章分类", help_text="文章所属分类")
    content = models.TextField(verbose_name="文章内容", help_text="文章图文详情")
    is_banner = models.BooleanField(
        default=False, verbose_name="是否Banner", help_text="是否Banner")
    is_hot = models.BooleanField(
        default=False, verbose_name="是否热门", help_text="是否热门")
    is_top = models.BooleanField(
        default=False, verbose_name="是否置顶", help_text="是否热门")

    class Meta:
        ordering = ['-add_date']
        verbose_name = '文章详情'
        verbose_name_plural = verbose_name
        db_table = 'd_article'

    def __str__(self):
        return self.title

    @classmethod
    def get_hot(cls):
        # 获取所有的热门文章
        return cls.objects.filter(is_del=False, is_hot=True)

    @classmethod
    def get_hot_top(cls):
        # 获取同时为热门和置顶的文章
        return cls.objects.filter(is_del=False, is_top=True, is_hot=True)

    @classmethod
    def get_top(cls):
        # 仅获取置顶且不为热门的文章
        return cls.objects.filter(is_del=False, is_top=True, is_hot=False)

    @cached_property
    def next_article(self):
        # 下一篇，这里用到了缓存装饰器,仅为self时可用
        return self.objects.filter(id__gt=self.id, is_del=False).order_by('id').first()

    @cached_property
    def prev_article(self):
        # 上一篇
        return self.objects.filter(id__lt=self.id, is_del=False).first()

    def save(self):
        if self.desc == "":
            self.desc = self.content[:120]
        super().save()
