from django.db import models


# Create your models here.

class BasicConfig(models.Model):
    key = models.CharField(max_length=255, null=False, primary_key=True)
    value = models.CharField(max_length=255, null=True)
