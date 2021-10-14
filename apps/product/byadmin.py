from django.contrib import admin
from django.utils.safestring import mark_safe
from dadmin.admin import admin_site
# Register your models here.
from dadmin.byadmin import BaseOwnerAdmin
from .models import (
    ProductBrand, ProductCategory,ProductSKU, ProductSPUImage, 
    ProductSKUSpec, ProductSPU, ProductSPUSpec, ProductSpecOption
)
from .inlines_admin import (
    ProductSKUInline, ProductSPUSpecInline, 
    ProductSpecOptionInline, ProductSPUImageInline, 
    ProductSKUSpecInline, CategoryADInline) 



class ProductCategoryAdmin(BaseOwnerAdmin):
    list_display = ('id', 'name', 'parent', 'cate_icon',
                    'is_nav', 'is_show', 'sort', 'operate')
    list_editable = ('is_nav', 'sort',)
    readonly_fields = ('cate_icon',)
    inlines = [CategoryADInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 筛选fk字段的下拉菜单数据
        if db_field.name == "parent":
            # 这个条件限制了上级分类只能选择顶层分类，也就是说分类最多到2级
            kwargs["queryset"] = ProductCategory.objects.filter(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def cate_icon(self, obj):
        # 分类图标
        if obj.icon:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.icon.url, width=32, height=32))
        else:
            return mark_safe('暂未上传')

    cate_icon.short_description = "封面图"


admin_site.register(ProductCategory, ProductCategoryAdmin)


class ProductBrandAdmin(BaseOwnerAdmin):
    '''商品品牌'''

    list_display = ('id', 'category', 'name', 'brand_logo',
                    'sort', 'is_show', 'operate', )
    list_filter = ()
    list_editable = ('sort',)
    readonly_fields = ('brand_logo',)
    search_fields = ('name', 'category')
    search_placeholder = '输入分类或品牌名搜索'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 筛选fk字段的下拉菜单数据
        if db_field.name == "category":
            # 这个条件限制了上级分类只能选择顶层分类，品牌只能属于顶级分类
            # kwargs["queryset"] = ProductCategory.objects.filter(parent=None)
            kwargs["queryset"] = ProductCategory.objects.exclude(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def brand_logo(self, obj):
        # 分类图标
        if obj.image:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url, width='auto', height=32))
        else:
            return mark_safe('暂未上传')

    brand_logo.short_description = "品牌logo"

admin_site.register(ProductBrand, ProductBrandAdmin)


class ProductSPUAdmin(BaseOwnerAdmin):
    """商品SPU"""
    list_display = ('id', 'title', 'brand', 'category', 'category1', 'sales')
    search_fields = ('title', 'brand', 'category',)
    search_placeholder = '可通过商品标题、品牌、分类搜索'
    inlines = [
        ProductSKUInline,
        ProductSPUSpecInline,
        ProductSPUImageInline
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 筛选fk字段的下拉菜单数据
        if db_field.name == "category":
            # 一级下拉框为一级数据
            kwargs["queryset"] = ProductCategory.objects.filter(parent=None)
        elif db_field.name == "category1":
            # 二级下拉框为二级数据
            kwargs["queryset"] = ProductCategory.objects.exclude(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js',
            'dadmin/ckeditor5/ckeditor.js',
            'dadmin/ckeditor5/translations/zh.js',
            'dadmin/ckeditor5/config.js',
        )

admin_site.register(ProductSPU, ProductSPUAdmin)


class ProductSKUAdmin(BaseOwnerAdmin):
    list_display = ('spu', 'image', 'bar_code', 'shop_price', 'market_price', 'cost_price', 'product_unit', 'sales', 'stock', )
    # list_display_links = ('title', )
    readonly_fields = ('sku_image', )
    inlines = [
        ProductSKUSpecInline,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 筛选fk字段的下拉菜单数据
        if db_field.name == "category":
            # 这个条件限制了上级分类只能选择顶层分类，品牌只能属于顶级分类
            kwargs["queryset"] = ProductCategory.objects.exclude(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def sku_image(self, obj):
        # 分类图标
        if obj.image:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url, width='auto', height=64))
        else:
            return mark_safe('暂未上传')

    sku_image.short_description = "商品主图"

admin_site.register(ProductSKU, ProductSKUAdmin)


class ProductSPUSpecAdmin(BaseOwnerAdmin):
    '''Admin View for ProductSPUSpec'''

    list_display = ('id', 'name', 'operate')
    # list_filter = ('',)
    inlines = [
        ProductSpecOptionInline,
    ]
   
admin_site.register(ProductSPUSpec, ProductSPUSpecAdmin)


# class ProductSKUSpecAdmin(BaseOwnerAdmin):

#     list_display = ('sku', )

#     inlines = [
#         ProductSKUInline,
#         # ProductSPUSpecInline,
#         # ProductSpecOptionInline
#     ]

# admin_site.register(ProductSKUSpec, ProductSKUSpecAdmin)
