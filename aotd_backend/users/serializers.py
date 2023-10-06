from djoser.serializers import UserCreateSerializer
from . import models

from djoser import serializers as djoser_serializers


class CustomUserSerializer(djoser_serializers.UserSerializer):
    class Meta(djoser_serializers.UserSerializer.Meta):
        fields = ['id', 'username']


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = ['username', 'password']
        model = models.CustomUser
