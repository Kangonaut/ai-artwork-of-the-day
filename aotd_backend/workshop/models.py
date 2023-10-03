from django.db import models
from users.models import CustomUser


class Artwork(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
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
    # pushover_user_token = models.CharField(
    #     max_length=30,
    #     null=True
    # )
    issue_time = models.TimeField(
        null=False
    )


class PushoverSettings(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    user_key = models.CharField(
        max_length=30,
        null=False,
    )
