from datetime import timedelta
from django.db.models import F
from django.utils import timezone
from apps.daily_records.models import DailyFarmRecord
from apps.farms.models import PoultryHouse
from apps.health.models import Vaccination
from apps.inventory.models import InventoryItem, StockTransaction
from .models import Notification


def _alert(active, *, fingerprint, **defaults):
    Notification.objects.update_or_create(
        fingerprint=fingerprint, defaults={**defaults, "is_resolved": False}
    )
    active.add(fingerprint)


def refresh_alerts():
    today = timezone.localdate()
    active = set()
    for item in InventoryItem.objects.filter(is_active=True, current_stock__lte=F("reorder_level")):
        _alert(active, fingerprint=f"low-stock:{item.pk}", alert_type="low_stock",
               severity="critical" if item.current_stock == 0 else "warning",
               title=f"Low stock: {item.name}",
               message=f"{item.current_stock} {item.unit} remaining; reorder level is {item.reorder_level}.",
               resource_type="inventory_item", resource_id=item.pk)
    expiring = StockTransaction.objects.filter(
        item__category__in=(InventoryItem.Category.MEDICINE, InventoryItem.Category.VACCINE),
        transaction_type=StockTransaction.TransactionType.STOCK_IN,
        expiry_date__range=(today, today + timedelta(days=30)),
    ).select_related("item")
    for stock in expiring:
        _alert(active, fingerprint=f"expiry:{stock.pk}", alert_type="expiry", severity="warning",
               title=f"Expiring: {stock.item.name}",
               message=f"Stock entry expires on {stock.expiry_date}.", due_date=stock.expiry_date,
               resource_type="stock_transaction", resource_id=stock.pk)
    for vaccination in Vaccination.objects.filter(
        status=Vaccination.Status.SCHEDULED,
        scheduled_date__lte=today + timedelta(days=7),
    ).select_related("batch", "vaccine"):
        severity = "critical" if vaccination.scheduled_date < today else "warning"
        _alert(active, fingerprint=f"vaccination:{vaccination.pk}", alert_type="vaccination",
               severity=severity, title=f"Vaccination due: {vaccination.batch.batch_code}",
               message=f"{vaccination.vaccine.name} is scheduled for {vaccination.scheduled_date}.",
               due_date=vaccination.scheduled_date, resource_type="vaccination", resource_id=vaccination.pk)
    recent_records = DailyFarmRecord.objects.filter(
        record_date__gte=today - timedelta(days=1), dead_birds__gt=0
    ).select_related("batch")
    for record in recent_records:
        flock_size = record.batch.current_bird_count + record.dead_birds
        if record.dead_birds < 5 and record.dead_birds < flock_size * 0.02:
            continue
        _alert(active, fingerprint=f"mortality:{record.pk}", alert_type="mortality", severity="critical",
               title=f"High mortality: {record.batch.batch_code}",
               message=f"{record.dead_birds} deaths recorded on {record.record_date}.",
               due_date=record.record_date, resource_type="daily_record", resource_id=record.pk)
    for house in PoultryHouse.objects.filter(is_active=True, next_cleaning_at__lte=today):
        _alert(active, fingerprint=f"cleaning:{house.pk}:{house.next_cleaning_at}",
               alert_type="cleaning", severity="warning", title=f"Cleaning due: {house.name}",
               message=f"Cleaning was scheduled for {house.next_cleaning_at}.",
               due_date=house.next_cleaning_at, resource_type="poultry_house", resource_id=house.pk)
    Notification.objects.filter(is_resolved=False).exclude(fingerprint__in=active).update(is_resolved=True)
    return len(active)
