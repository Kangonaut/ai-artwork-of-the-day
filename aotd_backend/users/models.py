from django.contrib.auth.models import AbstractUser
from django.db import models

from . import managers


class CustomUser(AbstractUser):
    email = None
    first_name = None
    last_name = None
    is_staff = None
    is_active = None
    date_joined = None
    is_superuser = None
    last_login = None

    objects = managers.CustomUserManager()

    class Meta:
        db_table = 'auth_user'
