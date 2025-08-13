from django.contrib import admin
from .models import Transaction, BalanceSnapshot


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "hours", "match", "created_at")
    list_filter = ("from_user", "to_user")
    search_fields = ("from_user__username", "to_user__username")


@admin.register(BalanceSnapshot)
class BalanceSnapshotAdmin(admin.ModelAdmin):
    list_display = ("user", "hours", "updated_at")
    search_fields = ("user__username",)
