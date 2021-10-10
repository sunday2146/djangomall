from rest_framework import mixins
from rest_framework import viewsets
from dadmin.models import Banner
from .serializers import BannerSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        banners列表数据
    """
    queryset = Banner.objects.filter(is_del=False, is_show=True)
    serializer_class = BannerSerializer