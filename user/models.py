from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
        ("superadmin", "Super Admin"),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    access_location = models.BooleanField(null=True)
    contact = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=100, null=True)
    birth_date = models.DateField(null=True)
    profile_picture = models.CharField(max_length=255, null=True)  
    bio = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="user")
    updated_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now=True)
    favorites = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    wishlists = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    saves = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    pandal_visits = ArrayField(models.CharField(max_length=255), default=list, blank=True)

    def clean(self):
        if User.objects.filter(username=self.username).exclude(pk=self.pk).exists():
            raise ValidationError({'username': _('A user with this username already exists.')})
        
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': _('A user with this email already exists.')})
        
        super(User, self).clean()

    def save(self, *args, **kwargs):
        # Perform clean before saving
        self.clean()
        super(User, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username'),
            models.UniqueConstraint(fields=['email'], name='unique_email'),
        ]

    def __str__(self):
        return str(self.id)



class BlacklistedToken(models.Model):
    token = models.CharField(max_length=512, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.token