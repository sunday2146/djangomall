from django.db import models
from django.utils.translation import gettext_lazy as _
from order.models import DmallOrderInfo
from dadmin.models import BaseModel
# from goods.models import GoodsSKU
from product.models import ProductSKU, ProductSPU
from comment.models import DmallComment
from users.models import DmallRate

 
class DmallOrderProduct(BaseModel):
    """订单商品"""

    order = models.ForeignKey(DmallOrderInfo,on_delete = models.CASCADE,verbose_name="订单")
    spu = models.ForeignKey(ProductSPU,on_delete = models.PROTECT,verbose_name="订单商品")
    sku = models.ForeignKey(ProductSKU,on_delete = models.PROTECT,blank=True, null=True,verbose_name="订单规格")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField('单价', max_digits=5, decimal_places=2)
    comment = models.ForeignKey(DmallComment,null=True,blank=True,on_delete = models.SET_NULL,verbose_name="评价信息")
    rate = models.ForeignKey(DmallRate,null=True,blank=True,on_delete = models.SET_NULL,verbose_name="满意度评分")
    is_commented = models.BooleanField(default=False,verbose_name="是否已评价")

    class Meta:
        db_table = "d_order_product"
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.spu.title