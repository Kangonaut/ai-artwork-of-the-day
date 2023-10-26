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


class OpenWeatherSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OpenWeatherSettings
        fields = ['lat', 'lon']


class CalDavSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalDavSettings
        fields = ['caldav_url', 'calendar_url', 'username', 'password']


class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artwork
        fields = ['id', 'created_at', 'data', 'image_prompt']
