from django.core.exceptions import ValidationError
from django.db import transaction

from .models import InventoryItem, StockTransaction

INCOMING = {
    StockTransaction.TransactionType.STOCK_IN,
    StockTransaction.TransactionType.ADJUSTMENT_IN,
}


@transaction.atomic
def record_stock_transaction(*, item, transaction_type, quantity, created_by, **extra):
    locked_item = InventoryItem.objects.select_for_update().get(pk=item.pk)
    delta = quantity if transaction_type in INCOMING else -quantity
    new_stock = locked_item.current_stock + delta
    if new_stock < 0:
        raise ValidationError({"quantity": "Insufficient stock for this transaction."})
    locked_item.current_stock = new_stock
    locked_item.save(update_fields=("current_stock", "updated_at"))
    return StockTransaction.objects.create(
        item=locked_item,
        transaction_type=transaction_type,
        quantity=quantity,
        created_by=created_by,
        **extra,
    )

