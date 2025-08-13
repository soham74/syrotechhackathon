from django.db import models
from accounts.models import User
from directory.models import Offer, Request


class Match(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_matches')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_matches')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    agreed_hours = models.DecimalField(max_digits=5, decimal_places=1, default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Match #{self.pk} {self.status}"

    def can_mark_done(self) -> bool:
        return self.status == self.STATUS_ACCEPTED and self.agreed_hours > 0

# Create your models here.
