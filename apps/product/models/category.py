from django.db import models
from dadmin.models import BaseModel


class ProductCategory(BaseModel):
    """商品分类"""
    name = models.CharField(max_length=30, unique=True,
                            verbose_name="分类名称", help_text="分类名称")
    desc = models.CharField(max_length=100, blank=True, default='', verbose_name="分类说明", 
        help_text="顶级分类请务必填写，字数限制在8个字，否则PC端楼层显示会有问题！")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_cate',
                               on_delete=models.CASCADE, verbose_name="父级分类", help_text="父级分类，允许为空")
    icon = models.ImageField(max_length=200, upload_to="product/icon/",
                             null=True, blank=True, verbose_name="分类图标", help_text="大小为48 x 48")
    pc_img = models.ImageField(max_length=200, upload_to="product/pc/icon/",
                               null=True, blank=True, verbose_name="PC分类图", help_text="大小为468 x 340")
    is_nav = models.BooleanField(
        default=False, verbose_name="是否导航", help_text="是否在导航栏显示")
    sort = models.PositiveIntegerField(default=0, verbose_name="排序")

    class Meta:
        ordering = ['-sort']
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        db_table = 'd_product_category'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        # 获取导航
        parents = cls.objects.filter(
            is_del=False, is_show=True, parent=None, is_nav=True)
        db_keys = []
        db_values = []
        for cate in parents:
            db_keys.append(cate)
            db_values.append(cate.sub_cate.filter(
                is_del=False, is_show=True, is_nav=True))
        navs = dict(map(lambda x, y: [x, y], db_keys, db_values))
        return navs


class CategoryAD(BaseModel):
    """PC首页楼层分类广告
    """
    image = models.ImageField(max_length=200, upload_to="product/pc/ad/",
                               null=True, blank=True, verbose_name="PC端楼层广告", help_text="大小为468 x 340")
    desc = models.CharField(max_length=100, verbose_name="位置说明", help_text="广告位所在的位置说明,第一个显示在楼层中间！")
    url = models.URLField(max_length=200, verbose_name="链接")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="分类")

    class Meta:
        # ordering = ['-sort']
        verbose_name = 'PC端楼层分类广告'
        verbose_name_plural = verbose_name
        db_table = 'd_category_ad'

    def __str__(self):
        return self.desc