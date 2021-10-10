from datetime import datetime
from django.core.exceptions import ValidationError
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View, CreateView
from django.urls import reverse_lazy, reverse
from order.models.order_info import DmallOrderInfo
# Create your views here.
from utils.dalipay import Alipay


class AliPayView(View):
    """[处理支付宝的回调]
    即支付宝支付成功之后的一些操作问题处理
    Args:
        View ([type]): [Django默认的基类视图]
    """

    def get(self, request, *args, **kwargs):
        """处理支付宝的return_url
        """
        data_dict = {}
        data_query_dict = request.GET
        for key, value in data_query_dict.items():
            data_dict[key] = value
        signature = data_dict.pop("sign")
        alipay = Alipay()
        success = alipay.verify(data_dict, signature)
        if success:
            order_sn = data_dict.get('out_trade_no')
            trade_no = data_dict.get('trade_no')
            self.change_order(order_sn, trade_no)  # 修改订单状态
        return HttpResponse('成功')

    def post(self, request, *args, **kwargs):
        """处理支付宝的notify_url
        """
        data_dict = {}
        data_query_dict = request.POST
        for key, value in data_query_dict.items():
            data_dict[key] = value
        signature = data_dict.pop("sign")
        alipay = Alipay()
        success = alipay.verify(data_dict, signature)
        if success:
            order_sn = data_dict.get('out_trade_no')
            trade_no = data_dict.get('trade_no')
            self.change_order(order_sn, trade_no)
        return HttpResponse("success")

    def change_order(self, order_sn, trade_no, pay_status=2):
        """修改订单状态

        Args:
            order_sn ([str]): [订单号]
            trade_no ([str]): [支付宝返回的交易号]
            pay_status ([int]): [订单状态，默认修改为待发货]

        Raises:
            ValidationError: [检查订单是否存在的错误信息]
        """
        try:
           order = DmallOrderInfo.objects.get(order_sn=order_sn)
        except DmallOrderInfo.DoesNotExist:
            raise ValidationError('该订单不存在！')
        order.trade_sn = trade_no
        order.pay_status = pay_status   # 更改状态为待发货
        order.pay_time = datetime.now()
        order.save()
        return 'success'
        