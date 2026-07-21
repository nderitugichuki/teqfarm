from django.contrib import admin

from .models import BirdMovement, Breed, FlockBatch, Supplier

admin.site.register(Supplier)
admin.site.register(Breed)


@admin.register(FlockBatch)
class FlockBatchAdmin(admin.ModelAdmin):
    list_display = ("batch_code", "batch_name", "bird_type", "current_bird_count", "poultry_house", "status")
    list_filter = ("bird_type", "status", "poultry_house")
    search_fields = ("batch_code", "batch_name")


@admin.register(BirdMovement)
class BirdMovementAdmin(admin.ModelAdmin):
    list_display = ("batch", "movement_type", "quantity", "movement_date", "created_by")
    list_filter = ("movement_type", "movement_date")

