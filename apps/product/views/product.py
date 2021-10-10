import json
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse
from order.models.shoping_cart import DmallShopingCart
from product.models.product import ProductSKU, ProductSKUSpec
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.db.models import Max,Min
# Create your views here.
from DjangoMall.views import BaseView
from product.models import ProductCategory, ProductSPU, ProductSpecOption

'''
@File    :   product.py
@Time    :   2021/09/16 10:46:40
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   商品详情页相关数据
'''

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
        context['sku'], context['sort'] = self.get_has_sku()
        return context
    
    def get_product(self):
        # 查询当前分类下的所有spu
        
        category = self.get_object()
        if category.parent == None:
            spu = category.cat_spu.filter(is_del=False)
        else:
            spu = category.cat1_spu.filter(is_del=False)
        return spu
    
    def get_has_sku(self):
        sort = self.request.GET.get('sort', '')
        # 判断是否为多规格，如果是多规格则默认显示第一个sku的相关值
        spu = self.get_product()
        if sort == "sales" or sort == "-sales": 
            spu = spu.order_by(sort)
        if sort == "shop_price" or sort == "-shop_price":
            spu = spu.order_by(sort)
        for product in spu:
            if product.spec_type == 1:
                sku = product.skus.filter(is_del=False, is_show=True).first()
                product.shop_price = sku.shop_price
                product.market_price = sku.market_price
                product.cost_price = sku.cost_price
                product.stock = sku.stock
                # product.image = sku.image
        return [spu, sort]
            


class ProductSPUDetailView(BaseView, DetailView):
    """ 商品详情页 """
    queryset = ProductSPU.objects.filter(is_del=False)
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_template_names(self):
        template_names = super().get_template_names()
        if self.get_object().spec_type == 1:
            template_names = ['product/product_sku_detail.html']
            return template_names
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skus'] = self.get_sku_list()
        # context['specs'] = self.get_spec_queryset()
        context['specs'] = [(index, spec) for index, spec in enumerate(self.get_spec_queryset())]
        # print( [(index, spec) for index, spec in enumerate(self.get_spec_queryset())])
        context['product_news'] = self.get_product_news()
    
        
        if self.get_object().spec_type == 1:
            context['sku'] = context['skus'].first()               # sku的第条数据，供默认显示
            context['price_range'] = self.get_price_range()        # sku的价位区间
            context['current_option'] = self.get_current_option()  # 默认显示的第一个sku的选项列表
            context['spec_json'],context['spec_sku_json'] = self.get_spec_sku_dict()    # 多规格的json数据，供前端匹配比对选择
        # print(context)
        return context
    
    def get_product_news(self):
        spu = ProductSPU.objects.filter(is_del=False, is_show=True, is_new=True)[:5]
        for product in spu:
            if product.spec_type == 1:
                sku = product.skus.filter(is_del=False, is_show=True).first()
                product.shop_price = sku.shop_price
                product.market_price = sku.market_price
                product.cost_price = sku.cost_price
                product.stock = sku.stock
                # product.image = sku.image
        return spu

    def get_sku_list(self):
        # 获取当前商品所有sku的queryset
        spu = self.get_object()
        sku_queryset = spu.skus.filter(is_del=False)
        return sku_queryset

    def get_spec_queryset(self):
        # 获取当前SPU的所有的规格
        spu = self.get_object()
        spec_queryset = spu.spu_spec.order_by('id')
        return spec_queryset
    
    def get_price_range(self):
        # sku的价格区间
        product = self.get_object()
        if product.spec_type == 1:
            price_range = self.get_sku_list().aggregate(Max('shop_price'), Min('shop_price'))
            return price_range
    
    def get_current_option(self):
        # 获取当前规格选项的列表[2, 4]
        if self.get_object().spec_type == 1:
            sku_spec_queryset = ProductSKUSpec.objects.filter(sku=self.get_sku_list().first().id)
        current_option_list = [ sku_spec.option.id for sku_spec in sku_spec_queryset ]
        return sorted(current_option_list)
    
    def get_spec_sku_dict(self):
        # 规格选项数据格式构造 {(2, 4): 1, (1, 5): 2}
        # key: 规格选项元组id
        # value: sku的id
        spec_sku_dict = dict()
        for temp_sku in self.get_sku_list():
            temp_sku_queryset = temp_sku.specs.order_by('-option_id')
            # 拥有对应sku产品的所有规格选项列表
            temp_sku_option_values = [temp_sku_option.option.value for temp_sku_option in temp_sku_queryset]
            # 数组转字符串
            options_str = ','.join(temp_sku_option_values)
            # 拼接规格的格式，供前端比对数据
            spec_sku_dict[options_str] = {
                'spu_id':temp_sku.spu.id, 
                'sku_id': temp_sku.id, 
                'sku_shop_price': '%.2f' % temp_sku.shop_price, 
                'sku_image': f'/media/{temp_sku.image}',
                'sku_bar_code': temp_sku.bar_code,
                'sku_market_price': '%.2f' % temp_sku.market_price,
                'sku_cost_price': '%.2f' % temp_sku.cost_price,
                'sku_product_unit': temp_sku.product_unit,
                'sku_sales': temp_sku.sales,
                'sku_stock': temp_sku.stock
            }
        # sku的列表数据
        spec_sku_dict = json.dumps(spec_sku_dict, ensure_ascii=False)

        # 获取规格json数据
        specs = self.get_spec_queryset()
        spec_json = []
        for index, spec in enumerate(specs):
            spec_dict = {}
            spec_dict['id'] = spec.id
            spec_dict['product_id'] = spec.spu.id
            spec_dict['spec_index'] = index
            spec_dict['spec_name'] = spec.name
            spec_dict['spec_options'] = [ option.value for option in spec.options.all()]
            spec_json.append(spec_dict)

        # 转换保存为json数据
        spec_json = json.dumps(spec_json, ensure_ascii=False)
        
        # 输出两个值
        return [spec_json, spec_sku_dict]


class ProductSPUDetailViewJson(View):
    # 商品详情页的JSON数据
    
    def get(self, request, pk, *args, **kwargs):

        context = {}  # 最终需要返回的上下文数据
        host = request.get_host()  # 获取当前网址

        # 1. 处理当前的spu数据，并包装到context
        product = ProductSPU.objects.filter(pk=pk)
        if product:
            # 获取当前spu
            temp_spu = product.first()

            # 序列化当前spu数据
            spu = serializers.serialize('json', product)
            spu = json.loads(spu)
            for stor in spu:
                context['storeInfo'] = stor.get('fields', None)
                # 这样拼接似乎前端有问题
                # context['storeInfo']['image'] = '{}/media/{}'.format(host, context['storeInfo']['image'])
                context['storeInfo']['image'] = '/media/{}'.format(context['storeInfo']['image'])

            
            # 2.遍历spu的关联图
            context['storeInfo']['slider_image'] = [image.image.url for image in temp_spu.images.all()]
            # 注意观察返回的数据是否需要拼接路径，如果不需要那么这里注释即可
            # for index, img in enumerate(context['storeInfo']['slider_image']):
            #     context['storeInfo']['slider_image'][index] = '{}{}'.format(host, img)
        
            # 3.规格数据
            specs = serializers.serialize('json', temp_spu.spu_spec.all())
            specs = json.loads(specs)
            productAttr = []
            for spec in specs:
                productAttr.append(spec.get('fields', None))
                # 获取当前spec下的所有option
                options = ProductSpecOption.objects.filter(spec=spec.get('pk'))
                spec.get('fields', None)['attr_values'] = [ option.value  for option in options] 

            context['productAttr'] = productAttr   # 将规格数据返回

            # 4. spu下的sku关联的数据
            spec_sku_dict = dict()
            sku_queryset = temp_spu.skus.filter(is_del=False)
            for temp_sku in sku_queryset:
                temp_sku_queryset = temp_sku.specs.order_by('-option_id')
                # 拥有对应sku产品的所有规格选项列表
                temp_sku_option_values = [temp_sku_option.option.value for temp_sku_option in temp_sku_queryset]
                # 数组转字符串
                options_str = ','.join(temp_sku_option_values)
                # 拼接规格的格式，供前端比对数据
                spec_sku_dict[options_str] = {
                    'spu_id':temp_sku.spu.id, 
                    'sku_id': temp_sku.id, 
                    'sku_shop_price': '%.2f' % temp_sku.shop_price, 
                    'sku_image': f'/media/{temp_sku.image}',
                    'sku_bar_code': temp_sku.bar_code,
                    'sku_market_price': '%.2f' % temp_sku.market_price,
                    'sku_cost_price': '%.2f' % temp_sku.cost_price,
                    'sku_product_unit': temp_sku.product_unit,
                    'sku_sales': temp_sku.sales,
                    'sku_stock': temp_sku.stock
                }
            context['productValue'] = spec_sku_dict   # 规格的字典数据，Js中的object对象，主要方便前端匹配
        else:
            return JsonResponse({'code': 10010, 'message': '该商品不存在！'})
        return JsonResponse(context)
