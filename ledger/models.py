from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User
from matches.models import Match


class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_received')
    hours = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0.1)])
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['to_user', 'created_at']),
            models.Index(fields=['from_user', 'created_at']),
        ]

    def __str__(self) -> str:
        return f"{self.from_user} -> {self.to_user}: {self.hours}h"


class BalanceSnapshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance_snapshots')
    hours = models.DecimalField(max_digits=7, decimal_places=1, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_balance_snapshot_user'),
        ]

    def __str__(self) -> str:
        return f"{self.user}: {self.hours}h"

# Create your models here.
