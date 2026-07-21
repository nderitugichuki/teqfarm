from datetime import timedelta
from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from apps.daily_records.models import DailyFarmRecord
from apps.expenses.models import Expense
from apps.farms.models import PoultryHouse
from apps.flocks.models import FlockBatch
from apps.health.models import Vaccination
from apps.inventory.models import InventoryItem
from apps.sales.models import Sale


def dashboard_summary(*, include_financials=True):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    chart_start = today - timedelta(days=29)
    active_statuses = (FlockBatch.Status.ACTIVE, FlockBatch.Status.QUARANTINED)
    total_birds = FlockBatch.objects.filter(status__in=active_statuses).aggregate(
        total=Sum("current_bird_count")
    )["total"] or 0
    daily = DailyFarmRecord.objects.filter(record_date=today).aggregate(
        eggs=Sum("eggs_collected"), mortality=Sum("dead_birds")
    )
    feed_stock = InventoryItem.objects.filter(
        category=InventoryItem.Category.FEED, is_active=True
    ).aggregate(total=Sum("current_stock"))["total"] or Decimal("0")
    upcoming = Vaccination.objects.filter(
        status=Vaccination.Status.SCHEDULED,
        scheduled_date__range=(today, today + timedelta(days=7)),
    ).count()

    production_chart = list(
        DailyFarmRecord.objects.filter(record_date__gte=chart_start)
        .values("record_date").annotate(eggs=Sum("eggs_collected"))
        .order_by("record_date")
    )
    sales_chart = list(
        Sale.objects.filter(sale_date__gte=chart_start)
        .annotate(day=TruncDate("sale_date"))
        .values("day").annotate(amount=Sum("total_amount"))
        .order_by("day")
    )
    quick_actions = [
        {"key": "daily_record", "label": "Record daily data", "path": "/daily-records?new=1"},
        {"key": "feed_issue", "label": "Issue feed", "path": "/feed?tab=Issues&new=1"},
        {"key": "mortality", "label": "Record mortality", "path": "/daily-records?new=1"},
    ]
    if include_financials:
        quick_actions.insert(
            2, {"key": "sale", "label": "Record sale", "path": "/sales?tab=Sales&new=1"}
        )

    result = {
        "total_birds": total_birds,
        "birds_by_batch": list(
            FlockBatch.objects.filter(status__in=active_statuses)
            .values("id", "batch_code", "batch_name", "current_bird_count")
            .order_by("batch_code")
        ),
        "active_poultry_houses": PoultryHouse.objects.filter(is_active=True).count(),
        "eggs_collected_today": daily["eggs"] or 0,
        "feed_stock_kg": feed_stock,
        "mortality_today": daily["mortality"] or 0,
        "upcoming_vaccinations": upcoming,
        "production_chart": production_chart,
        "sales_chart": sales_chart if include_financials else [],
        "quick_actions": quick_actions,
    }
    if include_financials:
        sales = Sale.objects.filter(sale_date__gte=month_start).aggregate(
            total=Sum("total_amount")
        )["total"] or Decimal("0")
        expenses = Expense.objects.filter(expense_date__gte=month_start).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")
        result["financials"] = {
            "sales_this_month": sales,
            "expenses_this_month": expenses,
            "profit_this_month": sales - expenses,
        }
    return result
