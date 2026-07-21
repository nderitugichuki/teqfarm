import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.farms.models import PoultryHouse
from apps.flocks.models import BirdMovement, Breed
from apps.flocks.services import create_batch, record_bird_movement


@pytest.fixture
def manager(db):
    return get_user_model().objects.create_user(
        username="manager3", email="phase3@teqfarm.test", password="SafePass!2468", role="manager"
    )


@pytest.fixture
def flock(manager):
    house = PoultryHouse.objects.create(name="House A", capacity=100, created_by=manager)
    breed = Breed.objects.create(name="Kuroiler", created_by=manager)
    return create_batch(
        created_by=manager, batch_code="TF-001", batch_name="First Flock",
        bird_type="kienyeji", breed=breed, arrival_date=timezone.localdate(),
        initial_bird_count=80, poultry_house=house,
    )


@pytest.mark.django_db
def test_batch_creation_adds_arrival_movement(flock):
    movement = flock.bird_movements.get()
    assert flock.current_bird_count == 80
    assert movement.movement_type == BirdMovement.MovementType.ARRIVAL
    assert movement.quantity == 80


@pytest.mark.django_db
def test_outgoing_movement_updates_count(flock, manager):
    record_bird_movement(
        batch=flock, movement_type=BirdMovement.MovementType.SALE, quantity=10,
        movement_date=timezone.localdate(), created_by=manager,
    )
    flock.refresh_from_db()
    assert flock.current_bird_count == 70


@pytest.mark.django_db
def test_movement_cannot_make_count_negative(flock, manager):
    with pytest.raises(ValidationError):
        record_bird_movement(
            batch=flock, movement_type=BirdMovement.MovementType.MORTALITY, quantity=81,
            movement_date=timezone.localdate(), created_by=manager,
        )

