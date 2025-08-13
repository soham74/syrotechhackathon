from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    location = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    reputation_score = models.IntegerField(default=0)
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True)

    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})

# Create your models here.
