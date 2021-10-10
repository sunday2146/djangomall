from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from .plugin import CaptchaAPIView, DmallTokenObtainPairView

router = DefaultRouter()

from .dadmin import BannerViewSet
router.register('banners', BannerViewSet, basename="banners")

from .product import ProductSKUViewSet
router.register('product-sku', ProductSKUViewSet, basename="product-sku")

from .product import ProductSPUViewSet
router.register('product-spu', ProductSPUViewSet, basename="product-spu")

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('captcha/', CaptchaAPIView.as_view(), name='captcha_api'),
    path('mytoken/', DmallTokenObtainPairView.as_view(), name='mytoken')
]

urlpatterns += router.urls