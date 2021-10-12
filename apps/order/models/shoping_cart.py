import json
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import serializers

from dadmin.models import BaseModel
from product.models import ProductSKU, ProductSPU
from utils.tools import sum_list


class DmallShopingCart(BaseModel):
    """ 购物车 """
    spu = models.ForeignKey(ProductSPU, on_delete=models.CASCADE, verbose_name="商品SPU")
    sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE, blank=True, null=True, verbose_name="商品SKU")
    num = models.PositiveSmallIntegerField(default=1, verbose_name="购买数量", help_text="下单数量")

    class Meta:
        db_table = 'd_shoping_cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        # 同一个商品加入购物车只产生一个记录，
        # 多次加入进订单数增加，用户与关联商品唯一
        unique_together = ['owner', 'spu', 'sku']

    def __str__(self):
        return self.spu.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product:product-detail', kwargs={'pk': self.spu.pk})

    @classmethod
    def get_cart_owner(cls, user):
        # 查询当前用户的购物车商品
        return cls.objects.filter(owner=user, is_del=False)
    
    @classmethod
    def get_cart_num(cls, user):
        # 返回当前用户购物车的商品数量
        return cls.get_cart_owner(user=user).count()

    @classmethod
    def get_cart_sum_money(cls, user):
        """[查询当前用户商品总金额及总数]

        Args:
            user ([当前登录用户]): [request.user]

        Returns:
            [list]: [返回购物车商品总金额及购物车总商品数量的列表，上下文传入请使用解构赋值]
            sum_money：购物车总商品金额
            goods_num：购物车总商品数量
        """
        carts = cls.get_cart_owner(user=user)
        
        money_list = []  # 每个商品的总金额列表
        for product in carts:
            if product.spu.spec_type == 1:
                money = product.num * product.sku.shop_price
                money_list.append(money)
            else:
                money = product.num * product.spu.shop_price
                money_list.append(money)
        
        sum_money = sum_list(money_list)   # 商品总金额，列表求和
        # 商品总数
        goods_num_list = [cart.num for cart in carts]
        goods_num = sum_list(goods_num_list)
        return [sum_money, goods_num]

    @classmethod
    def get_cart_json(cls, user):
        # 序列化购物车数据
        carts = cls.get_cart_owner(user)
        cart_data = serializers.serialize('json', carts)
        cart_data = json.loads(cart_data)
        fields = [ data['fields'] for data in cart_data ]

        for cart in fields:
            # 序列化spu数据
            spus = ProductSPU.objects.filter(id=cart['spu'])
            spu_data = serializers.serialize('json', spus)
            spu_data = json.loads(spu_data)
            for data in spu_data:
                cart['spu'] = data['fields']
                
            
            # 如果存在多规格数据，则序列化sku
            if cart['sku']:
                skus = ProductSKU.objects.filter(id=cart['sku'])
                sku_data = serializers.serialize('json', skus)
                sku_data = json.loads(sku_data)
                for data in sku_data:
                    # 购物车多规格的总价 数量 * 单价
                    cart['total'] = str(cart['num'] * data['fields']['shop_price'])
                    cart['sku'] = data['fields']
                    
            else:
                # 购物车单规格的总价 数量 * 单价
                cart['total'] = str(cart['num'] * data['fields']['shop_price'])
        # 输出json数据
        return json.dumps(fields, ensure_ascii=False)