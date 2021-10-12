'''
@File    :   __init__.py
@Time    :   2021/09/05 19:48:33
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   全局视图继承类
'''

from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from dadmin.models import Banner
from product.models import ProductCategory
from order.models import DmallShopingCart


class BaseView:
    """需要显示的地方继承该类
    """
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        navs = ProductCategory.get_navs()
        context['navs'] = navs
        # print(self.request.user.is_authenticated)
        if self.request.user.is_authenticated:
            context['cart_num'] = DmallShopingCart.get_cart_num(self.request.user)
            context['carts'] = DmallShopingCart.get_cart_owner(self.request.user)
            context['sum_money'], context['goods_num']  = DmallShopingCart.get_cart_sum_money(self.request.user)
            # DmallShopingCart.get_cart_sum_money(self.request.user)
            context['cart_json'] = DmallShopingCart.get_cart_json(self.request.user)
        return context


class IndexView(BaseView, ListView):
    template_name = 'index.html'
    queryset = Banner.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.get_banners_json()
        return context