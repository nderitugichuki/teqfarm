from django.contrib import admin

from .models import PoultryHouse


@admin.register(PoultryHouse)
class PoultryHouseAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "current_occupancy", "is_active", "next_cleaning_at")
    list_filter = ("is_active",)
    search_fields = ("name",)

