'''
@File    :   adspace.py
@Time    :   2021/08/21 22:54:29
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   自定义广告位模板标签
'''
import json
from django import template
from django.utils.safestring import mark_safe
from dadmin.models import ADSpace

# 官方文档：https://docs.djangoproject.com/zh-hans/3.2/howto/custom-template-tags/

# 这里的register不能随便修改
register = template.Library()

@register.simple_tag
def ad_space(id):   # 可以定义任意名称函
  try:
    ad_space = ADSpace.objects.get(id=id)
    ads = ad_space.adcontent_set.filter(is_show=True)

    # 前端采用vue获取数据的话，请取消注释，返回json数据
    # data = []
    # for ad in ads:
    #   ads_dict = {}
    #   ads_dict['image'] = ad.image.url
    #   ads_dict['url'] = ad.url
    #   data.append(ads_dict)
    # return json.dumps(data, ensure_ascii=False) 
    
    return ads  # 如果使用的是django的模板语法请返回这个
  except ADSpace.DoesNotExist:
    return mark_safe('该广告位不存在，请传入正确的广告位id')