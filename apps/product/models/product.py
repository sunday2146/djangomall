from django.db import models
from dadmin.models import BaseModel
from product.models import ProductCategory, ProductBrand


class ProductSPU(BaseModel):
    """ 商品 """
    SPEC_TYPE = (
        (0, "单规格"),
        (1, "多规格")
    )

    title = models.CharField(max_length=60, verbose_name="标题")
    sub_title = models.CharField(max_length=60, blank=True, default="", verbose_name="副标题")
    desc = models.CharField(max_length=256, default="", blank=True, verbose_name="简介")
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='cat_spu', verbose_name="一级类目")
    category1 = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='cat1_spu', verbose_name="二级类目")
    brand = models.ForeignKey(ProductBrand, on_delete=models.PROTECT, related_name="brands", blank=True, null=True, verbose_name="品牌")
    spec_type = models.PositiveIntegerField(choices=SPEC_TYPE, default=0, verbose_name="规格类型")
    image = models.ImageField(upload_to="product/spu/",blank=True, null=True, max_length=200, verbose_name="商品主图")
    bar_code = models.CharField(default="", blank=True, max_length=15, verbose_name="商品条码")
    shop_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="售价")
    market_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="市场价")
    cost_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="成本价")
    sales = models.PositiveIntegerField(default=0, verbose_name="销量")
    stock = models.PositiveIntegerField(default=0, verbose_name="库存")
    product_unit = models.CharField(max_length=30, default="", blank=True, verbose_name="商品单位")
    content = models.TextField(verbose_name="商品详情", help_text="详情")
    is_new = models.BooleanField(default=False, verbose_name="新品")
    is_hot = models.BooleanField(default=False, verbose_name="热销")
    is_benefit = models.BooleanField(default=False, verbose_name="促销")
    is_best = models.BooleanField(default=False, verbose_name="精品")
    is_release = models.BooleanField(default=True, verbose_name='是否上架')

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name
        db_table = "d_product_spu"

    def __str__(self):
        return self.title


class ProductSKU(BaseModel):
    """商品SKU"""
    spu = models.ForeignKey(ProductSPU, related_name="skus", on_delete=models.CASCADE, verbose_name="商品")
    image = models.ImageField(max_length=200, upload_to="product/sku/", verbose_name="商品主图")
    bar_code = models.CharField(default="", blank=True, max_length=15, verbose_name="商品条码")
    shop_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="售价")
    market_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="市场价")
    cost_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="成本价")
    product_unit = models.CharField(max_length=30, default="", blank=True, verbose_name="商品单位")
    sales = models.PositiveIntegerField(default=0, verbose_name="销量")
    stock = models.PositiveIntegerField(default=0, verbose_name="库存", help_text="库存")
    
    class Meta:
        verbose_name = "SKU"
        verbose_name_plural = verbose_name
        db_table = "d_product_sku"

    def __str__(self):
        return f'{self.spu.title}的SKU'


class ProductSPUImage(BaseModel):
    spu = models.ForeignKey(ProductSPU, related_name='images', on_delete=models.CASCADE, verbose_name="SPU")
    image = models.ImageField(max_length=200, upload_to="product/spu/imgs/", verbose_name="商品图片")
    sort = models.PositiveSmallIntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = "SPU图片"
        verbose_name_plural = verbose_name
        db_table = "d_product_spu_img"

    def __str__(self):
        return f'{self.spu.title} {self.id}'


class ProductSPUSpec(BaseModel):
    """商品SPU规格"""
    spu = models.ForeignKey(
        ProductSPU, related_name="spu_spec", on_delete=models.CASCADE, verbose_name="SPU")
    name = models.CharField("规格名称", max_length=50)

    class Meta:
        verbose_name = "规格"
        verbose_name_plural = verbose_name
        db_table = "d_product_spu_spec"

    def __str__(self):
        return self.name


class ProductSpecOption(BaseModel):
    """规格选项"""
    spec = models.ForeignKey(
        ProductSPUSpec, on_delete=models.CASCADE, related_name='options', verbose_name="规格")
    value = models.CharField("选项值", max_length=50)

    class Meta:
        verbose_name = "规格选项"
        verbose_name_plural = verbose_name
        db_table = "d_product_spec_option"

    def __str__(self):
        return self.value


class ProductSKUSpec(BaseModel):
    """SKU具体规格"""
    sku = models.ForeignKey(
        ProductSKU, related_name="specs", on_delete=models.CASCADE, verbose_name="SKU")
    spec = models.ForeignKey(
        ProductSPUSpec, on_delete=models.PROTECT, verbose_name="规格名称")
    option = models.ForeignKey(
        ProductSpecOption, on_delete=models.PROTECT, verbose_name="规格值")

    class Meta:
        verbose_name = "SKU规格"
        verbose_name_plural = verbose_name
        db_table = "d_product_sku_spec"

    def __str__(self):
        return f'{self.sku} - {self.spec.name} - {self.option.value}'