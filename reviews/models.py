from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from matches.models import Match


class Review(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='reviews')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    ratee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['match', 'rater'], name='unique_review_per_match_per_rater'),
        ]

    def __str__(self) -> str:
        return f"Review {self.rating} by {self.rater} for {self.ratee}"

# Create your models here.
