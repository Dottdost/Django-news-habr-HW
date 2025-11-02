from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'super admin'),
        ('ADMIN', 'admin'),
        ('USER', 'user'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
