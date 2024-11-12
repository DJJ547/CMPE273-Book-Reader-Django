from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    google_id = models.CharField(max_length=50, blank=True, null=True)  # Store Google ID
    profile_picture = models.URLField(null=True, blank=True)  # Store Google profile picture
