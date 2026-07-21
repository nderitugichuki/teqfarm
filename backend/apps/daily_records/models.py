from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from apps.common.models import AuditedModel


class DailyFarmRecord(AuditedModel):
    batch = models.ForeignKey(
        "flocks.FlockBatch", on_delete=models.PROTECT, related_name="daily_records"
    )
    record_date = models.DateField(db_index=True)
    eggs_collected = models.PositiveIntegerField(default=0)
    broken_eggs = models.PositiveIntegerField(default=0)
    dirty_eggs = models.PositiveIntegerField(default=0)
    feed_issued_kg = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    feed_item = models.ForeignKey(
        "inventory.InventoryItem", on_delete=models.PROTECT, related_name="daily_feed_records",
        blank=True, null=True,
    )
    feed_transaction = models.OneToOneField(
        "inventory.StockTransaction", on_delete=models.PROTECT,
        related_name="daily_feed_record", blank=True, null=True,
    )
    water_notes = models.TextField(blank=True)
    sick_birds = models.PositiveIntegerField(default=0)
    dead_birds = models.PositiveIntegerField(default=0)
    observations = models.TextField(blank=True)
    mortality_movement = models.OneToOneField(
        "flocks.BirdMovement",
        on_delete=models.PROTECT,
        related_name="daily_record",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("-record_date", "batch__batch_code")
        constraints = [
            models.UniqueConstraint(
                fields=("batch", "record_date"), name="unique_daily_record_per_batch"
            ),
            models.CheckConstraint(
                condition=Q(broken_eggs__lte=models.F("eggs_collected")),
                name="daily_broken_not_above_collected",
            ),
            models.CheckConstraint(
                condition=Q(dirty_eggs__lte=models.F("eggs_collected")),
                name="daily_dirty_not_above_collected",
            ),
        ]

    def __str__(self):
        return f"{self.batch.batch_code} - {self.record_date}"

    @property
    def good_eggs(self):
        return max(0, self.eggs_collected - self.broken_eggs - self.dirty_eggs)
