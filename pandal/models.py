from django.db import models

class Pandal(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField(null = True)
    lon = models.FloatField(null = True)
    address = models.TextField()
    zone = models.CharField(max_length=100)
    uuid = models.UUIDField()
    # TODO Images of the particular pandal

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
