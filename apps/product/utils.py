def get_breadcrumb(category):    
    """返回面包屑导航数据"""    
    # 定义一个变量用来包装面包屑导航数据

    breadcrumb = {}
    breadcrumb['cat2'] = category
    breadcrumb['cat1'] = category.parent
    breadcrumb['home'] = '首页'
    # breadcrumb['cat3'] = category_model    
    # breadcrumb['cat2'] = category_model.parent
    # cat1 = category_model.parent.parent  
    # # 查询到一级    
    # goods_channel_model_qs = cat1.goodschannel_set.all()  
    # # 查询到一级所对应的商品频道查询集    
    # goods_channel_model = goods_channel_model_qs[0]  
    # # 获取商品频道查询集中0角标的频道模型对象    
    # cat1.url = goods_channel_model.url  
    # # 给一级类别模型对象多添加一个url    
    # breadcrumb['cat1'] = cat1    
    return breadcrumb