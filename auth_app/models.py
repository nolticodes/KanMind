"""Custom user model for the authentication app."""

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """Extend Django's default user model with full name and email fields."""

    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=128)