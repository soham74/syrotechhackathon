from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("match", "rater", "ratee", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("rater__username", "ratee__username")
