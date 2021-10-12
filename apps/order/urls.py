from os import name
from django.urls import path

from order.views.order_info import DmallShopingCartPayAll
from .import views

app_name = "order"

urlpatterns = [ 
    path('cart_list/', views.DmallShopingCartListView.as_view(), name="cart_list"),
    path('cart_create/', views.DmallShopingCartCreateView.as_view(), name="cart_create"),
    path('cart_delete/<int:pk>/', views.DmallShopingCartDeleteView.as_view(), name="cart_delete"),
    path('buynow/', views.DmallBuyNowView.as_view(), name="buynow"),
    path('payall/', views.DmallShopingCartPayAll.as_view(), name="payall"),
    path('alipay/', views.AliPayView.as_view(), name="alipay")
]