from djoser.serializers import UserCreateSerializer
from . import models


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = ('username', 'password')
        model = models.CustomUser
