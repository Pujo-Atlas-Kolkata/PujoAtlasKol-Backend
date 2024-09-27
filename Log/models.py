from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Log(models.Model):
    LOG_LEVEL_CHOICES = (
        ('INFO', 'Info'),
        ('DEBUG', 'Debug'),
        ('ERROR', 'Error'),
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES)
    message = models.TextField()
    module = models.CharField(max_length=100)
    user_id = models.UUIDField(editable=False, default=None, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.level} {self.message}"
