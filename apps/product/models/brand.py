from django.db import models
from dadmin.models import BaseModel
from product.models.category import ProductCategory


class ProductBrand(BaseModel):
    """ 商品所属品牌 """
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 related_name="brands", verbose_name="所属分类", help_text="所属分类")
    name = models.CharField(max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = models.TextField(blank=True, max_length=200,
                            default="",  verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(blank=True, null=True, max_length=200,
                              upload_to="brands/", verbose_name="品牌logo", help_text="品牌logo")
    sort = models.PositiveSmallIntegerField(default=0, verbose_name="排序")

    class Meta:
        ordering = ["-sort"]
        verbose_name = "品牌"
        verbose_name_plural = verbose_name
        db_table = "d_product_brand"

    def __str__(self):
        return self.name
