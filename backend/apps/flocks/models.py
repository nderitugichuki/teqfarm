from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from apps.common.models import AuditedModel


class Supplier(AuditedModel):
    name = models.CharField(max_length=150, unique=True)
    contact_person = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Breed(AuditedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class FlockBatch(AuditedModel):
    class BirdType(models.TextChoices):
        LAYERS = "layers", "Layers"
        BROILERS = "broilers", "Broilers"
        KIENYEJI = "kienyeji", "Kienyeji"
        BREEDERS = "breeders", "Breeders"

    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        QUARANTINED = "quarantined", "Quarantined"
        CLOSED = "closed", "Closed"

    batch_code = models.CharField(max_length=40, unique=True)
    batch_name = models.CharField(max_length=120)
    bird_type = models.CharField(max_length=20, choices=BirdType.choices, db_index=True)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name="batches")
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="batches", blank=True, null=True
    )
    arrival_date = models.DateField()
    initial_bird_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    current_bird_count = models.PositiveIntegerField(default=0)
    purchase_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    poultry_house = models.ForeignKey(
        "farms.PoultryHouse", on_delete=models.PROTECT, related_name="batches"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-arrival_date", "batch_code")
        constraints = [
            models.CheckConstraint(
                condition=Q(current_bird_count__lte=models.F("initial_bird_count")),
                name="flock_current_not_above_initial",
            )
        ]

    def __str__(self):
        return f"{self.batch_code} - {self.batch_name}"

    def clean(self):
        super().clean()
        if not self.poultry_house_id or self.status not in self.occupying_statuses:
            return
        occupied = FlockBatch.objects.filter(
            poultry_house_id=self.poultry_house_id, status__in=self.occupying_statuses
        ).exclude(pk=self.pk).aggregate(total=models.Sum("current_bird_count"))["total"] or 0
        count = self.current_bird_count or self.initial_bird_count
        if occupied + count > self.poultry_house.capacity:
            raise ValidationError({"poultry_house": "This batch would exceed house capacity."})

    @property
    def occupying_statuses(self):
        return (self.Status.ACTIVE, self.Status.QUARANTINED)


class BirdMovement(AuditedModel):
    class MovementType(models.TextChoices):
        ARRIVAL = "arrival", "Arrival"
        MORTALITY = "mortality", "Mortality"
        SALE = "sale", "Sale"
        ADJUSTMENT_IN = "adjustment_in", "Adjustment In"
        ADJUSTMENT_OUT = "adjustment_out", "Adjustment Out"

    batch = models.ForeignKey(FlockBatch, on_delete=models.PROTECT, related_name="bird_movements")
    movement_type = models.CharField(max_length=20, choices=MovementType.choices, db_index=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    movement_date = models.DateField(db_index=True)
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-movement_date", "-created_at")

    def __str__(self):
        return f"{self.batch.batch_code}: {self.movement_type} {self.quantity}"

