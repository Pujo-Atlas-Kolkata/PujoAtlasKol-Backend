from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField

class Transport(models.Model):
    TRANSPORT_TYPE_CHOICES = [
        ("bus", "Bus"),
        ("auto", "Auto"),
        ("metro", "Metro"),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    lat = models.FloatField(null = True)
    lon = models.FloatField(null = True)
    name = models.CharField(max_length=100)
    station_code = models.CharField(max_length=100)
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_TYPE_CHOICES)
    line = ArrayField(models.CharField(max_length=255), default=list)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(null = True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.station_code = self.station_code.upper()
        self.transport_type = self.transport_type.title()
        super(Transport, self).save(*args, **kwargs)

    def __str__(self):
        return self.formatted_name()
