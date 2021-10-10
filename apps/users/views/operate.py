from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q, F
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View, ListView, CreateView, UpdateView
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from DjangoMall.views import BaseView
from dadmin.views import HasLoginRequired
from product.models.product import ProductSPU
from users.models.operate import DmallFavorite, DmallHotSearchWords
from users.models import DmallAddress
from users.forms import DmallFavoriteForm


# 文档：https://docs.djangoproject.com/zh-hans/3.2/topics/class-based-views/intro/#decorating-the-class


class DmallFavoriteView(View):
    """ 查看该商品是否已收藏接口 """
    def get(self, request, object_id, *args, **kwargs):
        text = "收藏"
        content_type = ContentType.objects.get_for_model(ProductSPU)  # 获取收藏对象的所属模型
        if request.user.is_authenticated:
            data = DmallFavorite.objects.filter(owner=request.user, content_type=content_type, object_id=object_id, is_del=False)  # 查询数据是否存在
            if data.exists():
                text = "已收藏"
            else:
                text = "收藏"
        return JsonResponse({'text': text})


class DmallFavoriteCreateView(HasLoginRequired, BaseView, CreateView):
    """商品收藏视图

    Args:
        HasLoginRequired ([type]): [description]
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = DmallFavorite
    form_class = DmallFavoriteForm
    template_name = 'users/fav.html'
    success_url = '/'

    def form_valid(self, form):
        object_id = self.request.POST.get('object_id')  #  获取要收藏的对象
        form.instance.owner = self.request.user  # 保存用户
        form.instance.content_type = ContentType.objects.get_for_model(ProductSPU)  # 获取收藏对象的所属模型
        data = DmallFavorite.objects.filter(owner=self.request.user, content_type=form.instance.content_type, object_id=object_id)  # 查询数据是否存在
        if data.exists():
            return JsonResponse({'status': 100, 'code': 'ok', 'message' :'该商品已收藏，请勿重复操作！'})
        form.save()
        return JsonResponse({'status': 200, 'code': 'ok', 'message' :'收藏成功！'})


class DmallFavoriteDeleteView(HasLoginRequired, BaseView, DeleteView):
    # 删除收藏
    # model = DmallFavorite
    fields = ('is_del',)
    template_name = "users/member/user_fav_delete.html"
    context_object_name = "fav"
    pk_url_kwarg = 'fav_id'

    def get_queryset(self):
        return DmallFavorite.objects.filter(owner=self.request.user)
    
    def get_success_url(self) -> str:
        return reverse('users:fav_list', kwargs={'pk': self.request.user.id})


class DmallSearchView(BaseView, ListView):
    """ 搜索视图"""
    template_name = 'users/search.html'
    context_object_name = 'spus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('keyword', '')       # 搜索词 
        context['hotwords'] = DmallHotSearchWords.objects.all()[:10]   # 热搜词
        return context

    def get_queryset(self):
        # 重写queryset
        queryset = ProductSPU.objects.filter(is_del=False, is_show=True, is_release=True)
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        else:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(sub_title__icontains=keyword) | Q(desc__icontains=keyword))
            for product in queryset:
                # 设置默认显示多规格信息
                if product.spec_type == 1:
                    sku = product.skus.filter(is_del=False, is_show=True).first()
                    product.shop_price = sku.shop_price
                    product.market_price = sku.market_price
                    product.cost_price = sku.cost_price
                    product.stock = sku.stock
            return queryset



# DmallAddressCreateView  添加收货地址
# DmallAddressUpdateView  修改收货地址
# DmallAddressDeleteView  删除收货地址
# DmallAddressHasDefault  是否设为默认

class DmallAddressCreateView(HasLoginRequired, CreateView):
    # 添加收货地址
    fields = ('province', 'city', 'district', 'address', 'signer_name', 'signer_mobile', 'email', 'is_default', )
    template_name = "users/member/address_form.html"

    def get_queryset(self):
        return DmallAddress.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # 默认地址只能有一个，所以需要把原来默认的给取消掉
        DmallAddress.objects.filter(owner=self.request.user, is_default=True).update(is_default=False)
        form.save()
        return JsonResponse({'status': 200, 'code': 'ok', 'message': '添加成功'})
    

class DmallAddressUpdateView(HasLoginRequired, BaseView, UpdateView):
    """用户中心修改收货地址视图

    Args:
        HasLoginRequired ([bool(object)]): [登录才能访问]
        BaseView ([View]): [继承全局数据视图]
        UpdateView ([UpdateView]): [django内置的编辑修改类视图]

    Returns:
        [type]: [修改用户信息后跳转到地址列表页]]
    """
    template_name = "users/member/address_form.html"
    fields = ('province', 'city', 'district', 'address', 'signer_name', 'signer_mobile', 'email', 'is_default', )
    pk_url_kwarg = "address_id"
    context_object_name = "address"

    def get_queryset(self):
        return DmallAddress.objects.filter(owner=self.request.user)
    
    def form_valid(self, form):
        # 保存的时候处理默认值
        DmallAddress.objects.filter(owner=self.request.user, is_default=True).update(is_default=False)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('users:address', kwargs={'pk': self.request.user.id})


class DmallAddressDeleteView(DmallAddressUpdateView):
    """伪删除用户的地址，只是修改is_del的状态

    Args:
        DmallAddressUpdateView ([type]): [继承修改地址的视图]

    Returns:
        [bool(object)]: [is_del=True]
    """
    fields = ('is_del',)
    template_name = "users/member/address_delete.html"

    def form_valid(self, form):
        # 保存的时候处理is_del的值
        form.instance.is_del = True
        return super().form_valid(form)


class DmallAddressHasDefault(DmallAddressUpdateView):
    # 收货地址设为默认
    fields = ('is_default',)
    template_name = "users/member/address_default.html"

    def form_valid(self, form):
        # 保存的时候处理is_del的值
        form.instance.is_default = True
        DmallAddress.objects.filter(owner=self.request.user, is_default=True).update(is_default=False)
        return super().form_valid(form)