from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class BasicConfig(models.Model):
    key = models.CharField(max_length=255, null=False, primary_key=True)
    value = models.CharField(max_length=255, null=True)


class Artwork(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False, primary_key=True)
    data = models.JSONField(null=False)
    image_url = models.URLField(max_length=1_000, null=False)
    image_prompt = models.CharField(max_length=1_000)


@receiver(post_save, sender=Artwork)
def send_pushover(sender, instance, created: bool, **kwargs):
    # TODO: implement
    print('send Pushover message')
