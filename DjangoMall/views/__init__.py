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
from product.models import ProductCategory, ProductSPU, product
from order.models import DmallShopingCart


class BaseView:
    """需要显示的地方继承该类
    """
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['navs'] = ProductCategory.get_navs()
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
        context['bests'] = ProductSPU.get_best()
        context['floor_datas'] = self.get_floor_data()
        return context

    def get_floor_data(self):
        navs = ProductCategory.get_navs()
        for nav in navs:
            if nav.parent == None:
                nav.spu = nav.cat_spu.filter(is_new=True, is_del=False)
            else:
                nav.spu = nav.cat1_spu.filter(is_new=True, is_del=False)
            # print(nav.spu)  商品数据
        return navs
