from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.daily_records.services import create_daily_record, delete_daily_record, update_daily_record
from apps.farms.models import PoultryHouse
from apps.flocks.models import BirdMovement, Breed
from apps.flocks.services import create_batch
from apps.inventory.models import InventoryItem, StockTransaction
from apps.inventory.services import record_stock_transaction


@pytest.fixture
def worker_and_batch(db):
    user = get_user_model().objects.create_user(
        username="worker", email="worker@teqfarm.test", password="SafePass!2468", role="worker"
    )
    house = PoultryHouse.objects.create(name="House B", capacity=200, created_by=user)
    breed = Breed.objects.create(name="Kenbro", created_by=user)
    batch = create_batch(
        created_by=user, batch_code="TF-002", batch_name="Broilers",
        bird_type="broilers", breed=breed, arrival_date=timezone.localdate(),
        initial_bird_count=100, poultry_house=house,
    )
    return user, batch


@pytest.mark.django_db
def test_daily_mortality_updates_flock_and_ledger(worker_and_batch):
    user, batch = worker_and_batch
    record = create_daily_record(
        created_by=user, batch=batch, record_date=timezone.localdate(), dead_birds=3,
        eggs_collected=0,
    )
    batch.refresh_from_db()
    assert batch.current_bird_count == 97
    assert record.mortality_movement.movement_type == BirdMovement.MovementType.MORTALITY


@pytest.mark.django_db
def test_correcting_mortality_reconciles_flock_count(worker_and_batch):
    user, batch = worker_and_batch
    record = create_daily_record(
        created_by=user, batch=batch, record_date=timezone.localdate(), dead_birds=4,
    )
    update_daily_record(instance=record, actor=user, dead_birds=1)
    batch.refresh_from_db()
    record.refresh_from_db()
    assert batch.current_bird_count == 99
    assert record.mortality_movement.quantity == 1


@pytest.mark.django_db
def test_deleting_record_reverses_mortality(worker_and_batch):
    user, batch = worker_and_batch
    record = create_daily_record(
        created_by=user, batch=batch, record_date=timezone.localdate(), dead_birds=2,
    )
    movement_id = record.mortality_movement_id
    delete_daily_record(instance=record)
    batch.refresh_from_db()
    assert batch.current_bird_count == 100
    assert not BirdMovement.objects.filter(pk=movement_id).exists()


@pytest.mark.django_db
def test_daily_feed_issue_reconciles_inventory(worker_and_batch):
    user, batch = worker_and_batch
    feed = InventoryItem.objects.create(
        name="Broiler Starter", sku="BS-1", category="feed", unit="kg", created_by=user
    )
    record_stock_transaction(
        item=feed, transaction_type=StockTransaction.TransactionType.STOCK_IN,
        quantity=Decimal("50"), transaction_date=timezone.localdate(), created_by=user,
    )
    record = create_daily_record(
        created_by=user, batch=batch, record_date=timezone.localdate(),
        feed_item=feed, feed_issued_kg=Decimal("7.5"),
    )
    feed.refresh_from_db()
    assert feed.current_stock == Decimal("42.5")
    assert record.feed_transaction.quantity == Decimal("7.5")
