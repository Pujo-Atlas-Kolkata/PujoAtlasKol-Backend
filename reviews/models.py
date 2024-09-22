from django.db import models
from pujo.models import Pujo
from user.models import User
import uuid

# Create your models here.
class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid5, editable=False, unique=True, primary_key=True)
    pujo = models.ForeignKey(Pujo, on_delete=models.CASCADE, related_name='reviews', editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', editable=False)
    review = models.TextField()
    created_at = models.DateField(auto_now_add=True, editable=False)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateField(null=True)

    def __str__(self) -> str:
        return self.id