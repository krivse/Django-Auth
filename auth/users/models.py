from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model with id as primary key
    and email as a unique field for auth and registration."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    username_validator = ''
    username = models.CharField(
        'username',
        unique=False,
        max_length=150
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
