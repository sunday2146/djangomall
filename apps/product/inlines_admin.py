from product.models.product import ProductSKUSpec
from dadmin.byadmin import BaseOwnerStackInline, BaseOwnerTabularInline
from .models import ProductSKU, ProductSPUImage, ProductSPUSpec, ProductSpecOption


class ProductSPUImageInline(BaseOwnerTabularInline):
    # 轮播图内联
    model = ProductSPUImage
    extra = 1
    fields = ('id', 'image', 'sort')


class ProductSKUInline(BaseOwnerStackInline):
    # sku内联
    model = ProductSKU
    extra = 1
    # fields = ('id', 'image', 'sort')
    template = 'product/inlines_admin/stacked.html'
    verbose_name = "多规格商品"
    verbose_name_plural = verbose_name
    # fk_name = "spu"
    # fk_name = 'specs'

class ProductSPUSpecInline(BaseOwnerTabularInline):
    # 轮播图内联
    model = ProductSPUSpec
    extra = 1
    # fields = ('id', 'image', 'sort')

class ProductSKUSpecInline(BaseOwnerTabularInline):
    # 轮播图内联
    model = ProductSKUSpec
    extra = 1
    # fields = ('id', 'image', 'sort')

class ProductSpecOptionInline(BaseOwnerTabularInline):
    # 规格选项
    model = ProductSpecOption
    extra = 1
    # fields = ('id', 'image', 'sort')