# Generated by Django 4.2.6 on 2023-11-12 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0013_rename_user_artstyle_user_set_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artstyle',
            old_name='user_set',
            new_name='users',
        ),
    ]
