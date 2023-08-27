from django.db import models


class BasicConfig(models.Model):
    key = models.CharField(max_length=255, null=False, primary_key=True)
    value = models.CharField(max_length=255, null=True)


class Artwork(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False, primary_key=True)
    data = models.JSONField(null=False)
    image = models.FileField(upload_to="uploads/%Y/%m/%d/", null=False)
    image_prompt = models.CharField(max_length=1_000)
