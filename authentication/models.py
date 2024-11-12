from django.db import models
from django.contrib.auth.models import AbstractUser
    
class CustomUser(AbstractUser):
    google_id = models.CharField(max_length=50, blank=True, null=True)  # Store Google ID
#    profile_picture = models.URLField(null=True, blank=True)  # Store Google profile picture
#    bookshelf = models.JSONField(default=list, blank=True)
#    reading_history = models.JSONField(default=dict, blank=True) 