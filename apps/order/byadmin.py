from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
# Register your models here.
from dadmin.admin import admin_site
from dadmin.byadmin import BaseOwnerAdmin
from order.models import DmallShopingCart, DmallOrderInfo, DmallOrderProduct


class DmallShopingCartAdmin(BaseOwnerAdmin):
    '''Admin View for '''

    list_display = ('id', 'spu', 'sku', 'num', 'is_del', 'is_show')


admin_site.register(DmallShopingCart, DmallShopingCartAdmin)


class DmallOrderInfoAdmin(BaseOwnerAdmin):
    '''订单信息'''
    list_display = ('order_sn', 'order_product', 'order_sku', 'order_count', 'pay_status', 'pay_method', 
        'dtotal_amount',  'freight', 'address',  'order_mark', )
    readonly_fields = ('order_product', 'order_count')
    list_filter = ('pay_status', 'pay_method')
    list_editable = ('pay_status',)

    def dtotal_amount(self, obj):
        return obj.total_amount

    dtotal_amount.short_description = '实际支付'

    def get_product(self, obj):
        product_queryset = obj.dmallorderproduct_set.all()
        for product in product_queryset:
            return product

    def order_product_title(self, obj):
        # 返回商品标题
        return self.get_product(obj).title

    def order_count(self, obj):
        # 返回订单数量
        return self.get_product(obj).count
    
    order_count.short_description = '订单数量'


    def order_sku(self, obj):
        # 返回规格数据
        product = self.get_product(obj)
        skus = []
        if product.spu.spec_type == 1 and product.sku != None:
            for sku in product.sku.specs.values_list('spec__name', 'option__value'):
                skus.append(':'.join(sku))
            return mark_safe(':'.join(skus))
                    
    order_sku.short_description = '订单规格'


    def order_product(self, obj):
        product_queryset = obj.dmallorderproduct_set.all()
        product_list = []
        
        for product in product_queryset:
            product_list.append('''
                <div style="float:left; width:50px; height: 50px; margin-right:5px">
                    <img src="{}" width="50" height="50" />
                </div> 
                '''.format(product.spu.image.url))
            product_list.append(f'<div style="font-weight: 500;">{product.spu.title}</div>')
            # product_list.append(f'<div style="color:red">数量：{str(product.count)}</div>')
            # if product.spu.spec_type == 1 and product.sku != None:
            #     for sku in product.sku.specs.values_list('spec__name', 'option__value'):
            #         product_list.append(':'.join(sku))
        return mark_safe(''.join(product_list))

    order_product.short_description = '订单商品'

admin_site.register(DmallOrderInfo, DmallOrderInfoAdmin)


class DmallOrderProductAdmin(BaseOwnerAdmin):
    '''订单信息'''
    list_display = ('order', 'spu', 'sku', 'count', 'price', 'comment', 'rate', 'is_commented', 
        'order_pay_status', 'order_pay_method' )
    readonly_fields = ('order_pay_status', 'order_pay_method')

    def order_pay_status(self, obj):
        # 支付状态
        return obj.order.get_pay_status_display()
    
    order_pay_status.short_description = '支付状态'

    def order_pay_method(self, obj):
        # 支付状态
        return obj.order.get_pay_method_display()
    
    order_pay_method.short_description = '支付方式'

admin_site.register(DmallOrderProduct, DmallOrderProductAdmin)
