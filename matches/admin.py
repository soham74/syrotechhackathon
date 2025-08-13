from django.contrib import admin
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "requester", "provider", "agreed_hours", "scheduled_at", "created_at")
    list_filter = ("status",)
    search_fields = ("requester__username", "provider__username")
