from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class TeqFarmUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Farm profile", {"fields": ("role", "phone_number", "job_title", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Farm profile", {"fields": ("email", "role", "phone_number", "job_title")}),
    )

