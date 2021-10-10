from rest_framework import mixins
from rest_framework import viewsets
from product.models import ProductSKU, ProductSPU
from api.frontapi.product.serializers import ProductSKUSerializer
from api.frontapi.product.serializers import ProductSPUSerializer


class ProductSKUViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ProductSKU.objects.all()
    serializer_class = ProductSKUSerializer
    # permission_classes = []


class ProductSPUViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ProductSPU.objects.filter(is_del=False, is_show=True)
    serializer_class = ProductSPUSerializer
    # permission_classes = []
