from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from DjangoMall.views import BaseView
from dadmin.views import HasLoginRequired
from order.models import DmallOrderInfo
from users.models import DmallAddress, DmallFavorite
# Create your models here.
User = get_user_model()


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class DmallUserInfoDetailView(BaseView, DetailView):
    """个人中心

    Args:
        HasLoginRequired ([type]): 登录方可访问
        BaseView ([type]): 全站继承数据
        DetailView ([type]): 当前用户中心
    """
    model = User
    template_name = "users/member/user_info.html"
    context_object_name = "userinfo"


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class DmallOwnerOrderInfoListView(BaseView, ListView):
    # 个人中心订单
    template_name = "users/member/user_order_list.html"
    context_object_name = "order_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["not_pay_orders"] = self.get_order_type(pay_status=1)
        context["not_shipped_orders"] = self.get_order_type(pay_status=2)
        context["not_accept_orders"] = self.get_order_type(pay_status=3)
        context["not_comment_orders"] = self.get_order_type(pay_status=4)
        context["over_orders"] = self.get_order_type(pay_status=5)
        context["cancel_orders"] = self.get_order_type(pay_status=6)
        return context

    def get_queryset(self):
        # 当前用户的所有订单
        queryset =  DmallOrderInfo.objects.filter(owner=self.request.user).order_by('-add_date')
        return queryset
   
    def get_order_type(self, pay_status):
        # 订单的不同状态
        return self.get_queryset().filter(pay_status=pay_status)


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class DmallOwnerOrderInfoDetailView(BaseView, DetailView):
    # 订单详情
    # model = DmallOrderInfo
    template_name = "users/member/user_order_detail.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"

    def get_queryset(self):
        # 当前用户只能查看自己的订单
        return DmallOrderInfo.objects.filter(owner=self.request.user)


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class DmallAddressListView(BaseView, ListView):
    # 查询当前用户的收货地址
    template_name = "users/member/user_address_list.html"
    context_object_name = "address_list"

    def get_queryset(self):
        return DmallAddress.objects.filter(owner=self.request.user, is_del=False)


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class DmallFavoriteListView(BaseView, ListView):
    # 查询当前用户收藏的产品
    template_name = "users/member/user_fav_list.html"
    context_object_name = "fav_list"

    def get_queryset(self):
        return DmallFavorite.objects.filter(owner=self.request.user, is_del=False)

