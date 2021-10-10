from rest_framework import serializers
from dadmin.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """首页Banner

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Banner
        fields = "__all__"