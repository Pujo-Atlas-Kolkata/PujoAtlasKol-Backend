from django.db import models
import uuid
from metro.models import Metro

class LastScoreModel(models.Model):
    pujo = models.ForeignKey('Pujo', related_name='last_scores', on_delete=models.CASCADE)
    value = models.IntegerField()
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Score: {self.value} at {self.last_updated_at}"

class Pujo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    lat = models.FloatField(null = True)
    lon = models.FloatField(null = True)
    address = models.TextField()
    city = models.TextField()
    zone = models.CharField(max_length=100)
    search_score=models.FloatField(default=100.0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(null = True)
    nearest_metro_distance = models.FloatField(null=True, blank=True)
    metro = models.ForeignKey(Metro, related_name='pujos', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name()
