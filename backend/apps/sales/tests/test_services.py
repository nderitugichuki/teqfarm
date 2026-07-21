from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.eggs.models import EggInventory
from apps.sales.models import Customer, Sale
from apps.sales.services import create_sale


@pytest.mark.django_db
def test_egg_sale_updates_inventory_and_calculates_total():
    user = get_user_model().objects.create_user(username="seller", email="seller@test.dev")
    customer = Customer.objects.create(name="Local Shop", created_by=user)
    EggInventory.objects.create(pk=1, good_eggs=100, created_by=user)
    sale = create_sale(
        created_by=user, sale_type=Sale.SaleType.EGGS, customer=customer,
        quantity=Decimal("30"), unit="egg", unit_price=Decimal("15"),
        amount_paid=Decimal("450"), payment_method=Sale.PaymentMethod.CASH,
        payment_status=Sale.PaymentStatus.PAID, sale_date=timezone.localdate(),
    )
    assert sale.total_amount == Decimal("450.00")
    assert sale.invoice_number.startswith("TF-")
    assert EggInventory.objects.get(pk=1).good_eggs == 70

