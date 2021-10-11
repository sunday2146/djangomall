from django.urls import path

from users.views.views import DmallRegisterCreateView
from .import views


app_name = "users"

urlpatterns = [
    path('login/', views.DmallLoginView.as_view(), name="login"),
    path('logout/', views.DmallLogoutView.as_view(), name="logout"),
    path('register/', views.DmallRegisterCreateView.as_view(), name="register"),
    path('add_fav/', views.DmallFavoriteCreateView.as_view(), name='add_fav'),
    path('get_fav/<int:object_id>/', views.DmallFavoriteView.as_view(), name='get_fav'),    # 查看该商品是否已收藏
    path('search/', views.DmallSearchView.as_view(), name='search'),
    path('create/address/', views.DmallAddressCreateView.as_view(), name='add_address'),
    path('member/<int:pk>/profile/', views.DmallUserInfoDetailView.as_view(), name='member'),
    path('member/<int:pk>/edit/', views.UserInfoUpdateView.as_view(), name='update_user'),
    path('member/<int:pk>/orders/', views.DmallOwnerOrderInfoListView.as_view(), name='orders'),
    path('member/<int:pk>/orderDetail/<int:order_id>/', views.DmallOwnerOrderInfoDetailView.as_view(), name='order_detail'),
    path('member/<int:pk>/address/', views.DmallAddressListView.as_view(), name='address'),
    path('member/<int:pk>/address/<int:address_id>/update/', views.DmallAddressUpdateView.as_view(), name='addr_update'),
    path('member/<int:pk>/address/<int:address_id>/delete/', views.DmallAddressDeleteView.as_view(), name='addr_delete'),
    path('member/<int:pk>/address/<int:address_id>/default/', views.DmallAddressHasDefault.as_view(), name='addr_default'),
    path('member/<int:pk>/fav/', views.DmallFavoriteListView.as_view(), name='fav_list'),
    path('member/<int:pk>/fav/<int:fav_id>/delete/', views.DmallFavoriteDeleteView.as_view(), name='fav_delete'),

]