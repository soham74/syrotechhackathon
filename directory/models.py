from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from accounts.models import User


class Skill(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('skills-detail', kwargs={'slug': self.slug})


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=200)
    description = models.TextField()
    hour_value = models.DecimalField(max_digits=5, decimal_places=1, default=1.0)
    availability = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['skill', 'is_active']),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.skill.name})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('offers-detail', kwargs={'pk': self.pk})


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    hours_needed = models.DecimalField(max_digits=5, decimal_places=1)
    when = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['skill', 'is_active']),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.skill.name})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('requests-detail', kwargs={'pk': self.pk})

# Create your models here.
