from product.models import product
from product.models.product import ProductSKU, ProductSKUSpec
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.
from DjangoMall.views import BaseView
from product.models import ProductCategory


class ProductCategoryListView(BaseView, ListView):
    """ 全部分类 """
    template_name = "product/category_list.html"
    context_object_name = 'categories'
    queryset = ProductCategory.objects.filter(is_del=False, is_show=True, parent=None)


class ProductCategoryDetailView(BaseView, DetailView):
    """ 分类详情页 """
    model = ProductCategory
    template_name = "product/category_detail.html"
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['category']
        context['sub_categories'] = category.sub_cate.filter(is_del=False, is_show=True)
        context['sku'], context['sort'] = self.get_sku()
        return context

    def get_cat_spu(self):
        # 获得顶级分类的SPU
        category = self.get_object()
        if category.parent == None:
            return category.cat_spu.filter(is_del=False)

    def get_sku(self):
        """ 
        返回SKU 的QuerySet数据 
        sort: 通过get传入字段进行排序
        """
        sort = self.request.GET.get('sort', '')

        category = self.get_object()

        if category.parent != None:
            sku = category.productsku_set.filter(is_del=False)
            if sort == "sales" or sort == "-sales": 
                sku = sku.order_by(sort)
            if sort == "shop_price" or sort == "-shop_price":
                sku = sku.order_by(sort)
        else:
            sku_id = []
            spu = self.get_cat_spu()
            for product in spu:
                sku_list = product.productsku_set.filter(is_del=False)
                for good in sku_list:
                    sku_id.append(good.id)
            
            # 将list转换为QuerySet,官方提示谨慎使用嵌套查询，查询性能可能不佳
            # 官方文档：https://docs.djangoproject.com/zh-hans/3.2/ref/models/querysets/#in
            sku = ProductSKU.objects.filter(id__in = sku_id)  # list转为queryset
            if sort == "sales" or sort == "-sales": 
                sku = sku.order_by(sort)
            if sort == "shop_price" or sort == "-shop_price":
                sku = sku.order_by(sort)
        return [sku, sort]


class ProductSKUDetailView(BaseView, DetailView):
    """ 商品详情页 """
    queryset = ProductSKU.objects.filter(is_del=False)
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spu'] = self.get_spu()
        context['spec_qs'] = self.get_sku_spec_option_build()
        context['sku_dict'] = self.get_spec_sku_dict()
        return context

    def get_spu(self):
        # 获取当前sku所属的SPU
        return self.get_object().spu
    
    def get_sku_list(self):
        # 获取当前sku所属spu的所有sku的queryset
        sku_queryset = self.get_spu().productsku_set.filter(is_del=False)
        return sku_queryset

    def get_spec_queryset(self):
        # 获取当前SPU的所有的规格
        spu = self.get_spu()
        spec_queryset = spu.productspuspec_set.order_by('id')
        return spec_queryset

    def get_current_option(self):
        # 获取当前规格选项的列表[2, 4]
        sku = self.get_object()
        sku_spec_queryset = ProductSKUSpec.objects.filter(sku=sku.id)
        current_option_list = [ sku_spec.option.id for sku_spec in sku_spec_queryset]
        return current_option_list

    def get_spec_sku_dict(self):
        # 规格选项数据格式构造 {(2, 4): 1, (1, 5): 2}
        # key: 规格选项元组id
        # value: sku的id
        spec_sku_dict = dict()
        for temp_sku in self.get_sku_list():
            temp_sku_queryset = temp_sku.productskuspec_set.order_by('option_id')
            # 拥有对应sku产品的所有规格选项列表
            temp_sku_option_ids = [temp_sku_option.option.id for temp_sku_option in temp_sku_queryset]
            spec_sku_dict[tuple(temp_sku_option_ids)] = temp_sku.id
        return spec_sku_dict
    
    def get_sku_spec_option_build(self):
        # 为当前sku绑定组合数据
        spu_spec_queryset = self.get_spec_queryset()  # 当前spu下的所有规格
        for index, spec in enumerate(spu_spec_queryset):
            spec_option_queryset = spec.options.all() # 当前规格下的所有值
            temp_option_ids = self.get_current_option()[:]  # 复制一个新的当前显示商品的规格选项列表[]
            # print(temp_option_ids)
            for option in spec_option_queryset:
                temp_option_ids[index] = option.id
                option.sku_id = self.get_spec_sku_dict().get(tuple(temp_option_ids))
                # print(option.sku_id)
            spec.spec_options = spec_option_queryset
        # print(spu_spec_queryset)
        for spec in spu_spec_queryset:
            for option in spec.spec_options:
                # print(option)
                # print(option.sku_id)
                if option.sku_id in self.get_spec_sku_dict().values():
                    print(self.get_spec_sku_dict().values())
            # print(spec.spec_options)
        return spu_spec_queryset