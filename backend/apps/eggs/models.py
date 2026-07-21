from django.db import models
from apps.common.models import AuditedModel

class EggInventory(AuditedModel):
    good_eggs = models.PositiveIntegerField(default=0)
    broken_eggs = models.PositiveIntegerField(default=0)
    dirty_eggs = models.PositiveIntegerField(default=0)
    trays_available = models.PositiveIntegerField(default=0)

class EggProduction(AuditedModel):
    daily_record = models.OneToOneField("daily_records.DailyFarmRecord", on_delete=models.PROTECT, related_name="egg_production")
    batch = models.ForeignKey("flocks.FlockBatch", on_delete=models.PROTECT, related_name="egg_production")
    production_date = models.DateField(db_index=True)
    good_eggs = models.PositiveIntegerField(default=0)
    broken_eggs = models.PositiveIntegerField(default=0)
    dirty_eggs = models.PositiveIntegerField(default=0)

    @property
    def production_percentage(self):
        birds = self.batch.current_bird_count
        return round((self.good_eggs / birds) * 100, 2) if birds else 0
