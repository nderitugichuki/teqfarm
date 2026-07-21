from django.db import transaction
from django.core.exceptions import ValidationError
from .models import EggInventory, EggProduction

@transaction.atomic
def sync_daily_egg_production(record):
    balance, _ = EggInventory.objects.select_for_update().get_or_create(pk=1)
    production = EggProduction.objects.filter(daily_record=record).first()
    old_good = production.good_eggs if production else 0
    old_broken = production.broken_eggs if production else 0
    old_dirty = production.dirty_eggs if production else 0
    good = record.good_eggs
    new_good = balance.good_eggs + good - old_good
    new_broken = balance.broken_eggs + record.broken_eggs - old_broken
    new_dirty = balance.dirty_eggs + record.dirty_eggs - old_dirty
    if min(new_good, new_broken, new_dirty) < 0:
        raise ValidationError({"eggs_collected": "Production cannot be reduced below eggs already issued or sold."})
    balance.good_eggs = new_good
    balance.broken_eggs = new_broken
    balance.dirty_eggs = new_dirty
    balance.save()
    EggProduction.objects.update_or_create(
        daily_record=record,
        defaults={"batch": record.batch, "production_date": record.record_date,
                  "good_eggs": good, "broken_eggs": record.broken_eggs,
                  "dirty_eggs": record.dirty_eggs, "created_by": record.created_by},
    )

@transaction.atomic
def reverse_daily_egg_production(record):
    production = EggProduction.objects.select_for_update().filter(daily_record=record).first()
    if not production:
        return
    balance = EggInventory.objects.select_for_update().get(pk=1)
    if (balance.good_eggs < production.good_eggs or
            balance.broken_eggs < production.broken_eggs or
            balance.dirty_eggs < production.dirty_eggs):
        raise ValidationError({"eggs_collected": "This record cannot be deleted after its eggs have been issued or sold."})
    balance.good_eggs -= production.good_eggs
    balance.broken_eggs -= production.broken_eggs
    balance.dirty_eggs -= production.dirty_eggs
    balance.save()
    production.delete()
