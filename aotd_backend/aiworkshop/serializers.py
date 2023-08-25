from rest_framework.serializers import ModelSerializer
from . import models


class BasicConfigSerializer(ModelSerializer):
    class Meta:
        model = models.BasicConfig
        fields = ['key', 'value']
        read_only_fields = ['key']
