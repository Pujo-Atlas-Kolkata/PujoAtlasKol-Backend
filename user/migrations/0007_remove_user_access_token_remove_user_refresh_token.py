# Generated by Django 5.0 on 2024-09-22 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_rename_created_at_blacklistedtoken_blacklisted_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='refresh_token',
        ),
    ]