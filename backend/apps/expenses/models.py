from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from apps.common.models import AuditedModel


class Expense(AuditedModel):
    class Category(models.TextChoices):
        FEED = "feed", "Feed"
        MEDICINE = "medicine", "Medicine"
        LABOUR = "labour", "Labour"
        ELECTRICITY = "electricity", "Electricity"
        WATER = "water", "Water"
        REPAIRS = "repairs", "Repairs"
        FUEL = "fuel", "Fuel"
        MISCELLANEOUS = "miscellaneous", "Miscellaneous"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        MOBILE_MONEY = "mobile_money", "Mobile Money"
        BANK = "bank", "Bank Transfer"
        CREDIT = "credit", "Credit"

    expense_date = models.DateField(default=timezone.localdate, db_index=True)
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    description = models.CharField(max_length=255)
    payee = models.CharField(max_length=150, blank=True)
    amount = models.DecimalField(
        max_digits=16, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    reference = models.CharField(max_length=100, blank=True)
    receipt = models.FileField(
        upload_to="expense_receipts/%Y/%m/", blank=True, null=True,
        validators=[FileExtensionValidator(("pdf", "jpg", "jpeg", "png", "webp"))],
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-expense_date", "-created_at")

    def __str__(self):
        return f"{self.get_category_display()} - {self.amount}"

