from django.db.models import F
from django.core.exceptions import ValidationError
from django.http.response import HttpResponse, JsonResponse
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import View, CreateView, ListView, DeleteView
from DjangoMall.views import BaseView
from dadmin.views import HasLoginRequired
from order.models import DmallOrderInfo, DmallShopingCart, DmallOrderProduct
from order.forms import DmallOrderInfoForm
from product.models.product import ProductSKU, ProductSPU
from users.models import DmallAddress
from utils.dalipay import Alipay
from DjangoMall.conf import return_url, notify_url


class DmallBuyNowView(HasLoginRequired, BaseView, CreateView):
    """ 立即购买视图 """
    model = DmallOrderInfo
    form_class = DmallOrderInfoForm
    template_name = "order/buynow.html"
    # success_url = reverse_lazy('/')
    success_url = "/"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        order_sn = timezone.now().strftime('%Y%m%d%H%M%S') + '%09d' % self.request.user.id
        form.instance.order_sn = order_sn                       # 1. 生成订单号
        form.instance.total_amount = self.get_sum_price()       # 2. 保存商品总价
        form.instance.freight = self.get_add_freight()          # 3. 保存运费,后续逻辑再处理运费
        form.save()                                             # 4. 保存该订单
        self.change_product_stock()                             # 5. 目前已实现减库存, 超时取消订单库存回归，未实现
        order = DmallOrderInfo.objects.get(order_sn=order_sn)   # 6. 查询到该订单实例
        self.save_order_product(order)                          # 7. 保存订单关联商品,并删除该购物车商品
        if order.pay_method == 2:
            re_url = self.get_alipay_url(order=order)           # 9. 获取支付宝的支付跳转链接
            # 不一定返回继承，可以返回任何自己想返回的结果，前提是在此之前调用了form.save()
            # return super().form_valid(form)
            return redirect(re_url)                             # 10. 跳转到支付宝支付页面
        else:
            return HttpResponse('暂不支持该支付方式')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = self.get_address()           # 查询到该用户的所有地址
        context['cart_product'] = self.get_cart_product() # 返回该购物车
        context['total_price'] = self.get_total_price()   # 返回商品总价，即件数*单价的价格
        context['total'] = self.get_sum_price()           # 应付总金额，即商品总价+运费及优惠过后的价格，实际支付价
        context['freight'] = self.get_add_freight()       # 返回计算好的运费
        context['pay_method'] = DmallOrderInfo.get_pay_method()    # 支付方式数据字典
        context['pay_default'] = DmallOrderInfo.get_pay_default()  # 默认支付方式
        return context

    def get_cart_product(self):
        cart_id = self.request.GET['cart_id']
        try:
            cart_product = DmallShopingCart.objects.get(id=cart_id, owner=self.request.user)
            return cart_product
        except DmallShopingCart.DoesNotExist:
            # 这里返回的字典格式不能变，后边根据这个数据格式验证错误！
            return {'message': '您要购买的该商品不存在！'}

    def get_address(self):
        # 获取该用户添加的地址
        return DmallAddress.objects.filter(owner=self.request.user, is_del=False)   # 地址

    def get_total_price(self):
        # 计算该商品的总价
        cart = self.get_cart_product()
        if not isinstance(cart, dict):
            if cart.spu.spec_type == 1 and cart.sku:
                return cart.num * cart.sku.shop_price
            else:
                return cart.num * cart.spu.shop_price
        else:
            return cart
    
    def get_add_freight(self):
        # 运费计算,后续完善
        # freight = self.get_object().freight
        # print(self.get_cart_product().spu.freight)
        return 0

    def get_sum_price(self):
        # 计算该商品实际应付，加运费，以及一些优惠活动之后的价格
        total = self.get_total_price()
        if not isinstance(total, dict):
            return total + self.get_add_freight()

    def save_order_product(self, order):
        # 创建订单时关联保存订单商品信息
        # order => 要保存订单的实例
        cart = self.get_cart_product()
        spu = cart.spu
        if spu.spec_type == 1:
            sku = cart.sku
            price = cart.sku.shop_price
        else:
            sku = None
            price = spu.shop_price
        DmallOrderProduct.objects.create(owner=self.request.user, order=order, spu=spu, sku=sku, count=cart.num, price=price)
        cart.delete()
        return 'chenggong'

    def get_alipay_url(self, order):
        """获取支付宝的支付跳转链接

        Args:
            order ([obj]): [该订单的实例对象]

        Returns:
            [str]: [返回支付宝的支付跳转url]
        """
        alipay = Alipay()
        url = alipay.api_alipay_trade_page_pay(
            subject = order.order_sn,
            out_trade_no = order.order_sn,
            total_amount = order.total_amount.to_eng_string(),
            # return_url = "http://127.0.0.1:8000/order/alipay/",
            # notify_url= "http://127.0.0.1:8000/order/alipay/" # 可选, 不填则使用默认notify url
            return_url= return_url,
            notify_url = notify_url
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url
    
    def change_product_stock(self):
        # 修改商品库存，订单保存之后就减掉库存
        cart = self.get_cart_product()
        if not isinstance(cart, dict):
            # 多规格库存处理
            if cart.spu.spec_type == 1 and cart.sku:
                if cart.sku.stock < cart.num:
                    print('库存不足')
                    return JsonResponse({'message': f'{cart.sku}的库存不足'})
                cart.sku.stock = F('stock') - cart.num
                return cart.sku.save()
                
            # 单规格库存处理
            else:
                if cart.spu.stock < cart.num:
                    print('库存不足')
                    return JsonResponse({'message': f'{cart.spu}的库存不足'})
                cart.spu.stock = F('stock') - cart.num
                return cart.spu.save()
        return cart


class DmallShopingCartPayAll(HasLoginRequired, BaseView, CreateView):
    
    # 购物车批量结算
    model = DmallOrderInfo
    form_class = DmallOrderInfoForm
    template_name = "order/payall.html"
    # success_url = reverse_lazy('/')
    success_url = "/"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        order_sn = timezone.now().strftime('%Y%m%d%H%M%S') + '%09d' % self.request.user.id
        form.instance.order_sn = order_sn                       # 1. 生成订单号
        form.instance.total_amount = self.get_sum_price()       # 2. 保存商品总价
        form.instance.freight = self.get_add_freight()          # 3. 保存运费,后续逻辑再处理运费
        self.change_product_stock()
        form.save()                                             # 4. 保存该订单
        order = DmallOrderInfo.objects.get(order_sn=order_sn)   # 6. 查询到该订单实例
        self.save_order_product(order)                          # 7. 保存订单关联商品,并清空购物车
        
        if order.pay_method == 2:
            re_url = self.get_alipay_url(order=order)           # 9. 获取支付宝的支付跳转链接
            # 不一定返回继承，可以返回任何自己想返回的结果，前提是在此之前调用了form.save()
            # return super().form_valid(form)
            return redirect(re_url)                             # 10. 跳转到支付宝支付页面
        else:
            return HttpResponse('暂不支持该支付方式')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = self.get_address()   # 查询到该用户的所有地址
        context['pay_method'] = DmallOrderInfo.get_pay_method()    # 支付方式数据字典
        context['pay_default'] = DmallOrderInfo.get_pay_default()  # 默认支付方式
        context['freight'] = self.get_add_freight()                # 运费计算
        context['total'] = self.get_sum_price()                    # 商品总价
        return context

    def get_address(self):
        # 获取该用户添加的地址
        return DmallAddress.objects.filter(owner=self.request.user, is_del=False)   # 地址
    
    def get_add_freight(self):
        # 运费计算,后续完善
        return 0
    
    def get_sum_price(self):
        # 商品总价+运费
        return DmallShopingCart.get_cart_sum_money(self.request.user)[0] + self.get_add_freight()

    def get_carts(self):
        return DmallShopingCart.objects.filter(owner=self.request.user, is_del=False)
    
    def change_product_stock(self):
        # 修改商品库存，订单保存之后就减掉库存
        carts = self.get_carts()
        
        for cart in carts:
            if cart.spu.spec_type == 1 and cart.sku:
                if cart.sku.stock < cart.num:
                    print('库存不足')
                    return JsonResponse({'message': f'{cart.sku}的库存不足'})
                # print(cart.num)
                ProductSKU.objects.filter(id=cart.sku.id).update(stock=F('stock') - cart.num)

            else:
                if cart.spu.stock < cart.num:
                    print('库存不足')
                    return JsonResponse({'message': f'{cart.spu}的库存不足'})
                ProductSPU.objects.filter(id=cart.spu.id).update(stock=F('stock') - cart.num)
        return carts
    
    def save_order_product(self, order):
        # 创建订单时关联保存订单商品信息
        # order => 要保存订单的实例
        carts = self.get_carts()
        for cart in carts:
            order_product = DmallOrderProduct()
            order_product.owner = self.request.user
            order_product.order = order
            order_product.spu = cart.spu
            order_product.sku = cart.sku
            order_product.count = cart.num
            if cart.spu.spec_type == 1:
                price = cart.sku.shop_price
                order_product.price = price
            else:
                order_product.price = cart.spu.shop_price
            order_product.save()
            cart.delete()
        return carts
    

    def get_alipay_url(self, order):
        """获取支付宝的支付跳转链接

        Args:
            order ([obj]): [该订单的实例对象]

        Returns:
            [str]: [返回支付宝的支付跳转url]
        """
        alipay = Alipay()
        url = alipay.api_alipay_trade_page_pay(
            subject = order.order_sn,
            out_trade_no = order.order_sn,
            total_amount = order.total_amount.to_eng_string(),
            # return_url = "http://127.0.0.1:8000/order/alipay/",
            # notify_url= "http://127.0.0.1:8000/order/alipay/"   # 可选, 不填则使用默认notify url
            return_url= return_url,
            notify_url = notify_url
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url