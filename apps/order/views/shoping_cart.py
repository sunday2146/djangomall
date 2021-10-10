from django.http import JsonResponse
from django.core import serializers
from django.views.generic import View, CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from dadmin.views import HasLoginRequired

from order.models import DmallShopingCart


class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)


class DmallShopingCartListView(HasLoginRequired, ListView):
    # 购物车列表页
    model = DmallShopingCart
    context_object_name = 'cart_list'
    template_name = 'order/cart_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_json'] = self.get_json()
        return context

    def get_json(self):
        queryset = self.get_queryset()
        data = serializers.serialize('json', queryset, fields=('goods','num', 'sku'))
        return data


class DmallShopingCartCreateView(HasLoginRequired, JsonableResponseMixin, CreateView):
    # 创建一个购物车商品
    model = DmallShopingCart
    fields = ['spu', 'sku', 'num']
    template_name = 'order/cart_form.html'

    def form_valid(self, form):
        """
        @author 幸福关中
        当前用户重复加入购物车只产生一条记录，多次加购只修改加购数量
        注意：这里有个点需要注意，加入购物车数量不能大于商品库存，不然下订单的时候库存数量不够怎么办？
        cart_id 返回购物车id，供立即购买去查询获取该添加到购物车的商品，单独结算！
        """
        form.instance.owner = self.request.user
        cart = DmallShopingCart.objects.filter(owner=self.request.user, spu=form.cleaned_data['spu'], sku=form.cleaned_data['sku'], is_del=False, is_show=True).last()
        if cart:
            cart.num += form.cleaned_data['num']
            if cart.num > (cart.spu.stock or cart.sku.stock):
                return JsonResponse({'code': 10010, 'message': '加入购物车的数量不能大于库存哟！'})
            cart.save()
            return JsonResponse({'code': 2001, 'message': '添加到购物车成功', 'cart_id': cart.id})
        new_form = form.save()  # 如果在这里想对一些数据处理请设置save方法的commit=False
        return JsonResponse({'code': 2001, 'message': '添加到购物车成功!', 'cart_id': new_form.id})


class DmallShopingCartDeleteView(HasLoginRequired, DeleteView):
    # 删除购物车
    model = DmallShopingCart
    template_name = 'order/cart_delete.html'
    # success_url = reverse_lazy('order:cart_list')
    success_url = '/'