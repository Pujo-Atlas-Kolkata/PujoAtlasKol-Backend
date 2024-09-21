from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
        ("superadmin", "Super Admin"),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    access_location = models.BooleanField(null=True)
    contact = models.IntegerField(null=True)
    gender = models.CharField(max_length=100, null=True)
    birth_date = models.DateField(null=True)
    profile_picture = models.CharField(max_length=255, null=True)  
    bio = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    access_token = models.CharField(max_length=255, null=True) 
    refresh_token = models.CharField(max_length=255, null=True)  
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="user")
    updated_at = models.DateTimeField(null=True, default=None)

    def clean(self):
        # Check if a user with the same username exists and is not soft-deleted
        if User.objects.filter(username=self.username, is_deleted=False).exclude(pk=self.pk).exists():
            raise ValidationError({'username': _('A user with this username already exists.')})
        
        # Check if a user with the same email exists and is not soft-deleted
        if User.objects.filter(email=self.email, is_deleted=False).exclude(pk=self.pk).exists():
            raise ValidationError({'email': _('A user with this email already exists.')})
        
        super(User, self).clean()

    def save(self, *args, **kwargs):
        # Perform clean before saving
        self.clean()
        super(User, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                condition=Q(is_deleted=False),
                name='unique_if_not_deleted'
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
