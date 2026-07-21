from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.dashboard.selectors import dashboard_summary
from apps.expenses.models import Expense
from apps.sales.models import Customer, Sale

@pytest.mark.django_db
def test_dashboard_profit_uses_sales_less_expenses():
    user = get_user_model().objects.create_user(username="dash", email="dash@test.dev")
    customer = Customer.objects.create(name="Buyer", created_by=user)
    Sale.objects.create(customer=customer, sale_type="manure", sale_date=timezone.localdate(),
        quantity=1, unit="bag", unit_price=500, total_amount=500, amount_paid=500,
        payment_method="cash", payment_status="paid", created_by=user)
    Expense.objects.create(expense_date=timezone.localdate(), category="fuel",
        description="Delivery", amount=Decimal("125"), payment_method="cash", created_by=user)
    result = dashboard_summary()
    assert result["financials"]["profit_this_month"] == Decimal("375")

