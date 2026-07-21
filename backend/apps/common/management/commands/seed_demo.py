from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.daily_records.models import DailyFarmRecord
from apps.daily_records.services import create_daily_record
from apps.expenses.models import Expense
from apps.farms.models import PoultryHouse
from apps.feed.models import FeedIssue, FeedPurchase, FeedSupplier
from apps.flocks.models import Breed, FlockBatch, Supplier
from apps.flocks.services import create_batch
from apps.health.models import DiseaseRecord, MedicationRecord, Vaccination, VetVisit
from apps.inventory.models import InventoryItem, StockTransaction
from apps.inventory.services import record_stock_transaction
from apps.notifications.services import refresh_alerts
from apps.sales.models import Customer, Sale
from apps.sales.services import create_sale


class Command(BaseCommand):
    help = "Seed TeqFarm with realistic demo data for local testing."

    def handle(self, *args, **options):
        today = timezone.localdate()
        User = get_user_model()
        actor = User.objects.filter(username="admin").first() or User.objects.filter(is_superuser=True).first()
        if not actor:
            self.stderr.write(self.style.ERROR("Create a superuser first, then rerun seed_demo."))
            return

        if FlockBatch.objects.filter(batch_code="DEMO-LAY-001").exists():
            self.stdout.write(self.style.WARNING("Demo data already exists. Skipping duplicate seed."))
            self.stdout.write("Open the UI and look for records starting with DEMO.")
            return

        with transaction.atomic():
            house_a = PoultryHouse.objects.create(
                name="DEMO House A - Layers",
                capacity=1000,
                notes="Demo main layers house.",
                cleaning_interval_days=7,
                next_cleaning_at=today - timedelta(days=1),
                created_by=actor,
            )
            house_b = PoultryHouse.objects.create(
                name="DEMO House B - Broilers",
                capacity=600,
                notes="Demo broiler house.",
                cleaning_interval_days=14,
                next_cleaning_at=today + timedelta(days=5),
                created_by=actor,
            )

            bird_supplier = Supplier.objects.create(
                name="DEMO Kenchic Supplier",
                contact_person="Mary Demo",
                phone_number="0711000000",
                email="supplier.demo@example.com",
                created_by=actor,
            )
            isa_brown = Breed.objects.create(
                name="DEMO ISA Brown",
                description="Demo commercial layer breed.",
                created_by=actor,
            )
            cobb = Breed.objects.create(
                name="DEMO Cobb 500",
                description="Demo broiler breed.",
                created_by=actor,
            )

            layers = create_batch(
                created_by=actor,
                batch_code="DEMO-LAY-001",
                batch_name="Demo July Layers",
                bird_type=FlockBatch.BirdType.LAYERS,
                breed=isa_brown,
                supplier=bird_supplier,
                arrival_date=today - timedelta(days=45),
                initial_bird_count=800,
                purchase_cost=Decimal("240000.00"),
                poultry_house=house_a,
                status=FlockBatch.Status.ACTIVE,
                notes="Demo flock used to test egg production, feed, health and sales.",
            )
            broilers = create_batch(
                created_by=actor,
                batch_code="DEMO-BRO-001",
                batch_name="Demo Broiler Batch",
                bird_type=FlockBatch.BirdType.BROILERS,
                breed=cobb,
                supplier=bird_supplier,
                arrival_date=today - timedelta(days=21),
                initial_bird_count=450,
                purchase_cost=Decimal("67500.00"),
                poultry_house=house_b,
                status=FlockBatch.Status.ACTIVE,
                notes="Demo flock used to test live bird sales.",
            )

            layers_mash = InventoryItem.objects.create(
                sku="DEMO-FEED-LM",
                name="DEMO Layers Mash",
                category=InventoryItem.Category.FEED,
                unit="kg",
                reorder_level=Decimal("100.00"),
                created_by=actor,
            )
            broiler_starter = InventoryItem.objects.create(
                sku="DEMO-FEED-BS",
                name="DEMO Broiler Starter",
                category=InventoryItem.Category.FEED,
                unit="kg",
                reorder_level=Decimal("75.00"),
                created_by=actor,
            )
            vaccine = InventoryItem.objects.create(
                sku="DEMO-VAC-ND",
                name="DEMO Newcastle Vaccine",
                category=InventoryItem.Category.VACCINE,
                unit="doses",
                reorder_level=Decimal("100.00"),
                created_by=actor,
            )
            medicine = InventoryItem.objects.create(
                sku="DEMO-MED-AMOX",
                name="DEMO Amoxicillin",
                category=InventoryItem.Category.MEDICINE,
                unit="bottles",
                reorder_level=Decimal("3.00"),
                created_by=actor,
            )
            trays = InventoryItem.objects.create(
                sku="DEMO-TRAY-001",
                name="DEMO Egg Trays",
                category=InventoryItem.Category.EGG_TRAY,
                unit="pieces",
                reorder_level=Decimal("20.00"),
                created_by=actor,
            )
            drinker = InventoryItem.objects.create(
                sku="DEMO-EQP-DRINKER",
                name="DEMO Bell Drinker",
                category=InventoryItem.Category.EQUIPMENT,
                unit="pieces",
                reorder_level=Decimal("2.00"),
                created_by=actor,
            )

            for item, qty, cost, expiry in (
                (layers_mash, Decimal("500.00"), Decimal("65.00"), None),
                (broiler_starter, Decimal("300.00"), Decimal("72.00"), None),
                (vaccine, Decimal("1000.00"), Decimal("2.00"), today + timedelta(days=20)),
                (medicine, Decimal("10.00"), Decimal("450.00"), today + timedelta(days=25)),
                (trays, Decimal("120.00"), Decimal("25.00"), None),
                (drinker, Decimal("10.00"), Decimal("850.00"), None),
            ):
                record_stock_transaction(
                    item=item,
                    transaction_type=StockTransaction.TransactionType.STOCK_IN,
                    quantity=qty,
                    transaction_date=today - timedelta(days=3),
                    expiry_date=expiry,
                    unit_cost=cost,
                    reference="DEMO opening stock",
                    created_by=actor,
                )

            feed_supplier = FeedSupplier.objects.create(
                name="DEMO Unga Feeds",
                phone_number="0722000000",
                email="feeds.demo@example.com",
                created_by=actor,
            )
            purchase_stock = record_stock_transaction(
                item=layers_mash,
                transaction_type=StockTransaction.TransactionType.STOCK_IN,
                quantity=Decimal("250.00"),
                transaction_date=today - timedelta(days=2),
                unit_cost=Decimal("64.00"),
                reference="DEMO-FEED-INV-001",
                created_by=actor,
            )
            FeedPurchase.objects.create(
                item=layers_mash,
                supplier=feed_supplier,
                quantity_kg=Decimal("250.00"),
                unit_cost=Decimal("64.00"),
                purchase_date=today - timedelta(days=2),
                invoice_number="DEMO-FEED-INV-001",
                stock_transaction=purchase_stock,
                created_by=actor,
            )

            issue_stock = record_stock_transaction(
                item=broiler_starter,
                transaction_type=StockTransaction.TransactionType.STOCK_OUT,
                quantity=Decimal("25.00"),
                transaction_date=today - timedelta(days=1),
                reference=broilers.batch_code,
                notes="DEMO broiler feed issue.",
                created_by=actor,
            )
            FeedIssue.objects.create(
                item=broiler_starter,
                batch=broilers,
                quantity_kg=Decimal("25.00"),
                issue_date=today - timedelta(days=1),
                notes="DEMO broiler feed issue.",
                stock_transaction=issue_stock,
                created_by=actor,
            )

            create_daily_record(
                created_by=actor,
                batch=layers,
                record_date=today - timedelta(days=1),
                eggs_collected=430,
                broken_eggs=8,
                dirty_eggs=12,
                feed_item=layers_mash,
                feed_issued_kg=Decimal("38.00"),
                water_notes="Water line normal.",
                sick_birds=3,
                dead_birds=1,
                observations="Demo: birds active, production steady.",
            )
            create_daily_record(
                created_by=actor,
                batch=layers,
                record_date=today,
                eggs_collected=420,
                broken_eggs=6,
                dirty_eggs=10,
                feed_item=layers_mash,
                feed_issued_kg=Decimal("37.50"),
                water_notes="Water pressure okay.",
                sick_birds=2,
                dead_birds=2,
                observations="Demo: minor coughing noticed near corner drinker.",
            )
            create_daily_record(
                created_by=actor,
                batch=broilers,
                record_date=today,
                eggs_collected=0,
                broken_eggs=0,
                dirty_eggs=0,
                feed_item=broiler_starter,
                feed_issued_kg=Decimal("28.00"),
                water_notes="Brooder drinkers refilled.",
                sick_birds=1,
                dead_birds=6,
                observations="Demo high mortality record to trigger alert.",
            )

            completed_stock = record_stock_transaction(
                item=vaccine,
                transaction_type=StockTransaction.TransactionType.STOCK_OUT,
                quantity=Decimal("800.00"),
                transaction_date=today - timedelta(days=1),
                reference=layers.batch_code,
                created_by=actor,
            )
            Vaccination.objects.create(
                batch=layers,
                vaccine=vaccine,
                scheduled_date=today - timedelta(days=1),
                administered_date=today - timedelta(days=1),
                dose_quantity=Decimal("800.00"),
                status=Vaccination.Status.COMPLETED,
                notes="Demo completed Newcastle vaccination via drinking water.",
                stock_transaction=completed_stock,
                created_by=actor,
            )
            Vaccination.objects.create(
                batch=broilers,
                vaccine=vaccine,
                scheduled_date=today + timedelta(days=3),
                dose_quantity=Decimal("0.00"),
                status=Vaccination.Status.SCHEDULED,
                notes="Demo upcoming vaccination reminder.",
                created_by=actor,
            )

            med_stock = record_stock_transaction(
                item=medicine,
                transaction_type=StockTransaction.TransactionType.STOCK_OUT,
                quantity=Decimal("2.00"),
                transaction_date=today,
                reference=layers.batch_code,
                created_by=actor,
            )
            MedicationRecord.objects.create(
                batch=layers,
                medicine=medicine,
                start_date=today,
                end_date=today + timedelta(days=4),
                dosage="1 bottle per 100L water",
                reason="Demo respiratory signs.",
                quantity_used=Decimal("2.00"),
                stock_transaction=med_stock,
                created_by=actor,
            )
            DiseaseRecord.objects.create(
                batch=layers,
                disease_name="DEMO Mild respiratory symptoms",
                diagnosed_date=today,
                affected_birds=12,
                symptoms="Coughing and watery eyes.",
                treatment="Amoxicillin in drinking water.",
                created_by=actor,
            )
            VetVisit.objects.create(
                batch=layers,
                visit_date=today,
                veterinarian="Dr Demo Vet",
                reason="Check respiratory symptoms.",
                findings="Mild infection suspected.",
                recommendations="Continue medication and monitor mortality.",
                follow_up_date=today + timedelta(days=5),
                created_by=actor,
            )

            customer = Customer.objects.create(
                name="DEMO Mama Asha Shop",
                phone_number="0733000000",
                email="customer.demo@example.com",
                address="Demo Market Road",
                created_by=actor,
            )
            create_sale(
                created_by=actor,
                sale_date=today,
                sale_type=Sale.SaleType.EGGS,
                customer=customer,
                quantity=Decimal("300.00"),
                unit="eggs",
                unit_price=Decimal("15.00"),
                amount_paid=Decimal("4500.00"),
                payment_method=Sale.PaymentMethod.CASH,
                notes="DEMO sale of 10 trays.",
            )
            create_sale(
                created_by=actor,
                sale_date=today,
                sale_type=Sale.SaleType.LIVE_BIRDS,
                customer=customer,
                batch=broilers,
                quantity=Decimal("20.00"),
                unit="birds",
                unit_price=Decimal("650.00"),
                amount_paid=Decimal("8000.00"),
                payment_method=Sale.PaymentMethod.MOBILE_MONEY,
                notes="DEMO partial payment live bird sale.",
            )
            create_sale(
                created_by=actor,
                sale_date=today,
                sale_type=Sale.SaleType.MANURE,
                customer=customer,
                quantity=Decimal("5.00"),
                unit="bags",
                unit_price=Decimal("250.00"),
                amount_paid=Decimal("0.00"),
                payment_method=Sale.PaymentMethod.CREDIT,
                notes="DEMO manure sale on credit.",
            )

            Expense.objects.create(
                expense_date=today,
                category=Expense.Category.FEED,
                description="DEMO feed transport",
                payee="Demo Transporter",
                amount=Decimal("1500.00"),
                payment_method=Expense.PaymentMethod.CASH,
                reference="DEMO-EXP-001",
                created_by=actor,
            )
            Expense.objects.create(
                expense_date=today,
                category=Expense.Category.MEDICINE,
                description="DEMO vet consultation",
                payee="Dr Demo Vet",
                amount=Decimal("3000.00"),
                payment_method=Expense.PaymentMethod.MOBILE_MONEY,
                reference="DEMO-EXP-002",
                created_by=actor,
            )

            alert_count = refresh_alerts()

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
        self.stdout.write(f"Created demo houses, flocks, inventory, daily records, health, sales, expenses.")
        self.stdout.write(f"Active alerts generated: {alert_count}")
        self.stdout.write("Open the UI and look for records starting with DEMO.")
