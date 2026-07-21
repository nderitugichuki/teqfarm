from django.core.management.base import BaseCommand

from apps.daily_records.models import DailyFarmRecord
from apps.eggs.models import EggInventory, EggProduction
from apps.expenses.models import Expense
from apps.farms.models import PoultryHouse
from apps.feed.models import FeedIssue, FeedPurchase, FeedSupplier
from apps.flocks.models import BirdMovement, FlockBatch
from apps.health.models import DiseaseRecord, MedicationRecord, Vaccination, VetVisit
from apps.inventory.models import InventoryItem, StockTransaction
from apps.notifications.models import Notification
from apps.reports.services import build_report
from apps.sales.models import Customer, Sale


class Command(BaseCommand):
    help = "Run a simple TeqFarm demo smoke test against seeded local data."

    def handle(self, *args, **options):
        checks = [
            ("Poultry houses", PoultryHouse.objects.filter(name__startswith="DEMO").count()),
            ("Flock batches", FlockBatch.objects.filter(batch_code__startswith="DEMO").count()),
            ("Bird movements", BirdMovement.objects.filter(batch__batch_code__startswith="DEMO").count()),
            ("Inventory items", InventoryItem.objects.filter(sku__startswith="DEMO").count()),
            ("Stock transactions", StockTransaction.objects.filter(reference__startswith="DEMO").count()),
            ("Feed suppliers", FeedSupplier.objects.filter(name__startswith="DEMO").count()),
            ("Feed purchases", FeedPurchase.objects.filter(invoice_number__startswith="DEMO").count()),
            ("Feed issues", FeedIssue.objects.filter(notes__startswith="DEMO").count()),
            ("Daily records", DailyFarmRecord.objects.filter(batch__batch_code__startswith="DEMO").count()),
            ("Egg production", EggProduction.objects.filter(batch__batch_code__startswith="DEMO").count()),
            ("Egg inventory rows", EggInventory.objects.count()),
            ("Vaccinations", Vaccination.objects.filter(batch__batch_code__startswith="DEMO").count()),
            ("Medication records", MedicationRecord.objects.filter(batch__batch_code__startswith="DEMO").count()),
            ("Disease records", DiseaseRecord.objects.filter(disease_name__startswith="DEMO").count()),
            ("Vet visits", VetVisit.objects.filter(veterinarian__startswith="Dr Demo").count()),
            ("Customers", Customer.objects.filter(name__startswith="DEMO").count()),
            ("Sales", Sale.objects.filter(notes__startswith="DEMO").count()),
            ("Expenses", Expense.objects.filter(description__startswith="DEMO").count()),
            ("Active notifications", Notification.objects.filter(is_resolved=False).count()),
        ]

        failures = []
        for name, count in checks:
            status = "OK" if count > 0 else "MISSING"
            self.stdout.write(f"{status:8} {name}: {count}")
            if count <= 0:
                failures.append(name)

        for report_type in (
            "daily",
            "production",
            "mortality",
            "feed",
            "sales",
            "expenses",
            "profit-loss",
            "inventory",
        ):
            try:
                report = build_report(report_type=report_type)
                rows = len(report)
                self.stdout.write(f"OK       Report {report_type}: {rows} rows")
            except Exception as exc:  # noqa: BLE001 - smoke command should report all failures.
                failures.append(f"Report {report_type}: {exc}")
                self.stdout.write(self.style.ERROR(f"FAILED   Report {report_type}: {exc}"))

        layers = FlockBatch.objects.filter(batch_code="DEMO-LAY-001").first()
        broilers = FlockBatch.objects.filter(batch_code="DEMO-BRO-001").first()
        eggs = EggInventory.objects.filter(pk=1).first()
        feed = InventoryItem.objects.filter(sku="DEMO-FEED-LM").first()
        vaccine = InventoryItem.objects.filter(sku="DEMO-VAC-ND").first()
        medicine = InventoryItem.objects.filter(sku="DEMO-MED-AMOX").first()

        if layers:
            self.stdout.write(f"INFO     DEMO-LAY-001 current birds: {layers.current_bird_count}")
        if broilers:
            self.stdout.write(f"INFO     DEMO-BRO-001 current birds: {broilers.current_bird_count}")
        if eggs:
            self.stdout.write(f"INFO     Good egg stock after egg sale: {eggs.good_eggs}")
        if feed:
            self.stdout.write(f"INFO     Layers Mash stock after purchases/issues: {feed.current_stock} {feed.unit}")
        if vaccine:
            self.stdout.write(f"INFO     Vaccine stock after vaccination: {vaccine.current_stock} {vaccine.unit}")
        if medicine:
            self.stdout.write(f"INFO     Medicine stock after medication: {medicine.current_stock} {medicine.unit}")

        if failures:
            self.stderr.write(self.style.ERROR("Smoke test found issues:"))
            for failure in failures:
                self.stderr.write(f" - {failure}")
            raise SystemExit(1)

        self.stdout.write(self.style.SUCCESS("Smoke test passed. Demo data is ready for UI testing."))
