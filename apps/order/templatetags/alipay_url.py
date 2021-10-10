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
from utils.dalipay import Alipay
from order.models import DmallOrderInfo

# 官方文档：https://docs.djangoproject.com/zh-hans/3.2/howto/custom-template-tags/

# 这里的register不能随便修改
register = template.Library()


@register.simple_tag
def alipay_url(order_sn):   # 可以定义任意名称函
    try:
        order = DmallOrderInfo.objects.get(order_sn=order_sn)
        if order.pay_status == 1:
            alipay = Alipay()
            url = alipay.api_alipay_trade_page_pay(
                subject = order.order_sn,
                out_trade_no = order.order_sn,
                total_amount = order.total_amount.to_eng_string(),
                return_url = "http://127.0.0.1:8000/order/alipay/",
                notify_url="http://127.0.0.1:8000/order/alipay/" # 可选, 不填则使用默认notify url
            )
            re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
            return re_url
    except:
        return "该订单不存在"