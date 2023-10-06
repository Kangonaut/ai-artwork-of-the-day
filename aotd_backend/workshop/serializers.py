from rest_framework import serializers
from . import models


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserSettings
        fields = ['issue_time']


class PushoverSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PushoverSettings
        fields = ['user_key']
