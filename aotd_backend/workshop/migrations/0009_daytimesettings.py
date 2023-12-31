# Generated by Django 4.2.6 on 2023-11-06 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_is_staff'),
        ('workshop', '0008_rename_lat_openweathersettings_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayTimeSettings',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('timezone_hour_offset', models.DecimalField(decimal_places=1, max_digits=3)),
            ],
        ),
    ]
