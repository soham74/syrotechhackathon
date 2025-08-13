from django.contrib import admin
from .models import Skill, Offer, Request


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "skill", "hour_value", "is_active", "created_at")
    list_filter = ("is_active", "skill")
    search_fields = ("title", "description", "user__username", "skill__name")


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "skill", "hours_needed", "is_active", "created_at")
    list_filter = ("is_active", "skill")
    search_fields = ("title", "description", "user__username", "skill__name")
