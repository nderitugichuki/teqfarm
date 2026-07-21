from django.core.exceptions import ValidationError
from django.db import transaction

from apps.flocks.models import BirdMovement, FlockBatch
from apps.inventory.models import InventoryItem, StockTransaction

from .models import DailyFarmRecord


def _apply_mortality(*, record, old_quantity, actor):
    batch = FlockBatch.objects.select_for_update().get(pk=record.batch_id)
    corrected_count = batch.current_bird_count + old_quantity - record.dead_birds
    if corrected_count < 0:
        raise ValidationError({"dead_birds": "Mortality exceeds the current bird count."})

    batch.current_bird_count = corrected_count
    batch.save(update_fields=("current_bird_count", "updated_at"))

    if record.dead_birds == 0:
        if record.mortality_movement_id:
            record.mortality_movement.delete()
            record.mortality_movement = None
            record.save(update_fields=("mortality_movement", "updated_at"))
        return

    if record.mortality_movement_id:
        movement = record.mortality_movement
        movement.quantity = record.dead_birds
        movement.movement_date = record.record_date
        movement.notes = "Generated from daily farm record"
        movement.save(update_fields=("quantity", "movement_date", "notes", "updated_at"))
    else:
        movement = BirdMovement.objects.create(
            batch=batch,
            movement_type=BirdMovement.MovementType.MORTALITY,
            quantity=record.dead_birds,
            movement_date=record.record_date,
            reference=f"Daily record #{record.pk}",
            notes="Generated from daily farm record",
            created_by=actor,
        )
        record.mortality_movement = movement
        record.save(update_fields=("mortality_movement", "updated_at"))


def _sync_feed(*, record, actor):
    transaction_record = record.feed_transaction
    old_quantity = transaction_record.quantity if transaction_record else 0
    old_item_id = transaction_record.item_id if transaction_record else None
    item_ids = sorted({pk for pk in (old_item_id, record.feed_item_id) if pk})
    locked = {item.pk: item for item in InventoryItem.objects.select_for_update().filter(pk__in=item_ids)}
    if old_item_id:
        locked[old_item_id].current_stock += old_quantity
    if record.feed_issued_kg > 0:
        if not record.feed_item_id or record.feed_item.category != InventoryItem.Category.FEED:
            raise ValidationError({"feed_item": "Select a feed inventory item."})
        item = locked[record.feed_item_id]
        if item.current_stock < record.feed_issued_kg:
            raise ValidationError({"feed_issued_kg": "Insufficient feed stock."})
        item.current_stock -= record.feed_issued_kg
    for item in locked.values():
        item.save(update_fields=("current_stock", "updated_at"))

    if record.feed_issued_kg == 0:
        if transaction_record:
            record.feed_transaction = None
            record.save(update_fields=("feed_transaction", "updated_at"))
            transaction_record.delete()
        return
    if transaction_record:
        transaction_record.item_id = record.feed_item_id
        transaction_record.quantity = record.feed_issued_kg
        transaction_record.transaction_date = record.record_date
        transaction_record.save(update_fields=("item", "quantity", "transaction_date", "updated_at"))
    else:
        transaction_record = StockTransaction.objects.create(
            item_id=record.feed_item_id, transaction_type=StockTransaction.TransactionType.STOCK_OUT,
            quantity=record.feed_issued_kg, transaction_date=record.record_date,
            reference=f"Daily record #{record.pk}", created_by=actor,
        )
        record.feed_transaction = transaction_record
        record.save(update_fields=("feed_transaction", "updated_at"))


@transaction.atomic
def create_daily_record(*, created_by, **validated_data):
    record = DailyFarmRecord.objects.create(created_by=created_by, **validated_data)
    _apply_mortality(record=record, old_quantity=0, actor=created_by)
    _sync_feed(record=record, actor=created_by)
    from apps.eggs.services import sync_daily_egg_production
    sync_daily_egg_production(record)
    return record


@transaction.atomic
def update_daily_record(*, instance, actor, **validated_data):
    record = DailyFarmRecord.objects.select_for_update().get(pk=instance.pk)
    old_quantity = record.dead_birds
    old_batch_id = record.batch_id
    for field, value in validated_data.items():
        setattr(record, field, value)
    if record.batch_id != old_batch_id:
        raise ValidationError({"batch": "A daily record cannot be moved to another batch."})
    record.save()
    _apply_mortality(record=record, old_quantity=old_quantity, actor=actor)
    _sync_feed(record=record, actor=actor)
    from apps.eggs.services import sync_daily_egg_production
    sync_daily_egg_production(record)
    return record


@transaction.atomic
def delete_daily_record(*, instance):
    record = DailyFarmRecord.objects.select_for_update().get(pk=instance.pk)
    batch = FlockBatch.objects.select_for_update().get(pk=record.batch_id)
    movement = record.mortality_movement
    from apps.eggs.services import reverse_daily_egg_production
    reverse_daily_egg_production(record)
    feed_transaction = record.feed_transaction
    if feed_transaction:
        item = InventoryItem.objects.select_for_update().get(pk=feed_transaction.item_id)
        item.current_stock += feed_transaction.quantity
        item.save(update_fields=("current_stock", "updated_at"))
    batch.current_bird_count += record.dead_birds
    batch.save(update_fields=("current_bird_count", "updated_at"))
    record.delete()
    if movement:
        movement.delete()
    if feed_transaction:
        feed_transaction.delete()
