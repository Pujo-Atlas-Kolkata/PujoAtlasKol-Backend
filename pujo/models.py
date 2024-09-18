from django.db import models
import uuid

class Pujo(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField(null = True)
    lon = models.FloatField(null = True)
    address = models.TextField()
    city = models.TextField()
    zone = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null = True)

    def __str__(self):
        return self.name
