from django.core.exceptions import ValidationError
from django.db import transaction

from apps.farms.models import PoultryHouse

from .models import BirdMovement, FlockBatch


INCOMING_MOVEMENTS = {
    BirdMovement.MovementType.ARRIVAL,
    BirdMovement.MovementType.ADJUSTMENT_IN,
}


def movement_delta(movement_type, quantity):
    return quantity if movement_type in INCOMING_MOVEMENTS else -quantity


@transaction.atomic
def create_batch(*, created_by, **validated_data):
    house = PoultryHouse.objects.select_for_update().get(pk=validated_data["poultry_house"].pk)
    initial_count = validated_data["initial_bird_count"]
    occupied = sum(
        FlockBatch.objects.filter(
            poultry_house=house,
            status__in=(FlockBatch.Status.ACTIVE, FlockBatch.Status.QUARANTINED),
        ).values_list("current_bird_count", flat=True)
    )
    if validated_data.get("status", FlockBatch.Status.ACTIVE) in (
        FlockBatch.Status.ACTIVE,
        FlockBatch.Status.QUARANTINED,
    ) and occupied + initial_count > house.capacity:
        raise ValidationError({"poultry_house": "This batch would exceed house capacity."})

    batch = FlockBatch.objects.create(
        **validated_data,
        current_bird_count=initial_count,
        created_by=created_by,
    )
    BirdMovement.objects.create(
        batch=batch,
        movement_type=BirdMovement.MovementType.ARRIVAL,
        quantity=initial_count,
        movement_date=batch.arrival_date,
        reference="Initial flock arrival",
        created_by=created_by,
    )
    return batch


@transaction.atomic
def record_bird_movement(*, batch, movement_type, quantity, movement_date, created_by, **extra):
    locked_batch = FlockBatch.objects.select_for_update().get(pk=batch.pk)
    delta = movement_delta(movement_type, quantity)
    new_count = locked_batch.current_bird_count + delta
    if new_count < 0:
        raise ValidationError({"quantity": "Movement exceeds the batch's current bird count."})
    if new_count > locked_batch.initial_bird_count:
        raise ValidationError({"quantity": "Bird count cannot exceed the initial flock size."})
    locked_batch.current_bird_count = new_count
    locked_batch.save(update_fields=("current_bird_count", "updated_at"))
    return BirdMovement.objects.create(
        batch=locked_batch,
        movement_type=movement_type,
        quantity=quantity,
        movement_date=movement_date,
        created_by=created_by,
        **extra,
    )

