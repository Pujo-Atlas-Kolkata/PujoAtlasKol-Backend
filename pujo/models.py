from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField

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
    search_score=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(null = True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.address = self.address.lower()
        self.city = self.city.lower()
        self.zone = self.zone.lower()
        super(Pujo, self).save(*args, **kwargs)

    def formatted_name(self):
        return self.name.title()

    def formatted_address(self):
        return self.address.title()

    def formatted_city(self):
        return self.city.title()

    def formatted_zone(self):
        return self.zone.upper()

    def __str__(self):
        return self.formatted_name()
