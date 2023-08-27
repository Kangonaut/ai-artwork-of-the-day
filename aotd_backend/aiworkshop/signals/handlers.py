from django.db.models.signals import post_save
from django.dispatch import receiver

from aiworkshop import models
from aiworkshop import delivery_services


@receiver(post_save, sender=models.Artwork)
def notify_delivery_services(sender, instance: models.Artwork, created: bool, **kwargs):
    delivery_services.Pushover.send_artwork(instance)
