from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import AuditedModel


class InventoryItem(AuditedModel):
    class Category(models.TextChoices):
        FEED = "feed", "Feed"
        MEDICINE = "medicine", "Medicine"
        VACCINE = "vaccine", "Vaccine"
        EGG_TRAY = "egg_tray", "Egg Tray"
        EQUIPMENT = "equipment", "Equipment"

    name = models.CharField(max_length=150, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    unit = models.CharField(max_length=30)
    current_stock = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    reorder_level = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("category", "name")

    def __str__(self):
        return f"{self.name} ({self.unit})"

    @property
    def is_low_stock(self):
        return self.current_stock <= self.reorder_level


class StockTransaction(AuditedModel):
    class TransactionType(models.TextChoices):
        STOCK_IN = "in", "Stock In"
        STOCK_OUT = "out", "Stock Out"
        ADJUSTMENT_IN = "adjustment_in", "Adjustment In"
        ADJUSTMENT_OUT = "adjustment_out", "Adjustment Out"

    item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices, db_index=True)
    quantity = models.DecimalField(
        max_digits=14, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    transaction_date = models.DateField(db_index=True)
    expiry_date = models.DateField(blank=True, null=True, db_index=True)
    unit_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-transaction_date", "-created_at")

    def __str__(self):
        return f"{self.item.name}: {self.transaction_type} {self.quantity}"

