from django.db.models.signals import post_save
from django.dispatch import receiver

from workshop import models
from workshop import delivery_services


@receiver(post_save, sender=models.Artwork)
def notify_delivery_services(sender, instance: models.Artwork, created: bool, **kwargs):
    delivery_services.Pushover.deliver(instance)
