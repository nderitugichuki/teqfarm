from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.inventory.models import InventoryItem, StockTransaction
from apps.inventory.services import record_stock_transaction

@pytest.mark.django_db
def test_stock_ledger_prevents_negative_balance():
    user = get_user_model().objects.create_user(username="stock", email="stock@test.dev")
    item = InventoryItem.objects.create(name="Layers Mash", sku="FEED-1", category="feed", unit="kg", created_by=user)
    record_stock_transaction(item=item, transaction_type="in", quantity=Decimal("10"), transaction_date=timezone.localdate(), created_by=user)
    with pytest.raises(ValidationError):
        record_stock_transaction(item=item, transaction_type="out", quantity=Decimal("11"), transaction_date=timezone.localdate(), created_by=user)
    item.refresh_from_db()
    assert item.current_stock == Decimal("10")
    assert StockTransaction.objects.count() == 1
