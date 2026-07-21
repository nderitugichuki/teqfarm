from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import AuditedModel


class PoultryHouse(AuditedModel):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    cleaning_interval_days = models.PositiveSmallIntegerField(
        default=14, validators=[MinValueValidator(1)]
    )
    last_cleaned_at = models.DateField(blank=True, null=True)
    next_cleaning_at = models.DateField(blank=True, null=True, db_index=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    @property
    def current_occupancy(self):
        return sum(
            batch.current_bird_count
            for batch in self.batches.filter(status__in=("active", "quarantined"))
        )

