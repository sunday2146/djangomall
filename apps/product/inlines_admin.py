from product.models.product import ProductSKUSpec
from dadmin.byadmin import BaseOwnerStackInline, BaseOwnerTabularInline
from .models import ProductSKU, ProductSPUImage, ProductSPUSpec, ProductSpecOption, CategoryAD


class ProductSPUImageInline(BaseOwnerTabularInline):
    # 轮播图内联
    model = ProductSPUImage
    extra = 1
    fields = ('id', 'image', 'sort')


class ProductSKUInline(BaseOwnerStackInline):
    # sku内联
    model = ProductSKU
    extra = 1
    template = 'product/inlines_admin/stacked.html'
    verbose_name = "多规格商品"
    verbose_name_plural = verbose_name
    

class ProductSPUSpecInline(BaseOwnerTabularInline):
    # 轮播图内联
    model = ProductSPUSpec
    extra = 1
    

class ProductSKUSpecInline(BaseOwnerTabularInline):
    # 轮播图内联
    model = ProductSKUSpec
    extra = 1
    

class ProductSpecOptionInline(BaseOwnerTabularInline):
    # 规格选项
    model = ProductSpecOption
    extra = 1

class CategoryADInline(BaseOwnerTabularInline):
    # 分类关联广告位
    model = CategoryAD
    extra = 1