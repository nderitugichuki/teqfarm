from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from apps.eggs.models import EggInventory
from apps.flocks.models import BirdMovement
from apps.flocks.services import record_bird_movement
from .models import Sale


@transaction.atomic
def create_sale(*, created_by, **data):
    quantity = data["quantity"]
    if quantity <= 0 or data["unit_price"] < 0:
        raise ValidationError({"quantity": "Quantity must be positive and price cannot be negative."})
    data["total_amount"] = (quantity * data["unit_price"]).quantize(Decimal("0.01"))
    if data.get("amount_paid", 0) > data["total_amount"]:
        raise ValidationError({"amount_paid": "Amount paid cannot exceed the total."})
    paid = data.get("amount_paid", Decimal("0"))
    expected_status = (
        Sale.PaymentStatus.PAID if paid == data["total_amount"]
        else Sale.PaymentStatus.PARTIAL if paid > 0 else Sale.PaymentStatus.UNPAID
    )
    data["payment_status"] = expected_status

    movement = None
    if data["sale_type"] == Sale.SaleType.EGGS:
        if quantity != quantity.to_integral_value():
            raise ValidationError({"quantity": "Egg quantity must be a whole number."})
        balance = EggInventory.objects.select_for_update().filter(pk=1).first()
        if not balance or balance.good_eggs < int(quantity):
            raise ValidationError({"quantity": "Insufficient good eggs in stock."})
        balance.good_eggs -= int(quantity)
        balance.save(update_fields=("good_eggs", "updated_at"))
    elif data["sale_type"] == Sale.SaleType.LIVE_BIRDS:
        if not data.get("batch"):
            raise ValidationError({"batch": "A flock batch is required for live bird sales."})
        if quantity != quantity.to_integral_value():
            raise ValidationError({"quantity": "Bird quantity must be a whole number."})
        movement = record_bird_movement(
            batch=data["batch"], movement_type=BirdMovement.MovementType.SALE,
            quantity=int(quantity), movement_date=data["sale_date"], created_by=created_by,
            reference="Live bird sale",
        )
    elif data.get("batch"):
        raise ValidationError({"batch": "Batch is only used for live bird sales."})

    return Sale.objects.create(**data, bird_movement=movement, created_by=created_by)


@transaction.atomic
def update_sale_payment(*, sale, amount_paid, payment_method):
    locked = Sale.objects.select_for_update().get(pk=sale.pk)
    if amount_paid < 0 or amount_paid > locked.total_amount:
        raise ValidationError({"amount_paid": "Payment must be between zero and the sale total."})
    locked.amount_paid = amount_paid
    locked.payment_method = payment_method
    locked.payment_status = (
        Sale.PaymentStatus.PAID if amount_paid == locked.total_amount
        else Sale.PaymentStatus.PARTIAL if amount_paid > 0 else Sale.PaymentStatus.UNPAID
    )
    locked.save(update_fields=("amount_paid", "payment_method", "payment_status", "updated_at"))
    return locked
