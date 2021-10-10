from rest_framework import serializers


class BaseOwnerSerializer(serializers.Serializer):
    # Serializer
    owner = serializers.HiddenField(
        default = serializers.CurrentUserDefault())

    class Meat:
        exclude = ('is_del', 'is_show')
        

class BaseOwnerModelSerializer(serializers.ModelSerializer):
    # ModelSerializer
    owner = serializers.HiddenField(
        default = serializers.CurrentUserDefault())

    class Meat:
        exclude = ('is_del', 'is_show')