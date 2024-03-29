# Generated by Django 5.0.2 on 2024-03-08 05:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_userprofile_recent_pages_alter_parcel_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='secondary_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='moves_as_secondary', to=settings.AUTH_USER_MODEL, verbose_name='Add Users'),
        ),
    ]
