# Generated by Django 5.0 on 2024-10-06 19:35

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pujo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid5,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("review", models.TextField()),
                ("created_at", models.DateField(auto_now_add=True)),
                ("is_edited", models.BooleanField(default=False)),
                ("edited_at", models.DateField(null=True)),
                (
                    "pujo",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="pujo.pujo",
                    ),
                ),
            ],
        ),
    ]
