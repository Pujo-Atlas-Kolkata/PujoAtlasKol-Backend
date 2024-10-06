from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField

class Metro(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    lat = models.FloatField(null = True)
    lon = models.FloatField(null = True)
    name = models.CharField(max_length=100)
    station_code = models.CharField(max_length=100)
    line = ArrayField(models.CharField(max_length=255), default=list)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(null = True)

    def save(self, *args, **kwargs):
        super(Metro, self).save(*args, **kwargs)

    def __str__(self):
        return self.name()
