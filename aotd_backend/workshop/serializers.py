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
        fields = ['latitude', 'longitude']


class CalDavSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalDavSettings
        fields = ['caldav_url', 'calendar_url', 'username', 'password']


class DaytimeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DaytimeSettings
        fields = ['timezone_hour_offset']


class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artwork
        fields = ['id', 'title', 'created_at', 'data', 'image_prompt', 'is_public']


class ArtStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArtStyle
        fields = ["id", "name"]


class PublishArtworkSerializer(serializers.Serializer):
    publish = serializers.BooleanField()
