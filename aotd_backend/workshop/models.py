from django.db import models
from users.models import CustomUser
from datetime import time


class Artwork(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
    )
    title = models.CharField(
        max_length=255,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )
    data = models.JSONField(null=False)
    image = models.FileField(
        upload_to="uploads/%Y/%m/%d/",
        null=False
    )
    image_prompt = models.CharField(max_length=1_000)

    class Meta:
        unique_together = ['user', 'created_at']


class UserSettings(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    issue_time = models.TimeField(
        null=False,
        default=time(
            hour=6,  # 06:00
        )
    )


class PushoverSettings(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    user_key = models.CharField(
        max_length=30,
        null=False,
    )


class CalDavSettings(models.Model):
    user = models.OneToOneField(
        CustomUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    caldav_url = models.URLField(
        max_length=255,
        null=False,
    )
    calendar_url = models.URLField(
        max_length=255,
        null=False,
    )
    username = models.CharField(
        max_length=255,
        null=False,
    )
    password = models.CharField(
        max_length=255,
        null=False,
    )


class OpenWeatherSettings(models.Model):
    user = models.OneToOneField(
        CustomUser,
        primary_key=True,
        on_delete=models.CASCADE
    )
    latitude = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=False,
    )
    longitude = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
    )


class DayTimeSettings(models.Model):
    user = models.OneToOneField(
        CustomUser,
        primary_key=True,
        on_delete=models.CASCADE
    )
    timezone_hour_offset = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=False,
    )


class ArtStyle(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        unique=True,
    )
    user = models.ManyToManyField(
        CustomUser,
    )


class CeleryTaskRun(models.Model):
    task = models.CharField(
        max_length=255,
        null=False,
    )
    run_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )

    class Meta:
        unique_together = ['task', 'run_at']
