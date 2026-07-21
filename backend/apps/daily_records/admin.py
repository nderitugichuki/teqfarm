from django.contrib import admin

from .models import DailyFarmRecord


@admin.register(DailyFarmRecord)
class DailyFarmRecordAdmin(admin.ModelAdmin):
    list_display = ("record_date", "batch", "eggs_collected", "feed_issued_kg", "sick_birds", "dead_birds")
    list_filter = ("record_date", "batch__poultry_house")
    search_fields = ("batch__batch_code", "observations")

