from dadmin import models
from rest_framework import fields, serializers
from api.utils import BaseOwnerSerializer, BaseOwnerModelSerializer
from product.models import (
    ProductSPU, ProductCategory, ProductSKU, ProductBrand, 
    ProductSPUImage, ProductSKUSpec, ProductSpecOption, ProductSPUSpec
)


class ProductSpecOptionSerializer(BaseOwnerModelSerializer):
    """[ProductSpecOption]
    """
    class Meta:
        model = ProductSpecOption
        # fields = "__all__"
        fields = ('id','value')


class ProductSPUSpecSerializer(BaseOwnerModelSerializer):
    """[ProductSPUSpec]
    """
    options = ProductSpecOptionSerializer(many=True)

    class Meta:
        model = ProductSPUSpec
        # fields = "__all__"
        fields = ('id', 'name', 'options')


class ProductSKUSpecSerializer(BaseOwnerModelSerializer):
    """[ProductSKUSpec]
    """
    spec = serializers.StringRelatedField()
    option = serializers.StringRelatedField()

    class Meta:
        model = ProductSKUSpec
        # fields = "__all__"
        fields = ('id', 'spec', 'option')


class ProductSPUImageSerializer(BaseOwnerModelSerializer):
    """[ProductSKUImage]
    """
    class Meta:
        model = ProductSPUImage
        # fields = "__all__"
        fields = ('image',)


class ProductSKUSerializer(BaseOwnerModelSerializer):
    """[ProductSKU]
    详情视图序列化
    """
    specs = ProductSKUSpecSerializer(many=True)

    class Meta:
        model = ProductSKU
        fields = "__all__"


class ProductSPUSerializer(BaseOwnerModelSerializer):
    """[ProductSPU]
    """
    spu_spec = ProductSPUSpecSerializer(many=True)
    skus = ProductSKUSerializer(many=True)
    images = ProductSPUImageSerializer(many=True)

    class Meta:
        model = ProductSPU
        fields = "__all__"