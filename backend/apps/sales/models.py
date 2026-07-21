import uuid
from django.db import models
from django.utils import timezone
from apps.common.models import AuditedModel


def generate_invoice_number():
    return f"TF-{timezone.localdate():%Y%m%d}-{uuid.uuid4().hex[:8].upper()}"


class Customer(AuditedModel):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Sale(AuditedModel):
    class SaleType(models.TextChoices):
        EGGS = "eggs", "Eggs"
        LIVE_BIRDS = "live_birds", "Live Birds"
        MANURE = "manure", "Manure"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        MOBILE_MONEY = "mobile_money", "Mobile Money"
        BANK = "bank", "Bank Transfer"
        CREDIT = "credit", "Credit"

    class PaymentStatus(models.TextChoices):
        PAID = "paid", "Paid"
        PARTIAL = "partial", "Partially Paid"
        UNPAID = "unpaid", "Unpaid"

    invoice_number = models.CharField(max_length=40, unique=True, default=generate_invoice_number)
    sale_date = models.DateField(default=timezone.localdate, db_index=True)
    sale_type = models.CharField(max_length=20, choices=SaleType.choices, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="sales")
    batch = models.ForeignKey(
        "flocks.FlockBatch", on_delete=models.PROTECT, related_name="sales", blank=True, null=True
    )
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    unit = models.CharField(max_length=30)
    unit_price = models.DecimalField(max_digits=14, decimal_places=2)
    total_amount = models.DecimalField(max_digits=16, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, db_index=True)
    notes = models.TextField(blank=True)
    bird_movement = models.OneToOneField(
        "flocks.BirdMovement", on_delete=models.PROTECT, related_name="sale",
        blank=True, null=True,
    )

    class Meta:
        ordering = ("-sale_date", "-created_at")

    def __str__(self):
        return self.invoice_number

